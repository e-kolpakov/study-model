from collections import defaultdict
import logging
from itertools import cycle

from pubsub import pub

from model.agents.base_agents import IntelligentAgent
from model.agents.student.activities import (
    IdleActivity, StudySessionActivity, PeerStudentInteractionActivity, PassExamActivity
)
from model.agents.student.messages import BaseMessage
from model.infrastructure import INFINITY
from model.infrastructure.observers import Observer, observer_trigger, AgentCallObserver, DeltaObserver
from model.simulation.resource_access import ResourceRosterMixin
from model.simulation.result import ResultTopics


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
        self._exam_results = defaultdict(list)

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
            PassExamActivity: self.behavior.activity_periods.get_pass_exam_period
        }

    def __subscribe_to_inbox(self):
        self._logger.info("{student} subscribes to inbox {address}".format(student=self, address=self.inbox_address))
        pub.subscribe(self._receive_message, self.inbox_address)

    def __lt__(self, other):
        assert isinstance(other, Student)
        return self.agent_id < other.agent_id

    def __eq__(self, other):
        assert isinstance(other, Student)
        return self.agent_id == other.agent_id

    def __hash__(self):
        return hash(self.agent_id)

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
    def exam_results(self):
        return self._exam_results

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
    def check_fact_skill(self):
        # TODO separate parameter for time calculation
        return self._skill * 10

    @property
    def curriculum(self):
        """ :rtype: knowledge_representation.Curriculum """
        return self._curriculum

    @curriculum.setter
    def curriculum(self, value):
        """ :type value: knowledge_representation.Curriculum """
        self._curriculum = value

    def start(self):
        for activity in self._next_activity_generator():
            activity_process = self._start_activity(activity)
            if activity_process:
                yield self.env.process(activity_process)

    def stop_participation(self):
        # TODO: check if we really want to stop participation
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

    @AgentCallObserver.observe(topic=ResultTopics.EXAM_RESULTS)
    def accept_feedback(self, exam=None, exam_feedback=None):
        self._exam_results[exam.code].append(exam_feedback)

    def get_available_exams(self):
        accessible_resources = self.get_accessible_resources()
        return (exam for resource in accessible_resources for exam in resource.exams)

    def estimate_exam_time(self, exam):
        return sum(fact.complexity / self.check_fact_skill for fact in exam.facts)

    # TODO: exam should expose competencies instead of facts, than student should weight his chances of passing based on
    # weighted sum of ratios of mastery of that competencies. For now it uses facts, which essentially means student
    # knows exam questions beforehand.
    # TODO: behavior?
    def _estimate_pass_probability(self, exam):
        knows_facts = exam.facts & self.knowledge
        return len(knows_facts) / float(len(exam.facts))

    def expects_can_pass(self, exam):
        """
        Student perception of if it can pass an exam
        :param Exam exam: exam to check
        :return: bool
        """
        return self._estimate_pass_probability(exam) > 0.8

    # TODO: behavior (goal driven)
    def choose_exam(self, complete_before=INFINITY):
        exams = self.get_available_exams()
        exam_map = {
            exam: self._estimate_pass_probability(exam)
            for exam in exams
            if self.env.now + self.estimate_exam_time(exam) <= complete_before
        }
        exams_to_attempt = {
            exam: exam.weight * probability
            for exam, probability in exam_map.items()
            if self.expects_can_pass(exam) and not self._passed_exam(exam)
        }
        if not exams_to_attempt:
            return None
        return max(exams_to_attempt, key=exams_to_attempt.get)

    @AgentCallObserver.observe(topic=ResultTopics.RESOURCE_USAGE)
    def study_resource(self, resource, until=INFINITY):
        """
        :type resource: agents.Resource
        :return bool: returns False if there was not enough time to study resource completely
        """
        self._logger.debug("{self}: Studying resource, until {until}".format(self=self, until=until))
        # TODO: behavior?
        study_result = True
        lectures_to_study = [lecture for lecture in resource.lectures if lecture.facts - self.knowledge]
        for lecture in lectures_to_study:
            self._logger.debug("{student}: Studying {lecture}, until {until}".format(
                student=self, lecture=lecture, until=until)
            )
            study_result = yield from lecture.take(self, until)
            self._logger.debug("{student}: Studying {lecture} done at {time}".format(
                student=self, lecture=lecture, time=self.env.now
            ))
            if not study_result:
                break

        return study_result

    def study_fact(self, fact, until=INFINITY):
        if fact in self._knowledge:
            self._logger.debug("{student}: {fact} already known - skipping".format(student=self, fact=fact))

        self._logger.debug("{student}: studies {fact}".format(student=self, fact=fact))
        time_to_study = fact.complexity / self.skill
        if self.env.now + time_to_study > until:
            self._logger.debug("{self}: not enough time to study fact - skipping".format(self=self))
            return False
        yield self.env.timeout(time_to_study)
        self._add_fact(fact)
        return True

    def check_fact(self, fact, until=INFINITY):
        # TODO: probabilistic check, revisiting lectures if missed, behavior
        time_to_check = fact.complexity / self.check_fact_skill
        enough_time = self.env.now + time_to_check <= until
        timeout = min(time_to_check, until - self.env.now)
        yield self.env.timeout(timeout)
        return enough_time and fact in self._knowledge

    def process_messages(self, until=INFINITY):
        success = True
        self._logger.debug("{student} starts reading messages (count:{count})".format(
            student=self, count=len(self._inbox)
        ))
        while success and self._inbox:
            message = self._inbox.pop()
            self._logger.debug("{student} reads message {message} from inbox".format(student=self, message=message))
            success = yield from message.process(self, until)

    def send_messages(self, until=INFINITY):
        for to_student, messages in self.behavior.send_messages.get_messages(self):
            address = to_student.inbox_address
            for message in messages:
                time_to_send = message.time_to_send(self)
                if self.env.now + time_to_send > until:
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

    def _next_activity_generator(self):
        for activity_type in cycle([
            StudySessionActivity, PeerStudentInteractionActivity, PassExamActivity, IdleActivity
        ]):
            if self.behavior.stop_participation.stop_participation(
                    self, self.curriculum, self.get_accessible_resources()
            ):
                self.stop_participation()
                return
            if activity_type.can_skip_if_not_required_by_goal and not self._activity_required(activity_type):
                continue
            activity_length = self._activity_lengths.get(activity_type)(self, self.env.now)
            yield activity_type(self, activity_length, self.env)

    def _activity_required(self, activity):
        return not self.goals or any(map(lambda goal: goal.requires_activity(self, activity), self.goals))

    def _passed_exam(self, exam):
        # TODO allow attempting passed exam again if there's room for improvement
        return any(feedback.passed for feedback in self._exam_results.get(exam.code, []))
