# GroupMeGame
##This is mainly a proof of concept. For a better GroupMe bot look at https://github.com/imd8594/GroupMeReddit

Groupme tic tac toe game made using only a bot.
GroupyAPI docs here: http://groupy.readthedocs.org/en/master/
GroupMe Dev page: https://dev.groupme.com/

How to use:
  Install GroupyAPI (Instructions at http://groupy.readthedocs.org/en/master/pages/installation.html)
  Create your bot at https://dev.groupme.com/bots
  Insert groupid and bot_name into groupme_tictactoe.py
  Run

How to Play:
  start a game "!<bot_name> start, @User1, @User2
  @User1 moves first
  to move "!<bot_name> move, @User1, (Position of piece [0-8])
  to manually end a game "!<bot_name> end" (Must be creator of game to end)
  
   0 | 1 | 2 
  -----------
   3 | 4 | 5
  -----------
   6 | 7 | 8

