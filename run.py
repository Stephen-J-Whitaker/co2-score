"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

import time
import string
import random
from datetime import datetime
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

questionnaire_details = questionnaire.get_questionnaire(CO2_SHEET)


class User():
    """
    Create a user instance
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_results = {
            "date": None,
            "results": None,
            "final_score": None
        }


class PreviousUser(User):
    """
    Creates a user instance with addition of previous results
    """
    def __init__(self, user_id, previous_results):
        super().__init__(user_id)
        self.previous_results = previous_results


def validate_option_input(user_input, user_range):
    """
    Confirm that the user input is in range and
    is numeric.
    """
    try:
        int(user_input)
        if int(user_input) < 1 or int(user_input) > user_range:
            raise ValueError(
                "The value entered was out of range"
            )
    except ValueError as error:
        gui.terminal_control("clear_screen")
        print(f"Data invalid: {error}")
        print(f"Please select an option from 1 - {user_range}")
        print("Please try again")
        input("Press Enter to continue.....")
        return False

    return True


def main_menu(current_user):
    """
    Display the main menu to the user and action there
    option choice
    """
    gui.terminal_control("clear_screen")
    print("1. Start the questionnaire\n")
    print("2. View instructions\n")
    print("3. Exit software\n")
    valid_input = False
    while valid_input is False:
        response = input("Please select an option [1 - 3]: ")
        valid_input = valid_input = validate_option_input(response, 3)
    if response == "1":
        if current_user is None:
            initialise_user()


def initialise_user():
    """
    Create user instance and call questionnaire
    """
    current_user = User(None)
    current_user.session_results["date"] = datetime.now().date()
    print("date " + current_user.session_results["date"])
    question_user(current_user)


def store_results(user_results):
    """
    Put user data in external spreadsheet
    """
    user_sheet = CO2_SHEET.worksheet("co2_scores")
    user_sheet.append_row(user_results)


def results(current_user):
    """
    Calculate co2 score and inform user
    """
    user_results = current_user.session_results["results"]
    current_user.session_results["final_score"] = sum(user_results)
    gui.terminal_control("clear_screen")
    print(f"Your carbon footprint score is {user_results}")
    print(questionnaire_details["summary"] + "\n\n")
    input("Press Enter to continue.....")
    store_data(current_user)


def question_user(current_user):
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
    current_user.session_results["results"] = responses
    results(current_user)


def create_user_id():
    """
    Generate and return a random 5 character alphanumeric user id
    """
    num_char_pool = list(string.ascii_letters)
    num_pool = range(10)
    num_char_pool += [str(num) for num in num_pool]
    print(num_char_pool)
    user_id_list = []
    for x in range(5):
        user_id_list.append(random.choice(num_char_pool))
    user_id = "".join(user_id_list)
    return user_id


def validate_yes_no(user_input, valid_range):
    """
    Check if the users response was y or n (or Y and N)
    and raise ValueError if not
    """
    try:
        if user_input not in valid_range:
            raise ValueError(
                'Please enter either "y" for yes or "n" for no'
            )
    except ValueError as error:
        gui.terminal_control("clear_screen")
        print(f"Data invalid: {error}")
        print("Please try again")
        input("Press Enter to continue.....")
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
        user_input = input('Please enter "y" for Yes and "n" for No: ')
        user_input.lower()
        valid_input = validate_yes_no(user_input, ["y", "n"])
    if user_input == "n":
        # Call main menu : to be implemented
        pass
    else:
        user_id = create_user_id()
    


def main():
    """
    Run all program functions
    """
    gui.set_gui_background("assets/images/gui_world.bmp")
    # time.sleep(3)
    gui.set_gui_background("assets/images/gui_back_blue_1.bmp")
    gui.app_title()
    # time.sleep(3)
    main_menu(None)
    # pprint(questionnaire_details)
    # print(questionnaire_details["questions"][0].question_info)
    # print(questionnaire_details["summary"])


main()
