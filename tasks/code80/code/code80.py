#!/usr/bin/env python2

import socket
import threading
import time
import SocketServer
import random
import time
import hashlib

HOST = "0.0.0.0"
PORT = 11117
WELCOME_MSG = "People say, you're good at brute forcing...\nHint: Format is T:C\n"
ERROR_MSG = "Ooops, something went wrong here. Please check your input!\n"
CORRECT_MSG = "Yay, that's right!\n"
WRONG_MSG = "Nope, that's not the right solution. Try again later!\n"
FLAG = "IW{M4N_Y0U_C4N_B3_BF_M4T3RiAL!}\n"

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            self.request.sendall(WELCOME_MSG)
            for i, c in enumerate(FLAG):
                h, time, plain = self.hash(c)
                self.request.sendall("Char {}: Time is {} +- 30 seconds and the hash is: {}\n".format(str(i), time, h))
                try:
                    answer = self.request.recv(1024)
                    answer = answer.strip()
                except:
                    self.request.sendall(ERROR_MSG)
                    return

                if answer == plain:
                    self.request.sendall(CORRECT_MSG)
                else:
                    self.request.sendall(WRONG_MSG)
                    return
        except:
            return

    def hash(self, c):
        time_jitter = random.randint(-30, 30)
        t = int(time.time())
        tj = t + time_jitter
        plain = str(tj)+":"+c
        h = hashlib.sha1(plain).hexdigest()

        tstr = time.strftime("%H:%M:%S, %jth day of %Y", time.localtime(t))

        return h, tstr, plain



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