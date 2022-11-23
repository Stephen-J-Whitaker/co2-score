"""
Module to import questionnaire from external spreasheet
"""

from pprint import pprint


class Question:
    """Creates a question instance"""
    def __init__(self, question_info, max_poss_score, options):
        self.question_info = question_info
        self.max_poss_score = max_poss_score
        self.options = options


def string_wrap(string):
    """
    Take strings and add a newline escape sequence
    after every 55th character where necessary to wrap
    the strings within a terminal 
    """
    new_string = ""
    if len(string) > 55:
        for char in len(string):
            new_string += string[char]
            if char == 55:
                new_string += "\n"
    return string


def get_questionnaire(co2_sheet):
    """
    Import the questionnaire from the external spreadsheet
    """
    first_step = True
    questionnaire_raw = co2_sheet.worksheet("questionnaire").get_all_values()
    question_info = ""
    max_poss_score = None
    # Options held in a list so order retained
    options = []
    # Questions held in a list so order retained
    questions = []
    questionnaire = {}
    for row in questionnaire_raw:
        if "Step" in row[0]:
            if first_step is True:
                first_step = False
            else:
                question_instance = Question(question_info, max_poss_score,
                                             options)
                questions.append(question_instance)
            options = []
            question_info = string_wrap(row[1])
            max_poss_score = row[2]
        elif "Option" in row[0]:
            option = {}
            option["option_detail"] = row[1]
            option["score"] = row[2]
            options += option
        elif "Summary" in row[0]:
            questionnaire["summary"] = row[1]
            question_instance = Question(question_info, max_poss_score,
                                         options)
            print(question_instance.question_info)
            questionnaire["questions"] = questions
    return questionnaire
