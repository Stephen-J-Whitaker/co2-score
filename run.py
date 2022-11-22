"""
Main co2 score code that asks a user questions in order to estimate their
carbon footprint
"""

import gspread
from google.oauth2.service_account import Credentials
import questionnaire

# SCOPE definition code provided by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Code to access Google Sheets provided by code institute
# Begins here
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
CO2_SHEET = GSPREAD_CLIENT.open('co2_score')
# Ends here


def main():
    """
    Run all program functions
    """
    question = questionnaire.Question(1, 2, 3)
    print(question.max_poss_score)


main()
