import pytest
import sys
import builtins
from unittest import mock
import sqlite3
# from commons import *
#from states import myWorkExperience
from inCollege.manageDB import *
from inCollege.testFunc import *
from inCollege.manageDB import clearFriendships, clearUsers, friendshipsCount
from inCollege.states import friendsList, mainInterface, myEducation, newAcct, friendsProfileView, myProfile, findFriends, requestFriends, myWorkExperience, updateProfileSimple, handleFriendRequests


# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #5 Test Cases
      




# ==================================================================================
# ==================================================================================
def initTestAccounts():
    accounts = [
        ('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs', 'plus'),
        ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce', 'standard'),
        ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs', 'plus'),
        ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE', 'standard'),
        ('test5', 'aaaaaaa!A1', 'firstname', 'lastname', 'usf', 'cse', 'plus')
	]
    for account in accounts:
        inputs = iter(account)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        
            newAcct()

@pytest.mark.jobExperience
@pytest.mark.parametrize('asId, title, employer, dateStarted, dateEnded, location, workDescription, result', 
                          [
                            (1, 'CS', 'Company', 'January 2022', 'May 2022','Tampa, FL', 'description', True),
                            (1, 'softwareDeveloper', 'Company1', 'January 2022', 'May 2022', 'Tampa, FL', 'description', True),
                            (1, 'BME', 'Company2', 'January 2022', 'May 2022','Tampa, FL', 'description', True),
                            (1, 'tester', 'Company3', 'January 2022', 'May 2022', 'Tampa, FL', 'description', False),
                            

                         ]
 )


def test_jobExperience(asId, title, employer, dateStarted, dateEnded, location, workDescription, result):
    removeWorkExperience()
    inputs = iter([title, employer, dateStarted, dateEnded, location, workDescription])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        state, data = myWorkExperience(asId)
        assert getExperienceCount(asId) == 1



@pytest.mark.parametrize('select, result', 

                        [
                        ('1', updateProfileSimple),
                        ('2', updateProfileSimple),
                        ('3', updateProfileSimple),
                        ('4', updateProfileSimple),
                        ('5', myWorkExperience),
                        ('6', myEducation)])
def test_myProfile(select, result):

    clearUsers()

    initTestAccounts()


    state = result
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = myProfile(1)
        assert output == state





# @pytest.mark.friends
# @pytest.mark.parametrize('senderId, recieverUsername, lookupSelection, query, result', [
# 	(1, 'test4', '1', 'lname', requestFriends),
# 	(1, 'test2', '2', 'usf', requestFriends),
# 	(1, 'test3', '3', 'cs', requestFriends),
	
# ])
# def test_sendFriendRequestByLookup(senderId, recieverUsername, lookupSelection, query, result):
# 	clearUsers()
# 	clearFriendships()
# 	initTestAccounts()

# 	inputs = iter([query, recieverUsername, ' '])
# 	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
# 		state, data = findFriends(senderId, lookupSelection)
# 		assert state == result


# @pytest.mark.friends
# @pytest.mark.parametrize('response, numFriendsInSystem', [
# 	('yes', 1),
# 	('no', 0)
# ])
# def test_friendRequest(response, numFriendsInSystem):
# 	clearUsers()
# 	clearFriendships()
# 	initTestAccounts()

# 	inputs = iter([' ', response, ' '])

# 	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
# 		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
# 		pendingRequest(2)
# 		assert friendshipsCount() == numFriendsInSystem


def initDummyProfile(asId):
    with mock.patch.object(builtins, 'input', lambda _: '7'):
        myProfile(asId)


@pytest.mark.profileView
@pytest.mark.parametrize('shouldHaveProfile, result',
                            [
                                (True, friendsProfileView),
                                (False, mainInterface)
                            ])
def test_friendsProfileView(shouldHaveProfile, result):

    clearUsers()
    clearFriendships()
    clearProfiles()
    initTestAccounts()

    if (shouldHaveProfile):
        initDummyProfile(2)

    inputs = iter([' ', 'accept', 'yes',' ', '1','test2',' '])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
        pendingRequests = checkExistingPendingRequest(2) # get friend requests from database
        handleFriendRequests(2, pendingRequests)
        state, data = friendsList(1)
        assert state == result




  

#Story:As a student, I want to be able to create a profile
#      so that other students can learn about me.
#A profile should contain fields:
#       Title (1 line)
#       Major (title case)
#       University (title case)
#       About me (paragraph)


@pytest.mark.profiles
@pytest.mark.parametrize('choice, title, major, university, aboutme, result',
                        [
                          (1, 'test1', 'cs', 'USF', 'student', 0),
                          (2, 'test2', 'ee', 'USF', 'student', 0),
                          (3, 'test3', 'cs', 'USF', 'student', 0),
                          (4, 'test4', 'ee', 'USF', 'student', 0)
                        ]
                        )



def test_profileCreation(choice, title, major, university, aboutme, result):
    clearProfiles()

    inputs = iter(['1', ' ', title, ' ', '2', ' ', major, ' ', '3', ' ', university, ' ', '4', ' ', aboutme, ' ']
    )
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        
        updateProfileSimple(1, choice)
        assert profilesCount() == result



# Story: View my own profile



@pytest.mark.profiles
@pytest.mark.parametrize('select',
                        [('6')]
)

def test_viewMyProfile(select):
    state = myProfile
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = mainInterface(-1)
        assert output == state



# Story: Convert text to title case.



@pytest.mark.profiles
@pytest.mark.parametrize('anyCase, titleCase', [('test', 'Test'), ('university of south florida', 'University Of South Florida'), ('Computer science', 'Computer Science'), ('Wow', 'Wow')])
def test_convertTitle(anyCase, titleCase):
    assert titleCase == anyCase.title()
