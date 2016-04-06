"""
	Ian Dansereau
	groupme_tictactoe.py
	April 5, 2016
	
	Groupme tic tac toe game made using only a bot.
	GroupyAPI docs here: http://groupy.readthedocs.org/en/master/
	GroupMe Dev page: https://dev.groupme.com/

"""
from groupy import Bot, Group

#groupme constents
groupid = "5598173"
bot_name = "ttt"

bot = [bot for bot in Bot.list() if bot.name == bot_name][0]

bot_triggers = ["!"+bot_name]
games = []

def printHelp():
	bot.post("To start a game do '!ttt start, @Yourname, @Opponentsname'\nTo move do '!ttt move, @Yourname, Position(0-8)'\nTo End a game do '!ttt end'")


def getBot():
	return [bot for bot in Bot.list() if bot.name == bot_name][0]

#TODO: figure out how to fix groupme output	
def printBoard(game):
	post = "     " + game['board'][0] + "   |   " + game['board'][1] + "   |   " + game['board'][2] + "\n    " + "--------" + "\n    " + game['board'][3] + "   |   " + game['board'][4] + "   |   " + game['board'][5] + "\n     " + "--------" + "\n     " + game['board'][6] + "   |   " +  game['board'][7] + "   |   " + game['board'][8] + "\n"
	bot.post(post)


def getLatestMessage():
	return [group for group in Group.list() if group.group_id == groupid][0].messages().newest


#Checks to see if the player is already participating in a game
#Returns True if player is currently in a game
def playerAlreadyInGame(playerName):
	for game in games:
		if game['p1']['name'] == playerName or game['p2']['name'] == playerName:
			return True
	return False


#Checks if there is a tie or someone has won the game
#Returns True if there is an end-game condition
def checkForWin(game):
	board = game['board']
	if board[0] == board[1] == board[2] != " ":
		endGame(game)
		return True
	if board[3] == board[4] == board[5] != " ":
		endGame(game)
		return True
	if board[0] == board[3] == board[6] != " ":
		endGame(game)
		return True
	if board[1] == board[4] == board[7] != " ":
		endGame(game)
		return True
	if board[2] == board[5] == board[8] != " ":
		endGame(game)
		return True
	if board[0] == board[4] == board[8] != " ":
		endGame(game)
		return True
	if board[2] == board[4] == board[6] != " ":
		endGame(game)
		return True
	if checkForTie(game):
		endGame(game)
		return True
	return False


def checkForTie(game):
	board = game['board']
	if " " not in board:
		return True
	else:
		return False
		

#Move validation done by making sure target space is empty and it is your turn
#Returns True if move is valid
def isValidMove(game, playerName, position):
		try:
			if game['board'][int(position)] != " ":
				return False
		except IndexError:
			return False
		if game['p1']['name'] == playerName:
			if game['p1']['turn'] == False:
				return False
		if game['p2']['name'] == playerName:
			if game['p2']['turn'] == False:
				return False
		return True


#Creates a new game and allows for multiple games at the same time
#Returns True is creating new game is successful
#Returns False if Creator of game still has an ongoing game
def newGame(player1Name, player2Name):
	player1 = {'name':player1Name, 'piece':'X', 'turn':True}
	player2 = {'name':player2Name, 'piece':'O', 'turn':False}
	board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
	for game in games:
		if game['creator'] == player1Name:
			return False
	games.append({'creator':player1Name, 'p1':player1, 'p2':player2, 'board':board})
	printBoard(games[-1])
	return True


#Method for allowing the creator of the game to end it early
#Returns true if Ending game is successful
def playerEndGame(playerName):
	index = ""
	for game in games:
		if game['creator'] == playerName:
			index = game
	try:
		games.remove(game)
		return True
	except Exception:
		return False


#Ends game when there is a winner or a tie	
#Returns True if ending the game is successful	
def endGame(game):
	try:
		games.remove(game)
		bot.post("Game over!")
		return True
	except Exception:
		return False


#Moves players piece to board position
#Returns True if PlayerMove is successful	
def doPlayerMove(playerName, boardPosition):
	move_game = ""
	playerNumber = ""
	for game in games:
		if game['p1']['name'] == playerName:
			move_game = game
			playerNumber = 'p1'
		if game['p2']['name'] == playerName:
			move_game = game
			playerNumber = 'p2'
	if isValidMove(move_game, playerName, boardPosition):
		move_game['board'][int(boardPosition)] = move_game[playerNumber]['piece']
		if playerNumber == 'p1':
			move_game['p1']['turn'] = False
			move_game['p2']['turn'] = True
		if playerNumber == 'p2':
			move_game['p2']['turn'] = False
			move_game['p1']['turn'] = True
		printBoard(move_game)
		checkForWin(move_game)
		return True
	else:
		return False	

	
#Parses command to make sure it is valid
#Returns True if command is valid
def parseCommand(name, command):
	command = command.split(",")
	command = [option.strip() for option in command]
	
	if command[0] == 'help':
		printHelp()	
		return True
	if command[0] == 'start' and command[1][0] == "@" and command[2][0] == "@":
		if not playerAlreadyInGame(command[1]) and not playerAlreadyInGame(command[2]):
			return newGame(command[1], command[2])
		else:
			return False
	if command[0] == 'end' and command[1][0] == "@":
		return playerEndGame(command[1])
	if command[0] == 'move' and command[1][0] == "@" and int(command[2]) <= 8:
		if name not in command[1]:
			return False
		if playerAlreadyInGame(command[1]):
			return doPlayerMove(command[1], command[2])
		else:
			return False
	return False


#Main process. Runs forever and will keep trying to reconnect after network failure
#Probably bad but there is no way to get notified of new messages that I know of
def runBot():
	while True:
		try:
			bot = getBot()
			message = getLatestMessage().text.lower()
			name = getLatestMessage().name.lower()
			if any(substring in message for substring in bot_triggers):
				command = message.split("!ttt")[1]
				if parseCommand(name, command):
					pass
				else:
					bot.post("Invalid Command")
		except Exception as e:
			print(e)
				
runBot()
				
				
		