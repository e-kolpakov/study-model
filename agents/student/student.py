import logging
from itertools import cycle

from simpy import Interrupt
from pubsub import pub

from agents.base_agents import IntelligentAgent
from agents.student.activities import IdleActivity, StudySessionActivity, PeerStudentInteractionActivity
from agents.student.behaviors.behavior_group import BehaviorGroup
from agents.student.messages import BaseMessage
from infrastructure.observers import Observer, observer_trigger, AgentCallObserver, DeltaObserver
from simulation.resource_access import ResourceRosterMixin
from simulation.result import ResultTopics


__author__ = 'e.kolpakov'


class Student(IntelligentAgent, ResourceRosterMixin):
    def __init__(self, name, knowledge, behavior, skill=None, goals=None, **kwargs):
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
        self._goals = goals or []

        self._logger = logging.getLogger(__name__)

        self._current_activity = None
        self._current_activity_end = None

        # injected properties
        self._curriculum = None
        self._env = None
        self._stop_participation_event = None
        # injected properties end

        self._known_students = {}
        self._inbox = []

        self.__init_activities()
        self.__subscribe_to_inbox()

    def __init_activities(self):
        self._activity_lengths = {
            IdleActivity: self._behavior.activity_periods.get_idle_period,
            StudySessionActivity: self._behavior.activity_periods.get_study_period,
            PeerStudentInteractionActivity: self._behavior.activity_periods.get_peer_interaction_period,
        }

    def __subscribe_to_inbox(self):
        self._logger.info("{student} subscribes to inbox {address}".format(student=self, address=self.inbox_address))
        pub.subscribe(self._receive_message, self.inbox_address)

    def __unicode__(self):
        return "{type} {name}({id})".format(type=type(self).__name__, id=self._agent_id, name=self._name)

    @property
    def name(self):
        return self._name

    @property
    def inbox_address(self):
        return "Student {name} (id: {id})".format(name=self.name, id=self.agent_id)

    @property
    def behavior(self):
        """ :return: BehaviorGroup """
        return self._behavior

    @property
    def current_activity(self):
        return self._current_activity

    @property
    def goals(self):
        return self._goals

    @property
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_SNAPSHOT)
    @Observer.observe(topic=ResultTopics.KNOWLEDGE_COUNT, converter=lambda x: len(x))
    @DeltaObserver.observe(topic=ResultTopics.KNOWLEDGE_DELTA, delta=lambda new, old: new-old)
    def knowledge(self):
        """ :rtype: frozenset """
        return frozenset(self._knowledge)

    @property
    def known_students(self):
        return tuple(self._known_students.values())

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
    def curriculum(self):
        """ :rtype: knowledge_representation.Curriculum """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """ :type value: knowledge_representation.Curriculum """
        self._curriculum = value

    def study(self):
        next_activity_gen = self._get_next_activity()
        for activity in next_activity_gen:
            activity_process = self._start_activity(activity)
            if activity_process:
                yield self.env.process(activity_process)

    @AgentCallObserver.observe(topic=ResultTopics.RESOURCE_USAGE)
    def study_resource(self, resource, until=None):
        """
        :type resource: Resource
        :rtype: None
        """
        self._logger.debug("{self}: Studying resource, until {until}".format(self=self, until=until))
        knowledge_to_acquire = self._behavior.knowledge_acquisition.acquire_facts(self, resource)
        for fact in knowledge_to_acquire:
            fact_study_process = self.study_fact(fact, until)
            success = yield from fact_study_process
            if not success:
                return False

        self._logger.debug("{self}: Studying resource {resource_name} done at {time}".format(
            self=self, resource_name=resource.name, time=self.env.now
        ))
        return True

    def study_fact(self, fact, until=None):
        if fact in self._knowledge:
            self._logger.debug("{student}: {fact} already known - skipping".format(student=self, fact=fact))

        self._logger.debug("{student}: studies {fact}".format(student=self, fact=fact))
        time_to_study = fact.complexity / self.skill
        if until is not None and self.env.now + time_to_study > until:
            self._logger.debug("{self}: not enough time to study fact - skipping".format(self=self))
            return False
        try:
            yield self.env.timeout(time_to_study)
            self._add_fact(fact)
        except Interrupt:
            return False
        return True

    def stop_participation(self):
        # TODO: check if we really wnat to stop participation
        self.stop_participation_event.succeed()

    def get_accessible_resources(self):
        return (resource for resource in self.known_resources if resource.allow_access(self))

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

    def process_messages(self, until=None):
        success = True
        self._logger.debug("{student} starts reading messages (count:{count})".format(
            student=self, count=len(self._inbox)
        ))
        while success and self._inbox:
            message = self._inbox.pop()
            self._logger.debug("{student} reads message {message} from inbox".format(student=self, message=message))
            success = yield from message.process(self, until)

    def send_messages(self, until=None):
        for to_student, messages in self.behavior.send_messages.get_messages(self):
            address = to_student.inbox_address
            for message in messages:
                time_to_send = message.time_to_send(self)
                if until is not None and self.env.now + time_to_send > until:
                    # there might be less involving messages in the queue - should try sending them
                    # On the other hand, it does not allow for short-circuiting out of this process
                    # if there are little time left. TODO: implement short-circuit
                    continue
                yield self.env.timeout(time_to_send)
                self._logger.debug("{student} sends message {message} to {address}".format(
                    student=self, message=message, address=address
                ))
                pub.sendMessage(address, message=message)

    @observer_trigger
    def _add_fact(self, fact):
        self._knowledge.add(fact)

    def _start_activity(self, activity, **kwargs):
        self._logger.debug("{student} Starting activity {activity} with args {kwargs}".format(
            student=self, activity=activity, kwargs=kwargs
        ))
        process = activity.run(**kwargs)
        self._current_activity = activity
        self._current_activity_end = self.env.now + activity.length
        return process

    def _receive_message(self, message):
        if not isinstance(message, BaseMessage):
            message = "Expected message type, got {message}".format(message=message)
            self._logger.warn(message)
            raise ValueError(message)
        self._logger.debug("{student} received message {message}".format(student=self, message=message))
        self._inbox.append(message)

    def _get_next_activity(self):
        for activity_type in cycle([StudySessionActivity, PeerStudentInteractionActivity, IdleActivity]):
            if self.stop_participation_event.processed:
                return
            activity_length = self._activity_lengths.get(activity_type)(self, self.env.now)
            yield activity_type(self, activity_length, self.env)
