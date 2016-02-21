#!/usr/bin/env python2

import socket
import threading
import time
import SocketServer
import random
import math

HOST = "0.0.0.0"
PORT = 11059
WELCOME_MSG = "Hi, you know that prime numbers are important, don't you? Help me calculating the next prime!\n"
ERROR_MSG = "Ooops, something went wrong here. Please check your input!\n"
CORRECT_MSG = "Yay, that's right!\n"
WRONG_MSG = "Nope, that's just wrong. Try again later!\n"
FLAG = "IW{Pr1m3s_4r3_!mp0rt4nt}\n"
MAX_TO_SOLVE = 100

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            self.request.sendall(WELCOME_MSG)
            num_solved = 0
            for level in range(1,MAX_TO_SOLVE+1):
                task, res = self.rand_prime(level)
                self.request.sendall("Level {}.: {}\n".format(str(level), task))
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

    def get_next_prime(self, number):
        def is_prime(number):
            for i in range(2, int(math.sqrt(number)) + 1):
                if number % i == 0:
                    return False
            return True

        test_num = number + 1
        while True:
            if is_prime(test_num):
                return test_num
            test_num += 1

    def rand_prime(self, level):
        num_range = [1, 10*level]
        rnd = random.randint(num_range[0], num_range[1])
        prime = self.get_next_prime(rnd)
        return "Find the next prime number after {}:".format(str(rnd)), prime

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
