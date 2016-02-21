#!/usr/bin/env python2

import socket
import threading
import time
import SocketServer
import random

HOST = "0.0.0.0"
PORT = 11071
WELCOME_MSG = "Hi, I like math and cryptography. Can you talk to me?!\n"
ERROR_MSG = "Ooops, something went wrong here. Please check your input!\n"
CORRECT_MSG = "Yay, that's right!\n"
WRONG_MSG = "Nope, that's not the right solution. Try again later!\n"
FLAG = "IW{Crypt0_c0d3}\n"
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
                    answer = int(self.decode(answer.strip()))
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

        return self.encode("x " + op + " " + str(num2) + " = " + str(res)), num1

    def _xor(self, a, b):
        return a ^ b

    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s

    def decode(self, answer):
        try:
            nums = answer.split(".")
            out = []
            for num in nums:
                o = ord(num)-51
                b = bin(o).lstrip("0b")
                b = "0" * (2-len(b)) + b
                out.append(b)
            bs = ''.join(out)
            cs = []
            for c in range(0,len(bs),8):
                b = bs[c:c+8]
                x = chr(int(b,2) ^ (2<<4))
                cs.append(x)
            s = ''.join(cs)
            return s
        except:
            return None


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