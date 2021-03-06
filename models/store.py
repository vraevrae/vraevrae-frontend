from models.answer import Answer
from models.question import Question
from models.quiz import Quiz
from models.user import User
from models.useranswer import UserAnswer


class Store:
    """Class in charge with the storing and retrieval of data"""

    def __init__(self):
        """create the store itself, on which the functions operate"""
        self.quizes = {}
        self.questions = {}
        self.answers = {}
        self.users = {}
        self.user_answers = {}

    def create_quiz(self, source, difficulty=None, category=None, max_questions=None):
        """creates a new quiz and adds it to the store"""
        # Get the lowest available code
        code = 1
        if len(self.questions) is not 0:
            code = max([quiz.code for quiz in self.quizes.values()]) + 1

        new_quiz = Quiz(source, code, difficulty, category, max_questions)
        self.quizes[new_quiz.quiz_id] = new_quiz
        return new_quiz.quiz_id

    def create_answer(self, question_id, text, is_correct):
        """create a new answer and add it to the store and to the quiz"""
        new_answers = Answer(question_id, text, is_correct)
        self.get_question_by_id(question_id).add_answer_by_id(
            new_answers.answer_id)
        self.answers[new_answers.answer_id] = new_answers
        return new_answers.answer_id

    def create_user(self, quiz_id, name, is_owner):
        """adds a user to the app"""
        new_user = User(quiz_id=quiz_id, name=name, is_owner=is_owner)
        self.users[new_user.user_id] = new_user
        self.get_quiz_by_id(quiz_id).add_user_by_id(new_user.user_id)
        return new_user.user_id

    def create_question(self, quiz_id, temp_question):
        """create a new question and add it to the store and to the quiz"""
        new_question = Question(**temp_question)
        self.get_quiz_by_id(quiz_id).add_question_by_id(
            new_question.question_id)
        self.questions[new_question.question_id] = new_question
        return new_question.question_id

    def create_question_from_source(self, quiz_id):
        """Creates a question with answers from a given source"""
        # get question from quiz source
        quiz = self.get_quiz_by_id(quiz_id)
        temp_question = quiz.source.get_question()

        # add the question to the store
        question_id = self.create_question(quiz_id, temp_question)

        # add the answers to the question and the store
        for answer in temp_question["answers"]:
            self.create_answer(
                question_id, answer["text"], answer["is_correct"])

        return question_id

    def set_user_answer(self, user_answer):
        """set a user_answer to the store"""
        self.user_answers[user_answer.user_answer_id] = user_answer
        return user_answer.user_answer_id

    def get_quiz_by_id(self, quiz_id):
        """read a specific quiz from the store by quizId"""
        return self.quizes[quiz_id]

    def get_quiz_by_code(self, code):
        """read a specific quiz from the store by quizId"""
        data = [quiz for quiz in self.quizes.values() if quiz.code is int(code)]
        return data[0] if len(data) != 0 else None

    def get_quiz_by_user_id(self, user_id):
        """reads a specific quiz from the store by quizId"""
        user = self.get_user_by_id(user_id)
        return self.get_quiz_by_id(user.quiz)

    def get_question_by_id(self, question_id):
        """reads a specific question from the store by questionId"""
        return self.questions[question_id]

    def get_questions_by_id(self, question_ids):
        """reads a list of question from the store by questionIds"""
        return [self.get_question_by_id(question_id) for question_id in question_ids]

    def get_answer_by_id(self, answer_id):
        """reads a specific answer from the store by answerIds"""
        return self.answers[answer_id]

    def get_answers_by_id(self, answer_ids):
        """reads a list of answers from the store by answerIds"""
        return [self.get_answer_by_id(answer_id) for answer_id in answer_ids]

    def get_user_answers_by_user_and_question_id(self, user_id, question_id):
        """reads a specific user_answer from the store by user_answerIds"""
        return [user_answer for user_answer in self.user_answers.values() if user_answer.user_id == user_id and user_answer.question_id == question_id]

    def get_user_by_id(self, user_id):
        """reads a specific user from the store by userId"""
        return self.users[user_id]

    def get_users_by_id(self, user_ids):
        """reads a list of users from the store by userId"""
        return [self.get_user_by_id(user_id) for user_id in user_ids]


# Instantiate the store in the module (to make it sharable)
store = Store()
