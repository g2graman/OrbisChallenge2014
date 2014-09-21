import random
from tronclient.Client import *

class PlayerAI():

	def __init__(self):
		self.num_moves = 0
		return


	def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
		self.num_moves = 0
		#self.player_num = player_lightcycle['playerNumber']
		#self.opponent_num = 3 - self.player_num

		#msg = TronMessage()
		#self.players = self.get_players(msg.players)
		return


	def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
		self.num_moves += 1
		self.my_pos = player_lightcycle['position']
		self.opp_pos = opponent_lightcycle['position']
		self.my_dir = player_lightcycle['direction']
		self.opp_dir = opponent_lightcycle['direction']

		my_position = self.my_pos
		my_x = my_position[0]
		my_y = my_position[1]
		my_direction = self.my_dir

		moves = self.moves(game_map, my_x, my_y)
		randMove = random.randint(0, len(moves))
		return moves[randMove - 1]


	def heuristic(self):
		return


	def moves(self, game_map, my_x, my_y):
		m = []
		if(my_x >= 0 < len(game_map) - 1 and \
		(game_map[my_x + 1][my_y] == EMPTY\
		or game_map[my_x + 1][my_y] == POWERUP)):
			m.append(PlayerActions.MOVE_RIGHT)
		if(my_y >= 0 < len(game_map) - 1 and \
		(game_map[my_x][my_y + 1] == EMPTY\
		or game_map[my_x][my_y + 1] == POWERUP)):
			m.append(PlayerActions.MOVE_DOWN)
		if(my_x > 0 and (game_map[my_x - 1][my_y] == EMPTY\
		 or game_map[my_x - 1][my_y] == POWERUP)):
			m.append(PlayerActions.MOVE_LEFT)
		if(my_y > 0 and (game_map[my_x][my_y - 1] == EMPTY\
		or game_map[my_x][my_y - 1] == POWERUP)):
			m.append(PlayerActions.MOVE_UP)

		if(m == []):
			m.append(PlayerActions.SAME_DIRECTION)
			if(game_map[my_x + 1][my_y] == LIGHTCYCLE):
				m.append(PlayerActions.MOVE_RIGHT)
			elif(game_map[my_x - 1][my_y] == LIGHTCYCLE):
				m.append(PlayerActions.MOVE_LEFT)
			elif(game_map[my_x][my_y + 1] == LIGHTCYCLE):
				m.append(PlayerActions.MOVE_DOWN)
			elif(game_map[my_x][my_y - 1] == LIGHTCYCLE):
				m.append(PlayerActions.MOVE_UP)
		return m


	def abeval(self, alpha, beta):
		return


	def wins(self):
		opp_pos = self.players[self.opponent_num]['position']
		my_pos = self.players[self.player_num]['position']
		return


	def is_terminal(self,):
		return
'''

8888888 8888888888 8 888888888o.      ,o888888o.     b.             8
      8 8888       8 8888    `88.  . 8888     `88.   888o.          8
      8 8888       8 8888     `88 ,8 8888       `8b  Y88888o.       8
      8 8888       8 8888     ,88 88 8888        `8b .`Y888888o.    8
      8 8888       8 8888.   ,88' 88 8888         88 8o. `Y888888o. 8
      8 8888       8 888888888P'  88 8888         88 8`Y8o. `Y88888o8
      8 8888       8 8888`8b      88 8888        ,8P 8   `Y8o. `Y8888
      8 8888       8 8888 `8b.    `8 8888       ,8P  8      `Y8o. `Y8
      8 8888       8 8888   `8b.   ` 8888     ,88'   8         `Y8o.`
      8 8888       8 8888     `88.    `8888888P'     8            `Yo

                                Quick Guide
                --------------------------------------------
                      Feel free to delete this comment.

        1. THIS IS THE ONLY .PY OR .BAT FILE YOU SHOULD EDIT THAT CAME FROM THE ZIPPED STARTER KIT

        2. Any external files should be accessible from this directory

        3. new_game is called once at the start of the game if you wish to initialize any values

        4. get_move is called for each turn the game goes on

        5. game_map is a 2-d array that contains values for every board position.
                example call: game_map[2][3] == POWERUP would evaluate to True if there was a powerup at (2, 3)

        6. player_lightcycle is your lightcycle and is what the turn you respond with will be applied to.
                It is a dictionary with corresponding keys: "position", "direction", "hasPowerup", "isInvincible", "powerupType"
                position is a 2-element int array representing the x, y value
                direction is the direction you are travelling in. can be compared with Direction.DIR where DIR is one of UP, RIGHT, DOWN, or LEFT
                hasPowerup is a boolean representing whether or not you have a powerup
                isInvincible is a boolean representing whether or not you are invincible
                powerupType is what, if any, powerup you have

        7. opponent_lightcycle is your opponent's lightcycle. Same keys and values as player_lightcycle

        8. You ultimately are required to return one of the following:
                                                PlayerAction.SAME_DIRECTION
                                                PlayerAction.MOVE_UP
                                                PlayerAction.MOVE_DOWN
                                                PlayerAction.MOVE_LEFT
                                                PlayerAction.MOVE_RIGHT
                                                PlayerAction.ACTIVATE_POWERUP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_UP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_DOWN
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_LEFT
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_RIGHT

        9. If you have any questions, contact challenge@orbis.com

        10. Good luck! Submissions are due Sunday, September 21 at noon. You can submit multiple times and your most recent submission will be the one graded.

'''
