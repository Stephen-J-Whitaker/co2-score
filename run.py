"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

import time
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


def validate_input(input, range):
    """
    Confirm that the user input is in range and
    is numeric.
    """
    try:
        int(input)
        if int(input) < 1 or int(input) > range:
            raise ValueError(
                "The value entered was out of range"
            )
    except ValueError as error:
        # Clear the screen
        print("\033[2J")
        print(f"Data invalid: {error}")
        print(f"Please select an option from 1 - {range}")
        print("Please try again")
        time.sleep(3)
        return False

    return True


def question_user(questionnaire_details):
    """
    Recall each question from the questionnaire sequentially,
     display the question to the user and record their
     responses into a variable
    """
    responses = []
    for question in questionnaire_details["questions"]:
        # Clear the screen
        print("\033[2J")
        valid_input = False
        while valid_input is False:
            print(question.question_info)
            ind = 1
            for option in question.options:
                print(f"{ind}. " + option["option_detail"])
                ind += 1
            num = len(question.options)
            response = input(f"Please select an option [1 - {num}]")
            valid_input = validate_input(response, num)
        responses.append(int(question.options[int(response) - 1]["score"]))
    return responses


def results(responses, questionnaire_details):
    """
    Calculate co2 score and inform user
    """
    result = sum(responses)
    # Clear the screen
    print("\033[2J")
    print(f"Your carbon footprint score is {result}")
    print(questionnaire_details["summary"])
    return result


def store_results(user_results):
    """
    Put user data in external spreadsheet
    """
    user_sheet = CO2_SHEET.worksheet("co2_scores")
    user_sheet.append_row(results)


def main():
    """
    Run all program functions
    """
    questionnaire_details = questionnaire.get_questionnaire(CO2_SHEET)
    responses = question_user(questionnaire_details)
    total_score = results(responses, questionnaire_details)
    print(responses)
    store_results(responses)
    # pprint(questionnaire_details)
    # print(questionnaire_details["questions"][0].question_info)
    # print(questionnaire_details["summary"])
    print(responses)


main()
