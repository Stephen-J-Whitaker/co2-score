"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

import time
import gspread
from google.oauth2.service_account import Credentials
import gui
import questionnaire
from colorama import Fore, Back, Style
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


def validate_option_input(input, range):
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
        print(gui.terminal_command["clear_screen"])
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
        gui.terminal_control("clear_screen")
        valid_input = False
        while valid_input is False:
            print(question.question_info)
            ind = 1
            for option in question.options:
                print(f"{ind}. " + option["option_detail"])
                ind += 1
            num = len(question.options)
            response = input(f"Please select an option [1 - {num}]: ")
            valid_input = validate_option_input(response, num)
        responses.append(int(question.options[int(response) - 1]["score"]))
    return responses


def results(responses, questionnaire_details):
    """
    Calculate co2 score and inform user
    """
    result = sum(responses)
    gui.terminal_control("clear_screen")
    print(f"Your carbon footprint score is {result}")
    print(questionnaire_details["summary"] + "\n\n")
    input("Press Enter to continue.....")
    return result


def create_user_id():
    """
    Generate and return a random 5 character alphanumeric user id
    """
    num_char_pool = list(string.ascii_letters)


def validate_yes_no(user_input):
    """
    Check if the users response was y or n (or Y and N)
    and raise ValueError if not
    """
    try:
        if user_input != "y" or user_input != "n":
            raise ValueError(
                'Please enter either "y" for yes or "n" for no'
            )
    except ValueError as error:
        print(gui.terminal_command["clear_screen"])
        print(f"Data invalid: {error}")
        print("Please try again")
        time.sleep(3)
        return False

    return True    


def store_data(total_score):
    """
    Ask the user if they would like to store their results
    and take appropraite action to their response
    """
    valid_input = False
    while valid_input is False:
        print("Would you like your results to be stored?")
        user_input = input('Please enter "y" for Yes and "n" for No: ').lower
        valid_input = validate_yes_no(user_input)
    if user_input == "n":
        # Call main menu : to be implemented
        pass
    else:
        create_user_id()


def store_results(user_results):
    """
    Put user data in external spreadsheet
    """
    user_sheet = CO2_SHEET.worksheet("co2_scores")
    user_sheet.append_row(user_results)


def main():
    """
    Run all program functions
    """
    gui.set_gui_background("assets/images/gui_world.bmp")
    # time.sleep(3)
    gui.set_gui_background("assets/images/gui_back_blue_1.bmp")
    gui.app_title()
    # time.sleep(3)
    questionnaire_details = questionnaire.get_questionnaire(CO2_SHEET)
    responses = question_user(questionnaire_details)
    total_score = results(responses, questionnaire_details)
    store_data(total_score)
    # pprint(questionnaire_details)
    # print(questionnaire_details["questions"][0].question_info)
    # print(questionnaire_details["summary"])


main()
