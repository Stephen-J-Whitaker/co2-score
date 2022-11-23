"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

import gspread
from google.oauth2.service_account import Credentials
import questionnaire
from pprint import pprint

# SCOPE definition code provided by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Code to access Google Sheets provided by code institute
# Code Institute code begins here
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
CO2_SHEET = GSPREAD_CLIENT.open('co2_score')
# Code Institute code ends here


def question_user(questionnaire_details):
    """
    Recall each question from the questionnaire sequentially,
     display the question to the user and record their
     responses into a variable
    """
    for question in questionnaire_details["questions"]:
        print(question.question_info)

def main():
    """
    Run all program functions
    """
    questionnaire_details = questionnaire.get_questionnaire(CO2_SHEET)
    question_user(questionnaire_details)
    # pprint(questionnaire_details)
    # print(questionnaire_details["questions"][0].question_info)
    # print(questionnaire_details["summary"])


main()
