import logging

from simpy import Interrupt

from agents.base_agents import IntelligentAgent
from agents.student.activities import IdleActivity, StudySessionActivity, SymmetricalHandshakeActivity
from agents.student.behaviors.behavior_group import BehaviorGroup
from infrastructure.descriptors import TypedDescriptor
from infrastructure.observers import Observer, observer_trigger, AgentCallObserver
from simulation.result import ResultTopics


__author__ = 'e.kolpakov'


class Student(IntelligentAgent):

    idle_activity = TypedDescriptor(IdleActivity, 'idle_activity')
    study_session_activity = TypedDescriptor(StudySessionActivity, 'study_session_activity')
    handshake_activity = TypedDescriptor(SymmetricalHandshakeActivity, 'handshake_activity')

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
        self._resource_lookup_service = None
        self._stop_participation_event = None

        self._logger = logging.getLogger(__name__)

        self._current_activity = None
        self._current_activity_end = None

        self.__init_activities()

    def __init_activities(self):
        # TODO: improve activity discovery
        self.idle_activity = IdleActivity(self)
        self.study_session_activity = StudySessionActivity(self)
        self.handshake_activity = SymmetricalHandshakeActivity(self)

        self.__activities_list = {
            type(IdleActivity): self.idle_activity,
            type(StudySessionActivity): self.study_session_activity,
            type(SymmetricalHandshakeActivity): self.handshake_activity,
        }

    def __unicode__(self):
        return "{type} {name}({id})".format(type=type(self).__name__, id=self._agent_id, name=self._name)

    @property
    def name(self):
        return self._name

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

    def study(self):
        while not self.stop_participation_event.processed:
            study_session_length = self._behavior.activity_periods.get_study_period(self, self.env.now)
            yield self.env.process(self._activate(self.study_session_activity, study_session_length))

            idle_session_length = self._behavior.activity_periods.get_idle_period(self, self.env.now)
            yield self.env.process(self._activate(self.idle_activity, idle_session_length))

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

    def _activate(self, activity, length, **kwargs):
        process = activity.activate(length, **kwargs)
        self._current_activity = process
        self._current_activity_end = self.env.now + length
        return process

    def stop_participation(self):
        # TODO: check if we really wnat to stop participation
        self.stop_participation_event.succeed()

    def get_next_conversation_availability(self):
        if self._current_activity == self.study_session_activity:
            result = self._current_activity_end
        else:
            result = self.env.now

        assert result > self.env.now
        return result

    def request_activity_start(self, activity_type, length, **kwargs):
        requested_activity = self.__activities_list.get(activity_type, None)
        if requested_activity is None:
            self._logger.warn("Requested activity {type} nt found".format(type=activity_type))
            return False

        self._logger.debug("Requested to start activity {type} with args {kwargs}".format(
            type=activity_type, kwargs=kwargs
        ))

        # TODO: check if we really want to switch activity
        self._activate(requested_activity, length, **kwargs)
        return True
