"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

# Imported library dependencies from third party sources
import time
import sys
import string
import random
import copy
import math
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style

# Custom imports developed for the application
import gui
import questionnaire

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
        self.previous_user = False
        self.session_results = {
            "date": None,
            "results": None,
            "final_score": None
        }

    def date(self):
        """
        Method to add current date to class instance
        """
        date = datetime.now().date().strftime("%d-%m-%Y")
        self.session_results["date"] = date


class PreviousUser(User):
    """
    Creates a user instance with addition of previous results
    """
    def __init__(self, user_id):
        super().__init__(user_id)
        self.previous_user = True
        self.previous_results = {
            "date": None,
            "results": None,
            "final_score": None
        }


def main_menu(current_user):
    """
    Display the main menu to the user and action there
    option choice
    """
    valid_input = False
    while valid_input is False:
        gui.terminal_control("clear_screen")
        if current_user is not None and current_user.user_id is not None:
            print(f"\033[1CUser logged in: {current_user.user_id}\n")
        print("                                    CO2 SCORE")
        print("                            Calculate your co2 score\n")
        # Moves cursor 1 place to right with \033[1C
        print("\n\033[1CMain menu\n")
        print("\033[1C1. View instructions\n")
        print("\033[1C2. Start the questionnaire\n")
        print("\033[1C3. Administer data\n")
        print("\033[1C4. Exit software\n")
        if current_user is not None and current_user.user_id is not None:
            print("\033[1C5. Log out\n")
            menu_range = 5
        else:
            menu_range = 4
        response = input(f"\033[1CPlease select an option [1-{menu_range}]: ")
        valid_input = validate_option_input(response, menu_range)
    if response == "1":
        instructions(current_user)
    elif response == "2":
        if current_user is None:
            current_user = load_user(current_user, "questions")
        question_user(current_user)
    elif response == "3":
        administer_data(current_user)
    elif response == "4":
        print(Style.RESET_ALL)
        gui.set_gui_background("assets/images/gui_world.bmp")
        print("\033[23;37H\033[44;37mEXITING")
        time.sleep(2)
        print(Style.RESET_ALL)
        gui.terminal_control("clear_screen")
        gui.terminal_control("cursor_home")
        sys.exit()
    elif response == "5":
        log_out(current_user)


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
        print(f"\033[1CData invalid: {error}")
        print(f"\033[1CPlease select an option from 1 - {user_range}")
        input("\033[23;2HPress Enter to try again")
        return False

    return True


def instructions(current_user):
    """
    Display instructions and then go to questionnaire
    or back to main menu
    """
    valid_response = False
    while valid_response is False:
        gui.terminal_control("clear_screen")
        print("\033[1CInstructions\n")
        print(f'\033[1C{questionnaire_details["Instructions"]}')
        print("\n")
        print("\033[1C1. Continue to questionnaire")
        print("\033[1C2. Return to main menu")
        user_choice = input("\033[1CPlease enter an option [1 or 2]: ")
        valid_response = validate_option_input(user_choice, 2)
    if user_choice == "1":
        if current_user is None:
            current_user = load_user(current_user, "questions")
        question_user(current_user)
    elif user_choice == "2":
        return main_menu(current_user)


def administer_data(current_user):
    """
    Enable users with a user id to administer their data
    """
    if current_user is None:
        current_user = load_user(current_user, "main_menu")
    valid_response = False
    while valid_response is False:
        gui.terminal_control("clear_screen")
        print(f"\033[1CUser logged in: {current_user.user_id}\n")
        print("\033[1C1. Review previous score")
        print("\033[1C2. Delete data")
        print("\033[1C3. Return to main menu")
        response = input("\033[1CPlease select an option [1-3]: ")
        valid_response = validate_option_input(response, 3)
    if response == "1":
        previous_score = current_user.previous_results["final_score"]
        gui.terminal_control("clear_screen")
        bar_chart(current_user, int(previous_score), int(180), "previous")
        print("\033[14;2H" + questionnaire_details["summary"] + "\n")
        input("\033[1CPress enter to continue.....")
        administer_data(current_user)
    elif response == "2":
        co2_scores_sheet = CO2_SHEET.worksheet("co2_scores")
        cell = co2_scores_sheet.find(current_user.user_id)
        co2_scores_sheet.delete_rows(cell.row)
        gui.terminal_control("clear_screen")
        print("\033[1CYour data has been deleted")
        input("\033[23;2HPress enter to continue....")
        log_out(current_user)
    elif response == "3":
        main_menu(current_user)


def log_out(current_user):
    """
    Delete the current user variable and its data
    then return to the main menu
    """
    del current_user
    gui.terminal_control("clear_screen")
    print("\033[2;2HYou have been logged out")
    input("\033[23;2HPress enter to continue.....")
    main_menu(None)


def initialise_user():
    """
    Create user instance and call questionnaire
    """
    current_user = User(None)
    current_user.date()
    return current_user


def validate_user_id_entry(user_id, current_user, cell, option):
    """
    Validate user id entry
    """
    try:
        if user_id.isalnum() is False:
            raise ValueError("\033[1CThe entered "
                             "value must be 5 alphanumeric characters\n"
                             "\033[1CYou entered non valid characters.")
        elif len(user_id) != 5:
            raise ValueError("\033[1CThe entered "
                             "value must be 5 alphanumeric characters\n"
                             f"\033[1CYou entered {len(user_id)} characters.")
        elif cell is None:
            raise ValueError("\033[1CThe user id cannot be found.")
    except ValueError as error:
        gui.terminal_control("clear_screen")
        print(f"\033[1CUser data invalid: {error}")
        if option == "main_menu":
            user_input = input('\033[23;2HPress Enter to continue.....')
            main_menu(current_user)
        elif option == "questions":
            user_input = input('\033[23;2HPress Enter to try again '
                               'or "q" to start the quesionnaire: ')
            if user_input.lower() == "q":
                question_user(current_user)
        return False

    return True


def load_user(current_user, option):
    """
    Request entry of user id
    """
    if current_user is None:
        valid_user_id = False
        while valid_user_id is False:
            gui.terminal_control("clear_screen")
            print("\033[1CIf you have a user id to retrieve previous data,")
            user_id = input("\033[1Center it now or press enter to continue: ")
            if user_id == "":
                if option == "questions":
                    valid_user_id = True
                    current_user = initialise_user()
                    return current_user
                elif option == "main_menu":
                    return main_menu(current_user)
            else:
                co2_scores_sheet = CO2_SHEET.worksheet("co2_scores")
                cell = co2_scores_sheet.find(user_id)
                valid_user_id = validate_user_id_entry(user_id,
                                                       current_user,
                                                       cell, option)
        previous_results_row = co2_scores_sheet.row_values(cell.row)
        print(f"valid_user_id = {user_id}")
        current_user = PreviousUser(user_id)
        current_user.previous_results["date"] = previous_results_row[1]
        previous_results = []
        for result in range(2, 14):
            print(previous_results_row[result])
            previous_results.append(int(previous_results_row[result]))
        current_user.previous_results["results"] = previous_results
        final_score = previous_results_row[14]
        current_user.previous_results["final_score"] = final_score
        current_user.date()
    return current_user


def store_results(current_user):
    """
    Put user data in external spreadsheet
    """
    sheet_data = []
    sheet_data.append(current_user.user_id)
    date = datetime.now().date().strftime("%d-%m-%Y")
    sheet_data.append(date)
    for data in current_user.session_results["results"]:
        sheet_data.append(data)
    sheet_data.append(str(current_user.session_results["final_score"]))
    user_sheet = CO2_SHEET.worksheet("co2_scores")
    if current_user.previous_user is False:
        user_sheet.append_row(sheet_data)
    elif current_user.previous_user is True:
        cell = user_sheet.find(current_user.user_id)
        sheet_range = "A" + str(cell.row) + ":O" + str(cell.row)
        update_data = []
        update_data.append(sheet_data)
        user_sheet.update(sheet_range, update_data)
    # Make previous results current results only if user wasn't a previous user
    # before this session
    previous_results = copy.deepcopy(current_user.session_results)
    current_user.previous_results = previous_results
    # Make previous user True in case saved for first time
    current_user.previous_user = True
    main_menu(current_user)


def results(current_user, max_total):
    """
    Calculate co2 score and inform user
    """
    user_results = sum(current_user.session_results["results"])
    current_user.session_results["final_score"] = user_results
    gui.terminal_control("clear_screen")
    print(f"\033[1CYour total carbon footprint score is {user_results}")
    print("\033[14;2H" + questionnaire_details["summary"] + "\n\n")
    bar_chart(current_user, user_results, max_total, "current")
    if current_user.previous_user is True:
        previous_score = int(current_user.previous_results["final_score"])
        bar_chart(current_user, previous_score, max_total, "previous")
        input("\033[23;2HPress enter to continue.....")
    store_data(current_user)


def question_user(current_user):
    """
    Recall each question from the questionnaire sequentially,
    display the question to the user and record their
    responses into a variable
    """
    responses = []
    max_total = 0
    index = 0
    num_of_questions = len(questionnaire_details["questions"])
    question_num = 1
    for question in questionnaire_details["questions"]:
        valid_input = False
        while valid_input is False:
            gui.terminal_control("clear_screen")
            print(f"\033[1CQuestion {question_num} of {num_of_questions}\n")
            print(f"\033[1C{question.question_info}\n")
            ind = 1
            option_list = []
            for option in question.options:
                option_list.append(option["option_detail"])
                print(f"\033[1C{ind}. " + option["option_detail"])
                ind += 1
            num = len(question.options)
            response = input(f"\n\033[1CPlease select an option [1-{num}]: ")
            valid_input = validate_option_input(response, num)
        question_num += 1
        option_chosen = option_list[int(response) - 1]
        score = int(question.options[int(response) - 1]["score"])
        max_poss_score = question.max_poss_score
        max_poss_score = max_poss_score.replace("Max possible score ", "")
        max_total += int(max_poss_score)
        responses.append(score)
        gui.terminal_control("clear_screen")
        print(f"\033[2;2HYou chose option:\n\033[1C'{option_chosen}'")
        print(f"\033[1C{score} points have been added to your carbon score")
        bar_chart(current_user, score, max_poss_score, "current")
        if current_user.previous_user is True:
            score = current_user.previous_results["results"][index]
            bar_chart(current_user, score, max_poss_score, "previous")
            input("\033[23;2HPress enter to continue.....")
        index += 1
    current_user.session_results["results"] = responses
    results(current_user, max_total)


def bar_chart(current_user, score, max_score, session):
    """
    Show the users response as a proportion of highest possible
    score in the form of a bar chart and show comparison to any
    present previous results
    """
    # Scale down max_total and score to fit on bar chart when necessary
    max_score_scaled = max_score / 4 if int(max_score) > 55 else max_score
    user_results_scaled = score / 4 if int(max_score) > 55 else score
    if session == "current":
        bar_chart_string = "\033[7;13H"
        print(f"\033[6;2HYour score is {score}")
    elif session == "previous":
        previous_date = current_user.previous_results["date"]
        print(f"\033[9;2HYour previous score on {previous_date} was {score}")
        bar_chart_string = "\033[10;13H"
    proportion = math.ceil((55 / int(max_score_scaled)) * user_results_scaled)
    for i in range(55):
        if i < proportion:
            # 60 is the recommended carbon score max
            if int(score) > 60:
                bar_chart_string += "\033[41;31m\u2588"
            else:
                bar_chart_string += "\033[42;32m\u2588"
        elif i == proportion:
            bar_chart_string += "\033[42;30m\u2588"
        else:
            bar_chart_string += "\033[47;30m\u2591"
    if session == "current":
        print("\033[7;4HMin 0" + bar_chart_string)
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT)
        print(f"\033[7;70HMax {max_score}")
    elif session == "previous":
        print("\033[10;4HMin 0" + bar_chart_string)
        print(Back.BLUE + Fore.WHITE + Style.BRIGHT)
        print(f"\033[10;70HMax {max_score}")
    if current_user.previous_user is False:
        input("\033[23;2HPress enter to continue.....")
        gui.terminal_control("clear_screen")


def create_user_id():
    """
    Generate and return a random 5 character alphanumeric user id
    """
    num_char_pool = list(string.ascii_letters)
    num_pool = range(10)
    num_char_pool += [str(num) for num in num_pool]
    new_user_id = False
    while new_user_id is False:
        user_id_list = []
        index = 5
        while index > 0:
            index -= 1
            user_id_list.append(random.choice(num_char_pool))
        user_id = "".join(user_id_list)
        co2_scores_sheet = CO2_SHEET.worksheet("co2_scores")
        cell = co2_scores_sheet.find(user_id)
        if cell is None:
            new_user_id = True
    gui.terminal_control("clear_screen")
    print("\033[1CIf you use this tool again the user id can be used to load")
    print("\033[1Cthis sessions data for comparison. Keep it safe it cannot")
    print("\033[1Cbe retrieved if lost\n")
    print(f"\033[1CYour user id is: {user_id}\n")
    input("\033[23;2HPress Enter to continue when ready .....")
    return user_id


def validate_range(user_input, valid_range):
    """
    Check if the users response was in letter range
    and raise ValueError if not
    """
    try:
        if user_input not in valid_range:
            raise ValueError(
                '\033[1CPlease enter either '
                f'"{valid_range[0]}" or "{valid_range[1]}"'
            )
    except ValueError as error:
        gui.terminal_control("clear_screen")
        print(f"\033[1CData invalid: {error}")
        input("\033[23;2HPress Enter to try again")
        gui.terminal_control("clear_screen")
        return False

    return True


def store_data(current_user):
    """
    Ask the user if they would like to store their results
    and take appropraite action to their response
    """
    if current_user.previous_user is False:
        valid_input = False
        while valid_input is False:
            print("\033[1CWould you like your results to be stored?")
            user_input = input('\033[1CPlease enter "y" or "n": ')
            user_input.lower()
            valid_input = validate_range(user_input, ["y", "n"])
        if user_input == "n":
            del current_user
            main_menu(None)
        else:
            user_id = create_user_id()
            current_user.user_id = user_id
            store_results(current_user)
    else:
        store_results(current_user)


def main():
    """
    Run all program functions
    """
    gui.set_gui_background("assets/images/gui_world.bmp")
    time.sleep(3)
    gui.set_gui_background("assets/images/gui_back_blue_1.bmp")
    gui.app_title()
    time.sleep(3)
    main_menu(None)


main()
