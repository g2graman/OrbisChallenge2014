import random
from tronclient.Client import *


class PlayerAI():

    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        return

    def get_move(self, game_map, p_cyc, opp_cyc, moveNumber):
        m = self.mmax(game_map, p_cyc, opp_cyc)
        if(m == []):
            pos_p = p_cyc["position"]
            moves = self.moves(game_map, pos_p, p_cyc, opp_cyc)
            randMove = random.randint(0, len(moves))
            return moves[randMove - 1]
        else:
            return m.pop(0)

    def _h(self, g_map, pos_p, pos_opp):
        term, l = self.is_terminal(g_map, pos_p, pos_opp), len(g_map)
        if(term != []):
            if(len(term) == 1):
                if(term[0] != "opp"):
                    return 1000  # I win
                else:
                    return 0  # I lose
            else:
                return 300  # tie game
        else:
            if(0 <= pos_p[0] < l and 0 <= pos_p[1] < l and
                    g_map[pos_p[0]][pos_p[1]] == POWERUP):
                return 10
        return -1  # not terminal state

    def _is_invincible(self, game_map, pos_p, p_cyc):
        return 0 <= pos_p[0] < len(game_map) and \
            0 <= pos_p[1] < len(game_map) and \
            game_map[pos_p[0]][pos_p[1]] == POWERUP or p_cyc["isInvincible"]

    def _is_empty(self, game_map, pos_p):
        return 0 <= pos_p[0] < len(game_map) and \
            0 <= pos_p[1] < len(game_map) and \
            game_map[pos_p[0]][pos_p[1]] == EMPTY

    def _is_vacant(self, game_map, pos_p, p_cyc):
        return (0 <= pos_p[0] < len(game_map) or
                0 <= pos_p[1] < len(game_map)) and \
            (self._is_invincible(game_map, pos_p, p_cyc)
             or self._is_empty(game_map, pos_p))

    def moves(self, game_map, pos_p, p_cyc, opp_cyc):
        x, y, m, l = [1, 0, -1, 0], [0, 1, 0, -1], [], len(game_map)
        M = [PlayerActions.MOVE_RIGHT, PlayerActions.MOVE_DOWN,
             PlayerActions.MOVE_LEFT, PlayerActions.MOVE_UP]
        for i in range(4):
            new_x, new_y = pos_p[0] + x[i], pos_p[1] + y[i]
            if(0 <= new_x < l and
                    0 <= new_y < l and
                    self._is_vacant(game_map, (new_x, new_y), p_cyc)):
                m.append(M[i])

        if(m == []):
            # No safe moves
            m.append(PlayerActions.SAME_DIRECTION)  # Might as well keep going

            # or settle for a draw
            for i in range(4):
                new_x, new_y = pos_p[0] + x[i], pos_p[1] + y[i]
                if(0 <= new_x < l and
                        0 <= new_y < l and
                        game_map[new_x][new_y] == LIGHTCYCLE):
                    m.append(M[i])

        MAP = map(
            lambda e: (e,
                       self._h(game_map,
                               self._get_move_toward(p_cyc, e),
                               opp_cyc["position"])), m)

        MAP.sort(key=lambda e: e[1])
        m = map(lambda e: e[0], MAP)
        return m

    def mmax(self, g_map, p_cyc, opp_cyc):
        copy_map, m = g_map[:], []
        self.max_mmax(copy_map, p_cyc.copy(), opp_cyc.copy(), [0, m, 8])
        return m

    def min_mmax(self, g_map, p_cyc, opp_cyc, acc=[0, [], 0]):
        depth, m, depth_limit = acc[0], acc[1], acc[2]
        pos_p, pos_opp, l = p_cyc["position"], opp_cyc["position"], len(g_map)
        if(depth >= depth_limit):
            return
        opponent_cyc, best, copy_map = opp_cyc.copy(), float("inf"), g_map[:]
        for move in self.moves(copy_map, pos_opp, opponent_cyc, p_cyc):
            if (not (0 <= pos_opp[0] < l and 0 <= pos_opp[1] < l)):
                continue
            copy_map[pos_opp[0]][pos_opp[1]] = TRAIL
            cyc_x, cyc_y = self._get_move_toward(opponent_cyc, move)
            if (not (0 <= cyc_x < l and 0 <= cyc_y < l)):
                continue
            opponent_cyc["position"] = (cyc_x, cyc_y)
            copy_map[cyc_x][cyc_y] = LIGHTCYCLE

            self.max_mmax(
                copy_map, p_cyc, opponent_cyc, [depth + 1, m, depth_limit])
            val = self._h(g_map, (cyc_x, cyc_y), p_cyc["position"])
            best = min(val, best)

    def max_mmax(self, g_map, p_cyc, opp_cyc, acc=[0, [], 0]):
        depth, m, depth_limit = acc[0], acc[1], acc[2]
        pos_p, pos_opp, l = p_cyc["position"], opp_cyc["position"], len(g_map)
        if(depth >= depth_limit):
            return
        player_cyc = p_cyc.copy()
        best = float("-inf")
        copy_map = g_map[:]
        for move in self.moves(copy_map, pos_p, player_cyc, opp_cyc):
            if (not (0 <= pos_p[0] < l and 0 <= pos_p[1] < l)):
                continue
            copy_map[pos_p[0]][pos_p[1]] = TRAIL
            cyc_x, cyc_y = self._get_move_toward(player_cyc, move)
            if (not (0 <= cyc_x < l and 0 <= cyc_y < l)):
                continue
            player_cyc["position"] = (cyc_x, cyc_y)
            copy_map[cyc_x][cyc_y] = LIGHTCYCLE

            self.min_mmax(
                copy_map, player_cyc, opp_cyc, [depth + 1, m, depth_limit])
            val = self._h(g_map, (cyc_x, cyc_y), opp_cyc["position"])
            if(val > best):
                m.append(move)
                best = max(val, best)

    def _get_direc_vector(self, move, direction):
        x, y = [0, 0, -1, 1], [-1, 1, 0, 0]
        if(move == PlayerActions.SAME_DIRECTION):
            return x[direction], y[direction]
        return x[move - 1], y[move - 1]

    def _get_move_toward(self, p_cyc, move):
        direc_x, direc_y = self._get_direc_vector(move, p_cyc["direction"])
        return (p_cyc["position"][0] + direc_x, p_cyc["position"][1] + direc_y)

    def _is_crashed(self, g_map, pos_p, pos_opp):
        if (not(0 <= pos_p[0] < len(g_map) and
                0 <= pos_p[1] < len(g_map))):
            return False

        pos = g_map[pos_p[0]][pos_p[1]]
        return (pos == WALL or pos == TRAIL
                or pos_p == pos_opp)

    def is_terminal(self, g_map, pos_p, pos_opp):
        NOT_TERMINAL = []
        WIN = ["p"]
        LOSE = ["opp"]
        TIE = WIN + LOSE

        crash_p = self._is_crashed(g_map, pos_p, pos_opp)
        crash_opp = self._is_crashed(g_map, pos_opp, pos_p)

        result = NOT_TERMINAL
        if(crash_p):
            result = LOSE
        elif(crash_opp):
            result += WIN
        return result  # result holds the winners in a list
