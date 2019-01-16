from uuid import uuid4


class User():
    """quiz users"""

    def __init__(self, **kwargs):
        self.userId = str(uuid4())
        self.quizId = kwargs["quizId"]
        self.sessionId = kwargs["sessionId"]
        self.name = kwargs["name"]
        self.score = 0
        self.isOwner = kwargs["isOwner"]

    def addScore(self):
        """adds the score to the users score"""
        pass