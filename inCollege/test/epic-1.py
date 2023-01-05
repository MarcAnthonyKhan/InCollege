import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import unique, clearUsers, checkExistingAccts
from inCollege.states import newAcct
from inCollege.testFunc import *
from inCollege.commons import passwordValidator

database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()

# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #1 Test Cases
      




# ==================================================================================
# ==================================================================================

def initTestAccounts():
	accounts = [
    ('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs', 'plus'),
    ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce', 'standard'),
    ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs', 'plus'),
    ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE', 'standard'),
    ('test5', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs', 'plus'),
	]
	for account in accounts:
		inputs = iter(account)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			newAcct()

'''
  Story: Account Creation
  - Username is unique
  - Password is: minimum of 8 characters, maximum of 12 characters, at least one capital letter, one digit, and one special character
  - User accounts saved to a database
'''
@pytest.mark.accountCreation
@pytest.mark.parametrize('username, result',
                        [
                          ('test1', False), # exist
                          ('test2', False), # exist
                          ('test3', False), # exist
                          ('test', True) # not exist
                        ]
)
def test_usernameUnique(username, result):
  clearUsers()
  initTestAccounts()
  output = unique(username)
  assert output == result


@pytest.mark.accountCreation
@pytest.mark.parametrize('password, result',
                        [
                          ('abcdefgA!1', True),
                          ('abcdefg', False), # min 8 chars
                          ('abcdefghijklmno', False), # max 12 chars
                          ('abcdefgA!', False), # at least one digit
                          ('abcdefg!1', False), # at least one capital letter
                          ('abcdefgA1', False) # at least one special character
                        ]
                        )
def test_passwordValidation(password, result):
  assert passwordValidator(password) == result


@pytest.mark.accountCreation
@pytest.mark.parametrize('username, password, result',
                        [
                          ('test1', 'aaaaaaa!A1', -1), # user exists
                          ('test2', 'aaaaaaa!A1', -1), # user exists
                          ('test3', 'aaaaaaa!A1', -1), # user exists
                          ('test', 'aaaaaaa!A1', -1) # No such user
                        ]
)
def test_checkUsernameSaved(username, password, result):
  if username == 'test':
    assert checkExistingAccts(username, password) == result
  else:
    assert checkExistingAccts(username, password) != result


'''
  Story: Account Number Limit
  - Only 5 accounts can be created
  (we can put whatever value as a parameter since it is replaced by the actual number of user in DB)
'''
@pytest.mark.accountNumber
def test_accountCount():
  assert accountCount(0) == True # counting the number of users in actual DB 

'''
  Story: Login Status
  - If login credentials recognized in database, the following message is displayed: "You have successfully logged in"
  - If the login credentials were not recognized in the database, the following message is displayed: "Incorrect username / password, please try again"
'''
@pytest.mark.loginStatus
@pytest.mark.parametrize('username, password, result',
                        [
                          ('test1', 'aaaaaaa!A1', True), # logged in
                          ('test2', 'aaaaaaa!A1', True), # logged in
                          ('test3', 'aaaaaaa!A1', True), # logged in
                          ('test', 'aaaaaaa!A1', False) # not logged in
                        ]
                        )
def test_loginStatus(username, password, result):
  assert loginStatus(username, password) == result

'''
  Story: User Additional Options
  - After logging in, the user will presented with a menu allowing them to select one of the following options:
    1. Search for a job
    2. Find someone they know
    3. Learn a skill
'''
@pytest.mark.userOptions
@pytest.mark.parametrize('username, password, result',
                        [
                          ('test1', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test2', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test3', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test', 'aaaaaaa!A1', False) # not logged in
                        ]     
                        )
def test_stateMainInterface(username, password, result):
  assert stateMainInterface(username, password) == result


@pytest.mark.userOptions
@pytest.mark.parametrize('sel, result',
                        [
                          ('1', True), # user option exists
                          ('2', True), # user option exists
                          ('3', True), # user option exists
                          ('4', False) # user option doesn't exist
                        ]     
                        )
def test_listOptions(sel, result):
  assert listOptions(sel) == result


'''
  Story: Skills Options
  - Sub-menu lists 5 skills that the user can select
  - There will be a 6th option to return to the previous menu
'''
@pytest.mark.skillsOptions
@pytest.mark.parametrize('sel, result',
                         [
                           ('1', True), # skill exists
                           ('2', True), # skill exists
                           ('3', True), # skill exists
                           ('4', True), # skill exists
                           ('5', True), # skill exists
                           ('6', True), # back to previous page exists
                           ('7', False) # No option exists
                         ]
)
def test_skillsOptions(sel, result):
   assert listSkillsOptions(sel) == result


'''
  Story: Under Construction
  - Users will receive an “Under Construction” message if they select the following options:
    1. Search for a job
    2. Find someone you know
    3. Any of the 5 skills listed
'''
@pytest.mark.underConstruction
@pytest.mark.parametrize('sel, result',
                        [
                          ('1', True), 
                          ('2', True), 
                          ('3', False),
                          ('4', True),
                          ('6', True), 
                          ('8', True),
                          ('10', True), 
                        ]
                        )
def test_underConstruction(sel, result):
  assert stateUnderConstruction(sel) == result


