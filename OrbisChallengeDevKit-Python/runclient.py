import sys, os
import logging
import traceback

sys.path.append(os.path.join(os.getcwd(), "lib"))
sys.path.append(os.path.join(os.getcwd(), "lib\\tronclient"))
sys.path.append(os.path.join(os.getcwd(), "tronplayer"))

from tronclient.Client import TronClient
import Enums
from PlayerAI import PlayerAI

if __name__ == '__main__':
        if len(sys.argv) != 4:
                print "Usage: python runclient.py <host> <port> <playername>"

        else:
                host = sys.argv[1]
                port = int(sys.argv[2])
                playername = sys.argv[3]
                TronClient().runClient(PlayerAI(), host, port, playername)
