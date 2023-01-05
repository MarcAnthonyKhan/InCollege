import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import clearApplications, clearFriendships, clearJobs, clearUsers, getFriendsOf, checkUserId, clearMessages, getAllUsersExcept
from inCollege.states import messagesInterface, loginNotifications, newAcct, requestFriends, sendMessageInterface, selectContactForMessage, readInbox
from inCollege.testFunc import getMessageCount, getMembershipStatus

database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()


# ==================================================================================
# ==================================================================================





# EPIC #7 Test Cases





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


def initTestFriendships():
	inputs = iter([' ',' ',' ',' ',' ',' ','yes','accept', 'accept','', 'yes', 'accept','', 'yes', 'accept','', 'yes', 'accept'])
	
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):

		requestFriends(1,'test2', 2)
		requestFriends(2, 'test3', 3)
		requestFriends(3, 'test4', 4)
		requestFriends(3, 'test1', 1)
		requestFriends(4, 'test1', 1)

		state, data = loginNotifications(1)
		state(*data)
		state, data = loginNotifications(2)
		state(*data)
		state, data = loginNotifications(3)
		state(*data)
		state, data = loginNotifications(4)
		state(*data)


@pytest.mark.friends
@pytest.mark.parametrize('userId, numFriends', [(1, 3), (2,2), (3,3), (4,2)])
def test_getFriendsOfCorrectNum(userId, numFriends):
	clearUsers()
	clearFriendships()
	clearJobs()
	clearApplications()
	clearMessages()

	initTestAccounts()
	initTestFriendships()
	
	assert len(getFriendsOf(userId)) == numFriends
 
 
def messageSent(senderId, receiverId):
    message = databaseCursor.execute('SELECT content FROM messages WHERE senderId = ? and receiverId = ?', (senderId, receiverId)).fetchone()
    return True if message[0] == 'test message' else False


@pytest.mark.messagingFriend
@pytest.mark.parametrize('userId, recipient, message',
                         [(1, 'test2', 'test message'),
                          (2, 'test3', 'test message'),
                          (3, 'test4', 'test message'),
                          (4, 'test1', 'test message')])
def test_sendMessageToFriend(userId, recipient, message):
     
	inputs = iter([message])
	rId = checkUserId(recipient)
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		sendMessageInterface(userId, recipient)
		assert True == messageSent(userId, rId)

 
@pytest.mark.messageNotification
@pytest.mark.parametrize('userId', [1, 2, 3, 4])
def test_messageNotification(capfd, userId):
	inputs = iter([''])
	message = "You have 1 unread messages in your inbox.\n"
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		output, dataOut = loginNotifications(userId)
		out, err = capfd.readouterr()
		assert True if message in out else False == True
  
  

@pytest.mark.differentAccountMessaging
@pytest.mark.parametrize('select, userId, username, result', [(1, 2, 'test1', sendMessageInterface), 
                                    (2, 2, 'test4', "\nI'm sorry, you are not friends with that person or they are not an InCollege user. Please enter the username of the user you would like to message from the above list or press ENTER to go back.\n")])
def test_standardMessaging(capfd, select, userId, username, result):
	state = result
	allowed = getFriendsOf(userId)
	if select % 2 == 1:
		with mock.patch.object(builtins, 'input', lambda _: username):
			output, dataOut = selectContactForMessage(userId, allowed)
			assert output == state
	else:
		inputs = iter([username, 'test1'])
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			output, dataOut = selectContactForMessage(userId, allowed)
			out, err = capfd.readouterr()
			assert True if result in out else False == True
    
    
@pytest.mark.differentAccountMessaging
@pytest.mark.parametrize('userId, username', [(1, 'test2'), 
                                              (1, 'test3'), 
                                              (1, 'test4')])
def test_plusMessaging(userId, username):
    allowed = getAllUsersExcept(userId)
    state = sendMessageInterface
    with mock.patch.object(builtins, 'input', lambda _: username):
        output, dataOut = selectContactForMessage(userId, allowed)
        assert output == state
        

@pytest.mark.messageResponse
@pytest.mark.parametrize('userId, option, reply', [(1, '2', '1'), 
												   (2, '2', '1'), 
												   (3, '2', '1'),
												   (4, '2', '1')])
def test_respondingToMessage(userId, option, reply):
    state = sendMessageInterface
    inputs = iter([option, reply])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        output, dataOut = readInbox(userId)
        assert output == state
        
        
@pytest.mark.showFriends
@pytest.mark.parametrize('userId, username, friends', [(1, 'test2', '''test2 - fname lname\ntest3 - f l\ntest4 - fff lll'''), 
                                            		  (4, 'test1', '''test1 - first last\ntest3 - f l''')])
def test_showFriends(capfd, userId, username, friends):
	allowed = getAllUsersExcept(userId) if userId == 1 else getFriendsOf(userId)
	with mock.patch.object(builtins, 'input', lambda _: username):
		output, dataOut = selectContactForMessage(userId, allowed)
		out, err = capfd.readouterr()
		assert True if friends in out else False == True


@pytest.mark.showMembership
@pytest.mark.parametrize('userId', [1, 3, 5])
def test_membershipStatus(capfd, userId):
	inputs = iter([''])
	message = "Your current membership is Plus. You need to pay $10 per Month.\n"
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		output, dataOut = loginNotifications(userId)
		out, err = capfd.readouterr()
		assert True if message in out else False == True


@pytest.mark.deleteMessage
@pytest.mark.parametrize('userId, option, view', [(1, '1', '2'), 
												  (2, '1', '2'), 
												  (3, '1', '2'),
												  (4, '1', '2')])
def test_deleteMessage(userId, option, view):
	inputs = iter([option, view])
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		output, dataOut = readInbox(userId)
		msgCount = getMessageCount(userId)
		assert msgCount == 0


@pytest.mark.membershipOption
@pytest.mark.parametrize('userId, membershipStatus', [(1, 'plus'), (2, 'standard'), (3, 'plus'), (4, 'standard'), (5, 'plus')])
def test_membershipOption(userId, membershipStatus):
	assert getMembershipStatus(userId) == membershipStatus


@pytest.mark.showMessages
@pytest.mark.parametrize('select', [('2')])
def test_viewJobInteface(select):
    state = readInbox
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = messagesInterface(-1)
        assert output == state