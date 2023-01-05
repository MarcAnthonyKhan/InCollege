from inCollege.commons import *
from inCollege.manageDB import *
from inCollege.api import *
import datetime
import random
from datetime import datetime
import time


# initial state
testimonials = ["""InCollege helped me develop the skills I needed to land a job!
                \t-Ron Willson""",
                """My normal resume wasn't getting noticed by employers. InCollege allowed my to market my skills and begin my carrer.
                \t-Henry Close""",
                """This program made finding an internship really easy.
                \t-Taylor Oak"""]


def applicationEntry():

  print(random.choice(testimonials))
  print()

  prompt = "Please select an option below:\n"\
           "\t1. Log in to an existing account\n"\
           "\t2. Create a new account\n"\
           "\t3. Why you should join InCollege\n"\
           "\t4. Find someone you know\n"\
           "\t5. InCollege navigation links\n"\
           "Selection: "
  sel = int(gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('123456')))

  if sel == 1:
    clear()
    return login, None

  elif sel == 2:
    clear()
    return newAcct, None
    
  elif sel == 3:
    clear()
    return videoPlayer, None

  elif sel == 4:
    clear()
    return findPpl, (-1,)

  elif sel == 5:
    clear()
    return inCollegeGroups, (-1,)


# main state
def mainInterface(asId):
  usersAPI()
  prompt = "Please select an option below:\n"\
          "\t1. Jobs and Internships\n"\
          "\t2. Find your network\n"\
          "\t3. Show my network\n"\
          "\t4. Learn a new skill\n"\
          "\t5. InCollege navigation links\n"\
          "\t6. My profile\n"\
          "\t7. Messages\n"\
          "\t8. Log out\n"\
          "Selection: "
  sel = int(
          gatherInput(prompt, "Invalid input. Please try again.\n",
                      menuValidatorBuilder('12345678')))

  if sel == 1:
      clear()
      return jobInterface, (asId,)

  elif sel == 2:
      clear()
      return findFriendsbyType, (asId,)

  elif sel == 3:
      clear()
      return friendsList, (asId,)

  elif sel == 4:
      clear()
      return listSkills, (asId,)

  elif sel == 5:
      clear()
      return inCollegeGroups, (asId,)
    
  elif sel == 6:
      clear()
      return myProfile, (asId,)

  elif sel == 7:
      clear()
      return messagesInterface, (asId,)

  elif sel == 8:
      clear()
      return applicationEntry, None


# login
def login():
  if dbEmpty():
    print("\n\nNo existing accounts. Please create a new account.\n")
    return applicationEntry, None

  else:
    username = input("Username: ")
    password = input("Password: ")
  
    id = checkExistingAccts(username, password)

    if (id != -1):
      clear()
      print("\n\nYou have successfully logged in\n")
      return loginNotifications, (id,)

    else:
      clear()
      print("\n\nIncorrect username/password. Please try again.\n")
      return applicationEntry, None


# create a new account
def newAcct():
  '''
  Creates a new account based on user input. Ensures there is room in the database and username and passwords are valid.

  :sideeffect Adds a new user to the users table in the database
  :return mainInterface state function
  '''
  if dbFull():
    print("\n\nAll permitted accounts have been created, please come back later.\n")
    return exitState, -1

  username = gatherInput(
            "Enter a username: ",
            "Username already exists. Please try again.",
            unique)

  password = gatherInput(
            "\nPassword must meet the following requirements:\n"\
            "\t-Length of 8-12 characters\n"\
            "\t-Contain one capital letter\n"\
            "\t-Contain one digit\n"\
            "\t-Contain one of the following special characters: !, @, #, $, %, ^, &, *\n"\
            "\nPassword: ",
            "Password does not meet security requirements",
            passwordValidator)

  firstname = gatherInput("\nEnter your first name:\n", "", vacuouslyTrue)
  lastname = gatherInput("\nEnter your last name: \n", "", vacuouslyTrue)
  university = gatherInput("\nEnter your university (if no, enter NONE): \n", "", vacuouslyTrue)
  major = gatherInput("\nEnter your major (if no, enter NONE): \n", "", vacuouslyTrue)
  membership =  gatherInput("\nChoose your membership (Standard or Plus): \n"\
                            "\n\tStandard can't send message to stranger."\
                            "\n\tPlus can send message to everyone."\
                            "\nEnter your membership choice (standard or plus): ", "", vacuouslyTrue)


  clear()

  return mainInterface, (initAcct(username, password, firstname, lastname, university, major, membership),)


# job
def jobInterface(asId):
	
   #Number of Jobs the User Applied
  appliedJobsCount = getAppliedJobCount(asId)

  print("You have applied to", appliedJobsCount , "jobs")

  enterToContinue()
	
  prompt = "Please select an option below:\n"\
      "\t1. Post a job\n"\
      "\t2. Search for a job\n"\
      "\t3. Delete my job posting\n"\
      "\t4. Go back\n"\
      "Selection: "
  sel = int(gatherInput(prompt, "Invalid input. Please try again\n", menuValidatorBuilder('1234')))

  if sel == 1:
    clear()
    return jobPost, (asId,)

  elif sel == 2:
    clear()
    return jobViewQuery, (asId,)
  
  elif sel == 3:
    clear()
    return deleteJobPosting, (asId,)

  else:
    clear()
    return mainInterface, (asId,)


def jobViewQuery(asId):
  prompt = "Please select what jobs you wish to view:\n"\
    "\t1. View my saved jobs\n"\
    "\t2. View jobs I have applied for\n"\
    "\t3. View jobs I have NOT applied for\n"\
    "\t4. View ALL jobs\n"\
    "\t5. Go back\n"\
    "Selection: "

  sel = int(gatherInput(prompt, "", menuValidatorBuilder('123456')))

  print()

  if sel == 5:
    clear()
    return jobInterface, (asId,)

  queriedJobs = None
  
  if sel == 1:
    queriedJobs = querySavedJobs(asId)
  elif sel == 2:
    queriedJobs = queryAppliedJobs(asId)
  elif sel == 3:
    queriedJobs = queryNotAppliedJobs(asId)
  elif sel == 4:
    queriedJobs = queryAllJobs(asId)

  if queriedJobs == None or len(queriedJobs) == 0:
    print("There are no jobs available under this query.")
    enterToContinue()
    return jobViewQuery, (asId,)

  for queryIndex, job in enumerate(queriedJobs):
    print("Job ", queryIndex + 1, ": ", job[1]) # job[1] is title field

  print()

  querySel = int(gatherInput('''Select a job from the above query or enter '0' to go back: ''', 'Not a valid option.', rangedMenuValidatorBuilder(0, len(queriedJobs))))

  clear()

  if querySel == 0:
    return jobInterface, (asId,)
  
  return jobDetails, (asId, queriedJobs[querySel - 1])


  
def jobDetails(asId, job):
  print("Title:", job[1])
  print("Description:", job[2])
  print("Employer:", job[3])
  print("Location:", job[4])
  print("Salary: $", job[5], sep='')

  userApplication = getApplicationByIds(asId, job[0])

  if (userApplication == None):
    print("Applied: NO")
    print("Saved: NO")
  else:
    print("Applied: ", 'YES' if (userApplication[2] != '') else 'NO')
    print("Saved: ", 'YES' if userApplication[5] == 1 else 'NO')

  print()

  if job[6] == asId or (userApplication != None and userApplication[2] != ''):
    
    if (userApplication == None or userApplication[5] == 0):
      prompt = 'Please select an option below: \n'\
              '\t1. Save job for later\n'\
              '\t2. Go back\n'\
              'Selection: '
    else:
      prompt = 'Please select an option below: \n'\
              '\t1. Unsave job\n'\
              '\t2. Go back\n'\
              'Selection: '
    
    sel = int(gatherInput(prompt, 'Not a valid option', menuValidatorBuilder('12')))

    if sel == 1:
      toggleSavedJob(asId, job[0])

  else:
    if (userApplication == None or userApplication[5] == 0):
      prompt = 'Please select an option below: \n'\
              '\t1. Save job for later\n'\
              '\t2. Apply for this job\n'\
              '\t3. Go back\n'\
              'Selection: '
    else:
      prompt = 'Please select an option below: \n'\
              '\t1. Unsave job\n'\
              '\t2. Apply for this job\n'\
              '\t3. Go back\n'\
              'Selection: '
    
    sel = int(gatherInput(prompt, 'Not a valid option', menuValidatorBuilder('123')))

    if sel == 1:
      toggleSavedJob(asId, job[0])
      print("Job saved state updated.\n")
      enterToContinue()
    elif sel == 2:
      return applyForJob ,(asId, job[0])

  savedJobsAPI()

  return jobInterface, (asId,)


def applyForJob(asId, jobId):
  gradDate = gatherInput("Enter your planned graduation date (i.e. 01/01/2022): ", "That is not a valid date", dateValidator)
  jobAvailabilityDate = gatherInput("Enter when you will be available to being working (i.e. 01/01/2022): ", "That is not a valid date", dateValidator)
  qualifications = gatherInput("Explain why you are a good fit for this opportunity: ", "", vacuouslyTrue)
  removeOldApplication(asId, jobId)
  addJobApplication(asId, jobId, gradDate, jobAvailabilityDate, qualifications)

  print("Job application processed.\n")
  enterToContinue()

  return jobInterface, (asId,)



def jobPost(asId):
  title = gatherInput("Enter job title: ", "", vacuouslyTrue)
  description = gatherInput("Enter job description: ", "", vacuouslyTrue)
  employer = gatherInput("Enter employer: ", "", vacuouslyTrue)
  location = gatherInput("Enter job location: ", "", vacuouslyTrue)
  salary = float(gatherInput("Enter salary (no dollar sign): ", "PLease enter a valid number without a dollar sign", numberValidator))

  initJob(title, description, employer, location, salary, asId)

  jobsAPI()

  return jobInterface, (asId,)


def deleteJobPosting(asId):
  query = queryMyPostings(asId)
  if query == -1:
    print("You have not posted any jobs.\n")
  else:
    count = 0
    validSelections = "0"
    for job in query:
      count = count + 1
      validSelections = validSelections + str(count)
      print("Job #", count, ": ")
      print("\tTitle: ", job[1])
      print("\tEmployer: ", job[3])
    
    prompt = "Please select which job you would like to delete by Job# or to return to previous menu, input 0: "
    sel = int(gatherInput(prompt, "Invalid input, please try again.\n", menuValidatorBuilder(validSelections)))
    if sel == 0:
      return jobInterface, (asId,)
    
    deleteJob(query[sel-1][0])
    print("Job posting successfully deleted!\n\n")
    
    more = gatherInput("Would you like to delete another job posting? (yes / no) ", "Please enter either \"yes\" or \"no\".", binaryOptionValidatorBuilder("yes", "no"))
    if more == "yes":
      return deleteJobPosting, (asId,)
  
  return jobInterface, (asId,)
    
    

# learn skills
def listSkills(asId):
  prompt = "Please select a skill below:\n"\
          "\t1. Setup a database\n"\
          "\t2. Setup access roles\n"\
          "\t3. Use a microservice from the marketplace\n"\
          "\t4. Create budget alerts\n"\
          "\t5. Calculate OPEX costs\n"\
          "\t6. Go Back\n"\
          "Selection: "
  sel = gatherInput(prompt, "Invalid input. Please try again.\n",
                  menuValidatorBuilder('123456'))

  if sel == '6':
    clear()
    return mainInterface, (asId,)

  clear()
  return underConstruction, (asId, listSkills)


# ads video
def videoPlayer():
  print("Video is now playing\n\n")
  enterToContinue()
  return applicationEntry, None


# find InCollege existing user
def findPpl(asId):
  findFirstname = gatherInput("Enter first name: ", "", vacuouslyTrue)
  findLastname = gatherInput("Enter last name: ", "", vacuouslyTrue)

  findId = checkExistingNames(findFirstname, findLastname)

  if (findId != -1):
    clear()
    print("\n\nThey are a part of the InCollege system\n")

  else:
    clear()
    print("\n\nThey are not yet a part of the InCollege system yet. Please try again.\n")
  
  if asId == -1:
    return applicationEntry, None

  else: 
    return mainInterface, (asId,)


# Notifications upon login
def loginNotifications(asId):
  
  pendingRequests = checkExistingPendingRequest(asId)
  
  deletions = queryDeletions(asId)

  newMessageCount = getNumUnreadMessages(asId)

  currMembership = getUserMembership(asId)

  newUsers = queryNewUsersAndUpdate(asId)
	
  userProfile = checkProfileExists(asId)

  newJobs = queryNewJobsAndUpdate(asId)

  jobTitle = getJobById(asId)

  timeAccountCreated = getTimeAccountCreated(asId)
  timeAppliedJob = getTimeAppliedJob(asId)
  timeNotApply = 0
  #timeNowInSec = int(round(time.time())) # get current time in sec

  now = datetime.now() #get now time
  timeNowInSec = int(round(now.timestamp())) # convert current time to second

  if (timeAppliedJob != None): # when time applied job is after time account created
        timeNotApply = timeNowInSec - timeAppliedJob #get time difference 
  else:
        timeNotApply = timeNowInSec - timeAccountCreated

  dayNotApply = int(abs(timeNotApply) / 86400) #convert to day: 1 day = 86400 sec
  if ((dayNotApply >= 7) and (dayNotApply != None)): # if more than 7 days not applied for a job
    print("Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs Today!")

  if currMembership == "plus":
    print("Your current membership is Plus. You need to pay $10 per Month.")
  elif currMembership == "standard":
    print("Your current membership is Standard. No charge for free members.")

  if newMessageCount != 0:
    print("You have", newMessageCount, "unread messages in your inbox.\n")
    enterToContinue()


  if newUsers:
    count = 0
    print("The following", len(newUsers), "users have joined InCollege:\n")
    for newUser in newUsers:
      count = count + 1
      print("User #", count)
      print("\tName: ", newUser[3], newUser[4])
    
    enterToContinue()
	
  if deletions:

      for job in deletions:
        print("The job", job[0], "you applied to has been deleted.")

      removeDeletions(asId)
    
      enterToContinue()

  # Notification for new job post
  if newJobs:
      
      for jobTitle in newJobs:
        print("The job", jobTitle, "has been added.")

      enterToContinue()
        

  #Notification for creating the user profile
  if userProfile == -1:    
    print("Don't forget to create a profile\n")

  print(userProfile)
    
  if pendingRequests:
    
    numRequests = len(pendingRequests)

    if numRequests == 1:
      print("You have 1 pending friend request.\n")
    else:  
      print("You have", numRequests, "pending friend requests.\n")

    accept = gatherInput("Would you like to manage your incoming friend requests? (yes / no) ",
    "Please enter either \"yes\" or \"no\".",
    binaryOptionValidatorBuilder("yes", "no"))

    if accept == 'yes':
      return handleFriendRequests, (asId, pendingRequests)

  clear()

  return mainInterface, (asId,)
    

def handleFriendRequests(asId, requests):

  for request in requests:
    
    senderId = request[1]
    senderUsername = usernameLookup(senderId)

    print("<", senderUsername, "> would like to add you as a friend.")

    decide = gatherInput("Would you like to (accept) or (reject) this friend request? ",
      "Please enter either \"accept\" or \"reject\".",
      binaryOptionValidatorBuilder("accept", "reject"))

    if decide == "accept":
      confirmFriendship(senderId, asId)
    else:
      deleteFromPendingList(asId, senderId)

    clear()

  return mainInterface, (asId,)

def findFriendsbyType(asId):
  prompt = "Search by below options:\n"\
        "\t1. Last name\n"\
        "\t2. University\n"\
        "\t3. Major\n"\
        "\t4. Go Back\n"\
        "Selection: "
  sel = gatherInput(prompt, "Invalid input. Please try again.\n",
                menuValidatorBuilder('1234'))

  if sel == '1':
    clear()
    return findFriends, (asId, sel)

  elif sel == '2':
    clear()
    return findFriends, (asId, sel)

  elif sel == '3':
    clear()
    return findFriends, (asId, sel)

  elif sel == '4': 
    clear()
    return mainInterface, (asId,)


def findFriends(asId, sel):
  rows = ()

  if sel == '1':
    findLastname = gatherInput("Enter last name: ", "", vacuouslyTrue)
    findLastname.lower()
    print("\n")
    rows = getUsersWithLastname(findLastname)

  elif sel == '2':
    findUniversity = gatherInput("Enter the University: ", "", vacuouslyTrue)
    findUniversity.lower()
    print("\n")
    rows = getUsersWithUniversity(findUniversity)

  elif sel == '3':
    findMajor = gatherInput("Enter the major: ", "", vacuouslyTrue)
    findMajor.lower()
    print("\n")
    rows = getUsersWithMajor(findMajor)

  if not rows:
    print("No such data in inCollege. Please find other options.\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  count = 0
  currentUsername = ""
  selectedFriendId = 0

  for row in rows:
    if row[0] == asId:
      currentUsername = row[1] # filter out the current user from the list

    else:
      count += 1
      print(count)
      print("Username  : ", row[1])
      print("Firstname : ", row[3])
      print("Lastname  : ", row[4])
      print("University: ", row[5])
      print("Major     : ", row[6])
      print("\n")

  selectedUsername = gatherInput("Enter the username of friend you would like to connect with (or enter 0 to go back): ", "", vacuouslyTrue)
  selectedFriendId = checkUserId(selectedUsername)

  if selectedUsername == '0':
    clear()
    return findFriendsbyType, (asId,)

  elif selectedUsername == currentUsername:
    print("You are not allowed to add your account to the network list.\n\n\n")
    enterToContinue()
    return findFriendsbyType, (asId,)

  else:
    clear()
    return requestFriends, (asId, selectedUsername, selectedFriendId)
    

def requestFriends(asId, selectedUsername, selectedFriendId):
  # check the entered username exists under USERS
  exist = checkExistingUsername(selectedUsername)

  if exist == -1:
    print("Username not found. Please enter the correct username in the list.\n\n\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  # check the selected friend is already under a network list
  isAccepted = checkExistingFriend(asId, selectedFriendId)

  if isAccepted == 0: # pending
    print("You have a pending request to <", selectedUsername, ">.\n")
    print("Please wait for <", selectedUsername, "> to accept your request and choose other friends.\n\n\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  elif isAccepted == 1: # already a friend
    print("You already have <", selectedUsername, "> in your network list.\n\n\n")
    print("Please choose other friends.")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  elif isAccepted == -1: # not added to the network list

    initFriendRequest(asId,  selectedFriendId)

    print("Your network request to <", selectedUsername, "> has been sent succesfully.\n")
    print("<", selectedUsername, "> will be added to your network list as soon as they accept your request.\n\n\n")
    enterToContinue()
    return findFriendsbyType, (asId,)


def friendsList(asId):
  print("Your Network List: \n")

  friendshipsRows = queryAllFriendsOf(asId) 

  friendsKeyList = []

  for row in friendshipsRows:
    if row[1] == asId: # when the user is a sender
      friendsKeyList.append(row[2])
    elif row[2] == asId: # when the user is a receiver
      friendsKeyList.append(row[1])

  if not friendsKeyList:
    print("NONE\n\n\n")
    enterToContinue()
    return mainInterface, (asId,)
  
  else:
    count = 0
    friendsList = []

    for friendKey in friendsKeyList:

      friend = getUserById(friendKey)

      friendsList.append([friend[0], friend[1]]) # contain key and username 
      count += 1
      print(count)
      print("Username  : ", friend[1])
      print("Firstname : ", friend[3])
      print("Lastname  : ", friend[4])
      print("University: ", friend[5])
      print("Major     : ", friend[6])
      print("\n")

    print("\n")


    prompt = "Please select an option:\n"\
            "\t1. View Friend's Profile\n"\
            "\t2. Disconnecting\n"\
            "\t3. Go Back\n"\
          "Selection: "
    sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

    if sel == 1:
      print("\nWould you like to view your friend's profile in detail?\n")
      usernameSel = gatherInput("Please enter the username you would like to view (if not, enter 0): ", "", vacuouslyTrue)

      if usernameSel == '0':
        clear()
        return mainInterface, (asId,)

      else:
        friendKey = -1
        friendUsername = ''

        wrongInputCheck = 1
        for friend in friendsList:
          if friend[1] == usernameSel:
            wrongInputCheck = 0
            friendKey = friend[0]
            friendUsername = friend[1]
            break
        if wrongInputCheck == 1:
          print("\nYou entered the wrong username.")
          enterToContinue()
          return mainInterface, (asId,)

        clear()
        found = checkProfileExists(friendKey)

        if found == -1:
          print("Your friend <", friendUsername, "> has not created their profile yet.")
          enterToContinue()
          return mainInterface, (asId,)

        return friendsProfileView, (asId, friendUsername, friendKey)

    elif sel == 2:
      print("\nWould you like to disconnect with someone on your network?\n")
      disconnectSel = gatherInput("Please enter the username you would like to disonnect (if not, enter 0): ", "", vacuouslyTrue)

      if disconnectSel == '0':
        clear()
        return mainInterface, (asId,)

      else:
        friendKey = -1
        friendUsername = ''

        wrongInputCheck = 1
        for friend in friendsList:
          if friend[1] == disconnectSel:
            wrongInputCheck = 0
            friendKey = friend[0]
            friendUsername = friend[1]
            break
        if wrongInputCheck == 1:
          print("\nYou entered the wrong username.")
          enterToContinue()
          return mainInterface, (asId,)

        clear()
        return disconnectFriends, (asId, friendUsername, friendKey)
        
    else:
      return mainInterface, (asId,)


def disconnectFriends(asId, disconnectUsername, friendKey):
    deleteFromFriendList(asId, friendKey)
    print("You have successfully removed <", disconnectUsername, "> from your network.\n\n\n")

    enterToContinue()
    return mainInterface, (asId,)

# InCollege navigation links
def inCollegeGroups(asId):
  prompt = "Please select an Incollege Group:\n"\
            "\t1. Useful Links\n"\
            "\t2. Incollege Important Links\n"\
            "\t3. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

  if sel == 1:
    clear()
    return usefulLinks, (asId,)

  elif sel == 2:
    clear()
    return importantLinks, (asId,)
  else:
    clear()
    if asId == -1:
        return applicationEntry, None
    else: 
        return mainInterface, (asId,)


def usefulLinks(asId):
  prompt = "Please select an option: \n"\
            "\t1. General \n"\
            "\t2. Browser Incollege\n"\
            "\t3. Business Solutions\n"\
            "\t4. Directories\n"\
            "\t5. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12345')))

  if sel == 1:
    clear()
    return generalLinks, (asId,)

  elif sel == 2 or sel == 3 or sel == 4:
    clear()
    return underConstruction, (asId, usefulLinks)
  
  elif sel == 5:
    clear()
    return inCollegeGroups, (asId,)


def importantLinks(asId):
  prompt = "Please select a option below:\n"\
          "\t1. A Copyright Notice\n"\
          "\t2. About\n"\
          "\t3. Accessibility\n"\
          "\t4. User Agreement\n"\
          "\t5. Privacy Policy\n"\
          "\t6. Cookie Policy\n"\
          "\t7. Copyright Policy\n"\
          "\t8. Brand Policy\n"\
          "\t9. Languages\n"\
          "\t10. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid input. Please try again.\n", menuValidatorBuilder(('1','2','3','4','5','6','7','8','9','10'))))

  if sel == 1:
    clear()
    return copyRightNotice, (asId,)
  
  elif sel == 2:
    clear()
    return about, (asId,)

  elif sel == 3:
    clear()
    return accessbility, (asId,)

  elif sel == 4:
    clear()
    return userAgreement, (asId,)

  elif sel == 5:
    clear()
    return privacyPolicy, (asId,)
  
  elif sel == 6:
    clear()
    return cookiePolicy, (asId,)

  elif sel == 7:
    clear()
    return copyRightPolicy, (asId,)
    
  elif sel == 8:
    clear()
    return brandPolicy, (asId,)
  
  elif sel == 9:
    clear()
    return languages, (asId,)
  
  elif sel == 10:
    clear()
    return inCollegeGroups, (asId,)


def copyRightNotice(asId):
  print("\n\nCopyright © 2022, InColeege, All rights reserved.\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def about(asId):
  print("\n\nWelcome to InCollege, the best professional network for college students\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def accessbility(asId):
  print("\n\nHere at InCollege we commit to do everything we can to ensure that\n" + 
        "the products and services we deliver are accessible to everyone\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)
    

def userAgreement(asId):
  print("\n\nWhen you use our Services you agree to all of these terms. Your use of\n" + 
        "our Services is also subject to our Cookie Policy and our Privacy Policy,\n" + 
        "which covers how we collect, use, share, and store your personal information.\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def privacyPolicy(asId):
  print("\n\nThis Privacy Policy describes Our policies and procedures on the collection,\n" +
        "use and disclosure of Your information when You use the Service and tells You\n" +
        "about Your privacy rights and how the law protects You.\n\n\n")

  if (asId == -1):
    return importantLinks, (asId,)

  controls = checkUserGuestControls(asId)

  print("Your current privacy settings:")
  
  if (controls[0] == 1):
    print("\tInCollege Emails: ENABLED")
  else:
    print("\tInCollege Emails: DISABLED")

  if (controls[1] == 1):
    print("\tInCollege SMS: ENABLED")
  else:
    print("\tInCollege SMS: DISABLED")

  if (controls[2] == 1):
    print("\tTargeted Emails : ENABLED")
  else:
    print("\tTargeted Emails : DISABLED")

  print()

  prompt = "Please select an option: \n"\
          "\t1. Edit Guest Controls\n"\
          "\t2. Go Back\n"\
          "selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12'))) 

  if sel == 1:
    clear()
    return guestControls, (asId,)

  elif sel == 2:
    clear()
    return importantLinks, (asId,)


def guestControls(asId):
  email = gatherInput("Would you like to receive emails from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  sms = gatherInput("Would you like to receive text messages from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  targetedAds = gatherInput("Would you like personalized advertising from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  initOrUpdateUserControls(asId, email, sms, targetedAds)
  clear()
  return privacyPolicy, (asId,)

def cookiePolicy(asId):
  print("\n\nThis Cookies Policy explains what Cookies are and how We use them.\n"+ 
        "You should read this policy so You can understand what type of cookies\n" + 
        "We use, or the information We collect using Cookies and how that information is used.\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def copyRightPolicy(asId):
  print("\n\nCopyright Policy. You may not post, distribute, or reproduce in any way any\n" +
        "copyrighted material, trademarks, or other proprietary information without \n" +
        "obtaining the prior written consent of the owner of such proprietary rights.\n" +
        "If you believe that your work has been copied and posted on the Websites in\n" +
        "a way that constitutes copyright infringement, please provide us with the \n" +
        "following information: \n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def brandPolicy(asId):
  print("\n\nOur trademarks and other brand features are protected by law.\n" +  
        "You wll need our permission in order to use them.\n" +
        "For permission requests, please contact TrademarkRequest@InCollege.com\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def languages(asId):
  print("InCollege is available in ENGLISH and SPANISH.\n")

  if (asId == -1):
    return importantLinks, (asId,)

  currLanguage = checkUserLanguage(asId)[0].upper()

  print("Your current language is: " + currLanguage)

  prompt = "Please select an option: \n"\
          "\t1. Change Language\n"\
          "\t2. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12')))      

  if sel == 1:
    clear()
    return setLanguage, (asId,)
  
  elif sel == 2:
    clear()
    return importantLinks, (asId,)


def setLanguage(asId):
  lang = gatherInput("Please select a language. (English or Spanish) ",
                      "Only English and Spanish are available at this time.",
                      binaryOptionValidatorBuilder("english", "spanish")).lower()

  initOrUpdateUserLanguage(asId, lang)


  clear()
  return languages, (asId,)


def generalLinks(asId):
  prompt = "Please select an option: \n"\
            "\t1. Sign Up \n"\
            "\t2. Help Center\n"\
            "\t3. About\n"\
            "\t4. Press\n"\
            "\t5. Blog\n"\
            "\t6. Careers\n"\
            "\t7. Developers\n"\
            "\t8. Go Back \n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12345678')))

  if sel == 1:
    clear()
    return newAcct, None

  elif sel == 2:
    clear()

    print("\n\nWe're here to help\n\n")
    return generalLinks, (asId,)

  elif sel == 3:
    clear()

    print("\n\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide\n\n")
    return generalLinks, (asId,)

  elif sel == 4:
    clear()

    print("\n\nIn College Pressroom: Stay on top of the latest news, updates, and reports\n\n")
    return generalLinks, (asId,)

  elif sel == 5 or sel == 6 or sel == 7:
    clear()
    
    return underConstruction, (asId, generalLinks)

  elif sel == 8:
    clear()

    return usefulLinks, (asId,)
  
  
  
# Profiles
def myProfile(asId):
  found = checkProfileExists(asId)

  if found != -1:
    fullname = getFullname(asId)
    profileInfo = getProfile(asId)
    works = getExperience(asId)
    count = 0

    print("Name: ", fullname)
    if profileInfo[1]: print("Title: ", profileInfo[1])
    if profileInfo[2]: print("Major: ", profileInfo[2])
    if profileInfo[3]: print("University: ", profileInfo[3])
    if profileInfo[4]: print("About me: ", profileInfo[4])
    if works != -1: 
      for work in works:
        count = count + 1
        print("Work Experience (", count, "): ")
        print("\tTitle: ", work[2])
        print("\tCompany: ", work[3])
        print("\tDate Started: ", work[4])
        print("\tDate Ended: ", work[5])
        print("\tLocation: ", work[6])
        print("\tDescription: ", work[7])
    if profileInfo[5]: print("Education: ", profileInfo[5])
    if profileInfo[6]: print("Degree: ", profileInfo[6])
    if profileInfo[7]: print("Years: ", profileInfo[7])
    
    print("\n")

  else:
    initEmptyProfile(asId)
  prompt = ("Please select one of the following to update:\n"\
        "\t1. Title\n"\
        "\t2. Major\n"\
        "\t3. University\n"\
        "\t4. About me\n"\
        "\t5. Work experience\n"\
        "\t6. Education\n"\
        "\t7. Return to Main Menu\n"\
        "Selection: ")
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('1234567')))
  
  if sel == 1 or sel == 2 or sel == 3 or sel == 4:
    clear()
    return updateProfileSimple, (asId, sel)
  
  elif sel == 5:
    clear()
    return myWorkExperience, (asId, )
  
  elif sel == 6:
    clear()
    return myEducation, (asId, )
  
  else:
    clear()
    return mainInterface, (asId, )
  

def updateProfileSimple(asId, sel):
  table = "profiles"
  field = ''
  value = ''
  if sel == 1:
    field = "title"
    value = input("Title: ")
  elif sel == 2:
    field = "major"
    inValue = input("Major: ")
    value = inValue.title()
  elif sel == 3:
    field = "university"
    inValue = input("University: ")
    value = inValue.title()
  elif sel == 4:
    field = "about"
    value = input("About Me: ")
  updateDB(table, field, asId, value)
  profilesAPI()

  clear()
  return myProfile, (asId, )

def myWorkExperience(asId):
  count = getExperienceCount(asId)
  if count == 3:
    print("You have entered the three allowed work experiences.\n\n")
    return myProfile, (asId, )
  
  print("Up to three previous jobs may be listed in your profile.\n"\
        "You currently have " + str(count) + " jobs listed.\n")
  title = input("Title: ")
  employer = input("Employer: ")
  dateStarted = input("Date started (i.e. Jan 2022): ")
  dateEnded = input("Date ended (i.e. May 2022): ")
  location = input("Location (i.e. Tampa, FL): ")
  description = input("Description: ")
  
  
  initWorkExperience(asId, title, employer, dateStarted, dateEnded, location, description)

  profilesAPI()

  clear()
  return myProfile, (asId, )


def myEducation(asId):
  school = input("School: ")
  degree = input("Degree: ")
  years = input("Years attended (i.e. 2019 - 2022): ")
  updateDB("profiles", "school", asId, school.title())
  updateDB("profiles", "degree", asId, degree.title())
  updateDB("profiles", "years", asId, years)

  profilesAPI()

  clear()
  return myProfile, (asId, )


def friendsProfileView(asId, friendUsername, friendKey):
  found = checkProfileExists(friendKey)

  if found == -1:
    print("Your friend <", friendUsername, "> has not created their profile yet.")
    enterToContinue()
    return mainInterface, (asId,)
  
  else:
    fullname = getFullname(friendKey)
    profileInfo = getProfile(friendKey)
    works = getExperience(friendKey)

    print("Selected User: ", friendUsername, "\n")
    print("Name: ", fullname)
    if profileInfo[1]: print("Title: ", profileInfo[1])
    if profileInfo[2]: print("Major: ", profileInfo[2])
    if profileInfo[3]: print("University: ", profileInfo[3])
    if profileInfo[4]: print("About me: ", profileInfo[4])
    if works != -1: 
      count = 0
      for work in works:
        count = count + 1
        print("Work Experience (", count, "): ")
        print("\tTitle: ", work[2])
        print("\tCompany: ", work[3])
        print("\tDate Started: ", work[4])
        print("\tDate Ended: ", work[5])
        print("\tLocation: ", work[6])
        print("\tDescription: ", work[7])
    if profileInfo[6]: print("Education: ", profileInfo[6])
    if profileInfo[7]: print("Degree: ", profileInfo[7])
    if profileInfo[8]: print("Years: ", profileInfo[8])
    
    print("\n")

    enterToContinue()
    return mainInterface, (asId,)


def messagesInterface(asId):
      
  found = checkUserMembership(asId)

  prompt = "Please select what jobs you wish to view:\n"\
    "\t1. Send a message\n"\
    "\t2. View your inbox\n"\
    "\t3. Go back\n"\
    "Selection: "

  sel = int(gatherInput(prompt, "Invalid input, please try again.\n", menuValidatorBuilder('123')))

  if sel == 1:
    if found == "standard":
      return selectContactForMessage, (asId, getFriendsOf(asId)) # show standard list
    elif found == "plus":
      return selectContactForMessage, (asId, getAllUsersExcept(asId)) # show plus list

  if sel == 2:
    return readInbox, (asId,)

  if sel == 3:
    return mainInterface, (asId,)

  pass


def selectContactForMessage(asId, allowedRecipients):

  if allowedRecipients:

    print("You may message the following users:\n")

    allRecipInfos = ""
    for recip in allowedRecipients:
      allRecipInfos += prettyUserInfo(recip)
    print(allRecipInfos)

    allRecipUsernames = usernamesFromRows(allowedRecipients)

    selectedRecip = gatherInput("Enter the username of the user you would like to message from the above list or press ENTER to go back.",
    allRecipInfos + "\nI'm sorry, you are not friends with that person or they are not an InCollege user. Please enter the username of the user you would like to message from the above list or press ENTER to go back.\n",
    optionsOrEnterBuilder(allRecipUsernames))

    if selectedRecip == '':
      clear()
      return messagesInterface, (asId,)

    return sendMessageInterface, (asId, selectedRecip)


  else:
    clear()
    print("You do not have anyone to message at this time.")
    return messagesInterface, (asId,)
    
def sendMessageInterface(asId, recipientUsername):

  messageContent = gatherInput("What would you like to send to " + recipientUsername+ "? ","", vacuouslyTrue)

  recipId = checkUserId(recipientUsername)

  pushMessage(asId, recipId, messageContent)

  clear()
  print("Message successfully sent.")
  return messagesInterface, (asId,)

def readInbox(asId):
  
  nextMessage = readTopMessage(asId)

  if nextMessage is None:
    print("You do not have any messages in your inbox at this time.")
    enterToGoBack()
    return messagesInterface, (asId,)
  
  senderUsername = checkUsername(nextMessage[1])

  print(senderUsername, "has sent you the following message:\n\n")

  print(nextMessage[3], "\n\n")


  prompt = "Please select an option below: \n"\
    "\t1. Delete this message from your inbox (you may still reply).\n"\
    "\t2. Leave this message in your inbox.\n"\
    "Selection: "

  sel = gatherInput(prompt, "Not a valid option.", menuValidatorBuilder('12'))

  if sel == '1':
    deleteMessage(nextMessage[0])


  prompt = "Please select an option below: \n"\
    "\t1. Reply to this message.\n"\
    "\t2. Read your next message.\n"\
    "\t3. Go back.\n"\
    "Selection: "

  sel = gatherInput(prompt, "Not a valid option.", menuValidatorBuilder('123'))

  if sel == '1':
    return sendMessageInterface, (asId, senderUsername)

  if sel == '2':
    return readInbox, (asId,)

  return messagesInterface, (asId,)


  
#====================================================================================================
#====================================================================================================
  
  
  
  



#====================================================================================================
#====================================================================================================



def underConstruction(asId, prevState):
  print("\n\nUnder construction.\n")
  enterToContinue()
  return prevState, (asId, )


def exitState(asId):
  clear()
  print("Goodbye")
  exit()


def stateLoop(state):
  data = None
  while (state is not exitState):
    if data is None:
      state, data = state()
    else:
      state, data = state(*data)



#====================================================================================================
#====================================================================================================







if (__name__ == "__main__"):
  print("Welcome to InCollege!\n")
	
  stateLoop(applicationEntry)
