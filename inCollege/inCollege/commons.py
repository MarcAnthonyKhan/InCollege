import os
from functools import lru_cache


MAX_USERS = 10
MAX_JOBS = 10
DEFAULT_GUEST_CONTROLS = (1, 1, 1)
DEFAULT_LANGUAGE_SETTINGS = ('english',)



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



clear = lambda: os.system('cls') # A function f() that clears all text from the terminal
isEqual = lambda x, y: (x == y)
isZero = lambda x : (isEqual(x,0)) # A function f(x) = x == 0
isYes = lambda x: (1 if x.lower() == "yes" else 0)
byKey = lambda x, y: (x[y]) # A function f(x) = x[y]



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def enterToContinue():
  input("\nPress ENTER to continue.\n")
  clear()


def enterToGoBack():
  input("\nPress ENTER to go back.\n")
  clear()


def numberValidator(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def passwordValidator(password):
  c, d, s = 0, 0, 0
  length = len(password)
  if length > 7 and length < 13:
    for i in password:
      if i.isupper():
        c += 1
      if i.isdigit():
        d += 1
      if i=='!' or i=='@' or i=='#' or i=='$' or i=='%' or i=='^' or i=='&' or i=='*':
        s += 1

  if c > 0 and d > 0 and s > 0:
    return True
  else:
    return False


@lru_cache
def menuValidatorBuilder(validOptions):
    '''
    Generates a validator from a list of valid options

    :param validOptions: A string or tuple consisting of every valid input from a menu
    :return a function f(x) that returns if x is in validOptions
    '''

    optionsList = list(validOptions)
    return lambda menuInput: (menuInput in optionsList and menuInput != '')

@lru_cache
def rangedMenuValidatorBuilder(start, end):
  '''
  Generates a validator from a range of acceptable integer options
  
  :param start: Begining of acceptable range (inclusive)
  :param end: End of acceptable range (inclusive)
  :returns a function f(x) that returns if x is in the range of start to end (inclusive)
  '''

  optionsRange = range(start, end + 1)
  return lambda menuInput: (int(menuInput) in optionsRange and menuInput != '')


@lru_cache
def binaryOptionValidatorBuilder(firstOption, secondOption):
  '''
  Generates a validator that excepts a case-insensitive version of a binary choise

  :param firstOption: A string that represent one of the two options
  :param secondOption: A string that represent one of the two options
  :return a function f(x) that returns if lower(x) == lower(firstOption) or lower(secondOption)
  '''

  firstOption = firstOption.lower()
  secondOption = secondOption.lower()
  return lambda textInput: (textInput == firstOption or textInput == secondOption)


def optionsOrEnterBuilder(options):
  '''
  Gemerates a validator that excepts any option in the provided area or an empty string (i.e. hitting enter immediately)

  :param options: a list of strings that are valid inputs
  :return a function f(x) that returns if x is in option or is nothing
  '''

  options.append('') # Add the empty string to the list of options

  return lambda textInput: (textInput.strip() in options)


def dateValidator(potentialDate):
  '''
  Checks if a given string is a valid date string of the form mm/dd/yyyy.
  Does not care if the date actually exists, so the strings "99/01/1982" and "02/30/2000" will evaluate to True
  '''

  if not potentialDate[0:2].isnumeric():
    return False

  if not potentialDate[3:-5].isnumeric():
    return False

  if not potentialDate[-4:].isnumeric():
    return False

  return True


def gatherInput(prompt, failResponse, validator):
    '''
	  Continuously prompts the user for input, validates the input it gets are returns it if its fine or gives an error message if its bad

    :param prompt: A string the user receives when being prompted for input, used in an "input(prompt)" call
    :param failResponse: A message the user receives if they give bad input
    :param validator: A function f(x) = (x is a valid string for a given prompt)
    :return validated user input
    '''
    userInput = input(prompt)
    while True:
        if len(userInput) == 0:
            clear()
            print("Please input a response.\n")
            userInput = input(prompt)
        elif not validator(userInput):
            clear()
            print(failResponse)
            userInput = input(prompt)
        else:
            return userInput



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


def usernamesFromRows(userRows):

  usernames = []

  for row in userRows:
    usernames.append(row[1])

  return usernames


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def prettyUserInfo(userRow):
  '''
  Gets a string that is used to 'view' a user for reference when deciding who to message
  :param userRow: a complete row from the users table
  :return a string of the format "username - firstname lastname" followed by a new line character
  '''
  #userInfo = []
  #userInfo = [userRow[1], userRow[3], userRow[4]]
  #for row in userRow:
  #userInfo.append(userRow[1] + userRow[3] +userRow[4] )
  #userInfo = userRow[1] + " - " + userRow[3] + " " + userRow[4]
  

  return userRow[1] + ' - ' + userRow[3] + ' ' + userRow[4] + '\n'