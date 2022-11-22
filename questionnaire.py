"""
Module to import questionnaire from external spreasheet
"""


class Question:
    """Creates a question instance"""
    def __init__(self, question_info, max_poss_score, options):
        self.question_info = question_info
        self.max_poss_score = max_poss_score
        self.options = options
