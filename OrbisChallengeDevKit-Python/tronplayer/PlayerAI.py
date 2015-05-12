import random
from tronclient.Client import *


class PlayerAI():

    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        return

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber, m=[]):
        m = self.mmax(game_map, player_lightcycle, opponent_lightcycle)
        if(m == []):
            my_x = player_lightcycle["position"][0]
            my_y = player_lightcycle["position"][1]

            moves = self.moves(game_map, my_x, my_y, player_lightcycle)
            randMove = random.randint(0, len(moves))
            return moves[randMove - 1]
        else:
            return m.pop(0)

    def heuristic(self, g_map, p_cyc, opp_cyc):
        term = self.is_terminal(g_map, p_cyc, opp_cyc)
        if(term != []):
            if(len(term) == 1):
                if(term[0] != "opp"):
                    # I win
                    return 1000  # I win
                else:
                    return -1000  # I lose
            else:
                return -10  # tie game
        else:
            pos_x = p_cyc["position"][0]
            pos_y = p_cyc["position"][1]
            if(g_map[pos_x][pos_y] == POWERUP):
                return 5
            return 0  # not terminal state

    def moves(self, game_map, my_x, my_y, p_cyc):
        m = []
        if(my_x >= 0 < len(game_map) - 1 and
           (game_map[my_x + 1][my_y] == EMPTY
                or game_map[my_x + 1][my_y] == POWERUP or p_cyc["isInvincible"])):
            m.append(PlayerActions.MOVE_RIGHT)
        if(my_y >= 0 < len(game_map) - 1 and
           (game_map[my_x][my_y + 1] == EMPTY
                or game_map[my_x][my_y + 1] == POWERUP or p_cyc["isInvincible"])):
            m.append(PlayerActions.MOVE_DOWN)
        if(my_x > 0 and (game_map[my_x - 1][my_y] == EMPTY
                         or game_map[my_x - 1][my_y] == POWERUP or p_cyc["isInvincible"])):
            m.append(PlayerActions.MOVE_LEFT)
        if(my_y > 0 and (game_map[my_x][my_y - 1] == EMPTY
                         or game_map[my_x][my_y - 1] == POWERUP or p_cyc["isInvincible"])):
            m.append(PlayerActions.MOVE_UP)

        if(m == []):
            # No safe moves

            m.append(PlayerActions.SAME_DIRECTION)  # Might as well keep going

            # or settle for a draw
            if(game_map[my_x + 1][my_y] == LIGHTCYCLE):
                m.append(PlayerActions.MOVE_RIGHT)
            elif(game_map[my_x - 1][my_y] == LIGHTCYCLE):
                m.append(PlayerActions.MOVE_LEFT)
            elif(game_map[my_x][my_y + 1] == LIGHTCYCLE):
                m.append(PlayerActions.MOVE_DOWN)
            elif(game_map[my_x][my_y - 1] == LIGHTCYCLE):
                m.append(PlayerActions.MOVE_UP)
        return m

    def mmax(self, g_map, p_cyc, opp_cyc):
        copy_map = g_map[:]
        player_cyc = p_cyc.copy()
        opponent_cyc = opp_cyc.copy()
        m = []
        self._mmax(copy_map, player_cyc, opponent_cyc, 8, m)
        return m

    def _mmax(self, g_map, p_cyc, opp_cyc, depth=0, max_not_min=True, m=[]):
        h = self.heuristic(g_map, p_cyc, opp_cyc)
        if(depth == 0 or h != 0):
            return h

        copy_map = g_map[:]
        if(max_not_min):
            player_cyc = p_cyc.copy()
            best = float("-inf")
            cyc_x = player_cyc["position"][0]
            cyc_y = player_cyc["position"][1]
            potential_moves = self.moves(copy_map, cyc_x, cyc_y, player_cyc)
            for move in potential_moves:
                if(move == PlayerActions.MOVE_UP
                        or (move == PlayerActions.SAME_DIRECTION
                            and player_cyc["direction"] == Direction.UP)):
                    direc_x = 0
                    direc_y = -1
                elif(move == PlayerActions.MOVE_DOWN
                        or (move == PlayerActions.SAME_DIRECTION
                            and player_cyc["direction"] == Direction.DOWN)):
                    direc_x = 0
                    direc_y = 1
                elif(move == PlayerActions.MOVE_LEFT
                        or (move == PlayerActions.SAME_DIRECTION
                            and player_cyc["direction"] == Direction.LEFT)):
                    direc_x = -1
                    direc_y = 0
                elif(move == PlayerActions.MOVE_RIGHT
                        or (move == PlayerActions.SAME_DIRECTION
                            and player_cyc["direction"] == Direction.RIGHT)):
                    direc_x = 1
                    direc_y = 0
                else:
                    direc_x = 0
                    direc_y = 0

                pos_x = cyc_x + direc_x
                pos_y = cyc_y + direc_y
                copy_map[cyc_x][cyc_y] = TRAIL
                player_cyc["position"] = (pos_x, pos_y)
                copy_map[pos_x][pos_y] = LIGHTCYCLE
                val = self._mmax(
                    copy_map, player_cyc, opp_cyc, depth - 1, False, m)
                if(val > best):
                    m.append(move)
                    best = max(val, best)
            return best
        else:
            opponent_cyc = opp_cyc.copy()
            best = float("inf")
            cyc_x = opponent_cyc["position"][0]
            cyc_y = opponent_cyc["position"][1]
            for move in self.moves(copy_map, cyc_x, cyc_y, opponent_cyc):
                if(move == PlayerActions.MOVE_UP
                        or (move == PlayerActions.SAME_DIRECTION
                            and opponent_cyc["direction"] == Direction.UP)):
                    direc_x = 0
                    direc_y = -1
                elif(move == PlayerActions.MOVE_DOWN
                        or (move == PlayerActions.SAME_DIRECTION
                            and opponent_cyc["direction"] == Direction.DOWN)):
                    direc_x = 0\
                        or (move == PlayerActions.SAME_DIRECTION
                            and opponent_cyc["direction"] == Direction.UP)
                    direc_y = 1
                elif(move == PlayerActions.MOVE_LEFT
                        or (move == PlayerActions.SAME_DIRECTION
                            and opponent_cyc["direction"] == Direction.LEFT)):
                    direc_x = -1
                    direc_y = 0
                elif(move == PlayerActions.MOVE_RIGHT
                        or (move == PlayerActions.SAME_DIRECTION
                            and opponent_cyc["direction"] == Direction.RIGHT)):
                    direc_x = 1
                    direc_y = 0
                else:
                    direc_x = 0
                    direc_y = 0

                pos_x = cyc_x + direc_x
                pos_y = cyc_y + direc_y
                copy_map[cyc_x][cyc_y] = TRAIL
                opponent_cyc["position"] = (pos_x, pos_y)
                copy_map[pos_x][pos_y] = LIGHTCYCLE
                val = self._mmax(
                    copy_map, p_cyc, opponent_cyc, depth - 1, True, m)
                best = min(val, best)
            return best

    def is_terminal(self, g_map, p_cyc, opp_cyc):
        my_pos_x = p_cyc['position'][0]
        my_pos_y = p_cyc['position'][1]
        opp_pos_x = opp_cyc['position'][0]
        opp_pos_y = opp_cyc['position'][1]

        next_pos_me = g_map[my_pos_x][my_pos_y]
        crash_me = next_pos_me == WALL or next_pos_me == TRAIL \
            or (my_pos_x == opp_pos_x and my_pos_y == opp_pos_y)

        next_pos_opp = g_map[opp_pos_x][opp_pos_y]
        crash_opp = next_pos_opp == WALL or next_pos_opp == TRAIL \
            or (my_pos_x == opp_pos_x and my_pos_y == opp_pos_y)

        if(crash_me):
            if(crash_opp):
                result = ["p", "opp"]
            else:
                result = ["opp"]
        elif(crash_opp):
            if(crash_me):
                result = ["p", "opp"]
            else:
                result = ["p"]
        else:
            result = []
        return result  # result holds the winners in a list
