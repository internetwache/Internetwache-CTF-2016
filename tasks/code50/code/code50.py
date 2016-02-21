#!/usr/bin/env python2

import socket
import threading
import time
import SocketServer
import random

HOST = "0.0.0.0"
PORT = 11027
WELCOME_MSG = "Hi, I heard that you're good in math. Prove it!\n"
ERROR_MSG = "Ooops, something went wrong here. Please check your input!\n"
CORRECT_MSG = "Yay, that's right!\n"
WRONG_MSG = "Nope, that's not the right solution. Try again later!\n"
FLAG = "IW{M4TH_1S_34SY}\n"
MAX_TO_SOLVE = 100

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            self.request.sendall(WELCOME_MSG)
            num_solved = 0
            for level in range(1,MAX_TO_SOLVE+1):
                eq, res = self.rand_equation(level)
                self.request.sendall("Level {}.: {}\n".format(str(level), eq))
                try:
                    answer = self.request.recv(1024)
                    answer = int(answer.strip())
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
    def rand_equation(self, level):
        num1 = num2 = 0
        operators = ["*","+","-"]
        num_range = [2, 20*level]

        op = operators[random.randint(0, len(operators) -1)]

        while (num1 in [0,1]) or (num2 in [0,1]): 
            num1 = random.randint(num_range[0], num_range[1])
            num2 = random.randint(num_range[0], num_range[1])

        res = eval(str(num1) + " " + op + " " + str(num2))

        return "x " + op + " " + str(num2) + " = " + str(res), num1

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