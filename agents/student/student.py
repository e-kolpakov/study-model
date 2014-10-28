import logging
from itertools import cycle

from simpy import Interrupt
from pubsub import pub

from agents.base_agents import IntelligentAgent
from agents.student.activities import IdleActivity, StudySessionActivity, PeerStudentInteractionActivity
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.messages import BaseMessage
from infrastructure.observers import Observer, observer_trigger, AgentCallObserver
from simulation.result import ResultTopics


__author__ = 'e.kolpakov'


class Student(IntelligentAgent):
    def __init__(self, name, knowledge, behavior, skill=None, **kwargs):
        """
        :type name: str
        :type knowledge: list[knowledge_representation.Fact]
        :type behavior: BehaviorGroup
        :type skill: double
        """
        super(Student, self).__init__(**kwargs)
        self._name = name
        self._behavior = behavior
        self._knowledge = set(knowledge)
        self._skill = skill if skill else 1

        # injected properties
        self._curriculum = None
        self._env = None
        self._resource_lookup_service = None
        self._stop_participation_event = None

        self._logger = logging.getLogger(__name__)

        self._current_activity = None
        self._current_activity_end = None

        self._known_students = {}
        self._inbox = []

        self.__init_activities()

    def __init_activities(self):
        self._activity_lengths = {
            IdleActivity: self._behavior.activity_periods.get_study_period,
            StudySessionActivity: self._behavior.activity_periods.get_idle_period,
            PeerStudentInteractionActivity: self._behavior.activity_periods.get_peer_interaction_period,
        }

    def __subscribe_to_inbox(self):
        pub.subscribe(self._receive_message, self.inbox_address)

    def __unicode__(self):
        return "{type} {name}({id})".format(type=type(self).__name__, id=self._agent_id, name=self._name)

    @property
    def name(self):
        return self._name

    @property
    def inbox_address(self):
        return "Student {name} (id: {id})".format(self.name, self.agent_id)

    @property
    def behavior(self):
        """ :return: BehaviorGroup """
        return self._behavior

    @property
    def current_activity(self):
        return self._current_activity

    @property
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_SNAPSHOT)
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_COUNT, converter=lambda x: len(x))
    def knowledge(self):
        """ :rtype: frozenset """
        return frozenset(self._knowledge)

    @property
    def stop_participation_event(self):
        if not self._stop_participation_event:
            self._stop_participation_event = self.env.event()
        return self._stop_participation_event

    @property
    def skill(self):
        """ :return: double """
        return self._skill

    @property
    def resource_lookup_service(self):
        """ :rtype: ResourceLookupService """
        return self._resource_lookup_service

    @resource_lookup_service.setter
    def resource_lookup_service(self, value):
        """ :type value: ResourceLookupService """
        self._resource_lookup_service = value

    @property
    def curriculum(self):
        """ :rtype: knowledge_representation.Curriculum """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """ :type value: knowledge_representation.Curriculum """
        self._curriculum = value

    def _get_next_activity(self):
        for activity_type in cycle([StudySessionActivity, PeerStudentInteractionActivity, IdleActivity]):
            if self.stop_participation_event.processed:
                return
            activity_length = self._activity_lengths.get(activity_type)(self, self.env.now)
            yield activity_type(self, activity_length, self.env)

    def study(self):
        next_activity_gen = self._get_next_activity()
        for activity in next_activity_gen:
            activity_process = self._start_activity(activity)
            if activity_process:
                yield self.env.process(activity_process)

    @observer_trigger
    @AgentCallObserver.observe(topic=ResultTopics.RESOURCE_USAGE)
    def study_resource(self, resource, until=100):
        """
        :type resource: Resource
        :rtype: None
        """
        self._logger.debug("{self}: Studying resource, until {until}".format(self=self, until=until))
        knowledge_to_acquire = self._behavior.knowledge_acquisition.acquire_facts(self, resource)
        for fact in knowledge_to_acquire:
            time_to_study = fact.complexity / self.skill
            if self.env.now + time_to_study > until:
                self._logger.debug("{self}: not enough time to study fact - skipping".format(self=self))
                return False
            try:
                yield self.env.timeout(time_to_study)
                self._add_fact(fact)
            except Interrupt:
                return False

        self._logger.debug("{self}: Studying resource {resource_name} done at {time}".format(
            self=self, resource_name=resource.name, time=self.env.now
        ))
        return True

    @observer_trigger
    def _add_fact(self, fact):
        self._knowledge.add(fact)

    def stop_participation(self):
        # TODO: check if we really wnat to stop participation
        self.stop_participation_event.succeed()

    def meet(self, other_student):
        if not isinstance(other_student, Student):
            message = "Expected student, got {other_student}".format(other_student=other_student)
            self._logger.warn(message)
            raise ValueError(message)
        if self == other_student:
            self._logger.info("Student {student} already knows himself".format(student=self))
        if other_student.agent_id in self._known_students.keys():
            self._logger.info("Already met student {other}".format(other=other_student))

        self._known_students[other_student.agent_id] = other_student

    def _start_activity(self, activity, **kwargs):
        self._logger.debug("Starting activity {activity} with args {kwargs}".format(activity=activity, kwargs=kwargs))
        process = activity.run(**kwargs)
        self._current_activity = activity
        self._current_activity_end = self.env.now + activity.length
        return process

    def _receive_message(self, message):
        if not isinstance(message, BaseMessage):
            message = "Expected message type, got {message}".format(message=message)
            self._logger.warn(message)
            raise ValueError(message)
        self._inbox.append(message)