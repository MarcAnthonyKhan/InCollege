import pytest
import builtins
from unittest import mock
from inCollege.manageDB import clearFriendships, clearUsers, friendshipsCount
from inCollege.states import findFriends, findFriendsbyType, friendsList, mainInterface, newAcct, handleFriendRequests, requestFriends 
from inCollege.commons import *
from inCollege.testFunc import *

# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #4 Test Cases
      




# ==================================================================================
# ==================================================================================


def initTestAccounts():
	accounts = [
		('test1', '123456A!', 'first', 'last', 'usf', 'cs', 'plus'),
        ('test2', '123456A!', 'fname', 'lname', 'usf', 'ce', 'plus'),
        ('test3', '123456A!', 'f', 'l', 'hcc', 'cs', 'plus'),
        ('test4', '123456A!', 'fff', 'lll', 'NONE', 'NONE', 'plus')
	]
	for account in accounts:
		inputs = iter(account)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			newAcct()


@pytest.mark.friends
@pytest.mark.parametrize('senderId, recieverUsername, lookupSelection, query, result', [
	(1, 'test4', '1', 'lname', requestFriends),
	(1, 'test2', '2', 'usf', requestFriends),
	(1, 'test3', '3', 'cs', requestFriends),
	(1, 'johnnynohit', '1', 'nohit', findFriendsbyType),
	(1, 'test1', '1', 'last', findFriendsbyType),
	(1, '0', '1', 'lname', findFriendsbyType)
])
def test_sendFriendRequestByLookup(senderId, recieverUsername, lookupSelection, query, result):
	clearUsers()
	clearFriendships()
	initTestAccounts()

	inputs = iter([query, recieverUsername, ' '])
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		state, data = findFriends(senderId, lookupSelection)
		assert state == result


@pytest.mark.friends
@pytest.mark.parametrize('userId, response, numFriendsInSystem', [
	(2, 'accept', 2),
	(3, 'accept', 2)
])
def test_friendRequest(userId, response, numFriendsInSystem):

	inputs = iter([' ', ' ', response, ' '])

	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
		requestFriends(1, 'test3', 3) # hard-coded friend request from test1 to test3
		pendingRequests = checkExistingPendingRequest(userId) # get friend requests from database
		handleFriendRequests(userId, pendingRequests)
		assert friendshipsCount() == numFriendsInSystem
  
  
# Story: Friends
#		 As a developer, I want to add a friends list feature so that 
# 		 user’s can connect with people they know.
# Acceptance Criteria:
# 		 User will have a “show my network” option that will present 
#  		 the user with the list of people they’ve connected with (including none).
@pytest.mark.friends
@pytest.mark.parametrize('userId, friendId, result',
                        [
                        (1, 2, 1), #friend in the list
                        (1, 1, -1),
			  			(1, 0, -1)
                        ]
                        )
def test_friendList(userId, friendId, result):
    assert checkExistingFriend(userId, friendId) == result

	
@pytest.mark.friends
@pytest.mark.parametrize('disconnectChoice, numFriendsInSystem', [
	('test2', 1),
	('test3', 0)
])
def test_disconnectFriend(disconnectChoice, numFriendsInSystem):

	inputs = iter(['2', disconnectChoice, ' '])

	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):

		state, data = friendsList(1)
		if state != mainInterface:
			state, data = state(*data)
		
		assert friendshipsCount() == numFriendsInSystem
		
		
		
# Story: Total Accounts
#        As a developer, I want to increase the account limit so  
#        that InCollege can support 10 unique student accounts.   

@pytest.mark.accountNumber
def test_accountCount():
  assert accountCount(0) == True # counting the number of users in actual DB 