#!/usr/bin/env python2

import socket
import threading
import time
import SocketServer
import random
import tree

HOST = "0.0.0.0"
PORT = 11491
WELCOME_MSG = "I'm lost in a forest. Can you invert the path?\n"
ERROR_MSG = "Ooops, something went wrong here. Please check your input!\n"
CORRECT_MSG = "Yay, that's right!\n"
WRONG_MSG = "Nope, that's not the right solution. Try again later!\n"
FLAG = "IW{10000101010101TR33}\n"
MAX_TO_SOLVE = 50

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            self.request.sendall(WELCOME_MSG)
            num_solved = 0
            for level in range(1,MAX_TO_SOLVE+1):
                eq, res = self.rand_tree(level)
                self.request.sendall("Level {}.: {}\n".format(str(level), eq))
                try:
                    answer = self.request.recv(1024)
                    answer = str(self.decode(answer.strip()))
                except:
                    self.request.sendall(ERROR_MSG)
                    return
                
                if answer == res:
                    num_solved += 1
                    self.request.sendall(CORRECT_MSG)
                else:
                    self.request.sendall(WRONG_MSG)
                    return
            if num_solved == MAX_TO_SOLVE:
                self.request.sendall(FLAG)
        except:
            return

    def rand_tree(self, level):
        num_range = [2,20*level]
        nums = [random.randint(num_range[0], num_range[1]) for i in range(2*level)]

        t = tree.BST()
        for num in nums:
            t.insertVal(num)
        tchal = t.serialize(t.root)
        t.invert(t.root)
        tsol = t.serialize(t.root)

        return self.encode(tchal), str(tsol) 

    def encode(self, l):
        return l

    def decode(self, answer):
        return str(answer)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()

    while True:
        try:
            time.sleep(1)
        except:
            break

    server.shutdown()
    server.server_close()