import os
import socket
import websocket
import struct

import sys
if sys.version_info >= (3, 0):
    import queue
else:
    import Queue as queue

from threading import Event, Thread
from . import IOHandler

def resolve_hostname(hostname, port):
    # We do our own mDNS resolution
    # to enforce we only search for IPV4 address
    # and avoid a 5s timeout in the websocket on the ESP
    # See https://github.com/esp8266/Arduino/issues/2110
    addrinfo = socket.getaddrinfo(hostname, port,
                                  socket.AF_INET, 0,
                                  socket.SOL_TCP)
    addr = addrinfo[0][4][0]
    return addr


class Ws(IOHandler):

    @classmethod
    def is_host_compatible(cls, host):
        try:
            socket.inet_pton(socket.AF_INET, host)
            return True
        except socket.error:
            return host.endswith('.local') or (host == "localhost")

    @classmethod
    def available_hosts(cls):
        hosts = ['pi-gate.local']

        return [
            ip
            for ip in hosts
            if os.system('ping -c 1 -W1 -t1 {} > /dev/null 2>&1'.format(ip)) == 0
        ]

    def __init__(self, host, port=9342, baudrate=None):
        host = resolve_hostname(host, port)

        self._ws = websocket.WebSocket()
        self._ws.connect("ws://" + str(host) + ":" + str(port)+"/ws")

        self._msg = queue.Queue(4096)
        self._running = True

        self._poll_loop = Thread(target=self._poll)
        self._poll_loop.daemon = True
        self._poll_loop.start()

    def is_ready(self):
        return True

    def recv(self):
        try:
            data = self._msg.get(True, 1)
        except queue.Empty:
            data = None
        return data

    def write(self, data):
        self._ws.send(data)

    def close(self):
        self._running = False
        self._poll_loop.join()
        self._ws.close()

    def _poll(self):
        def extract_line(s):
            j = s.find(b'\n')
            if j == -1:
                return b'', s
            # Sometimes the begin of serial data can be wrong remove it
            # Find the first '{'

            x = s.find(b'{')
            if x == -1:
                return b'', s[j + 1:]

            return s[x:j], s[j + 1:]

        buff = b''

        while self._running:
            s = self._ws.recv()
            buff = buff + s
            while self._running:
                line, buff = extract_line(buff)
                if not len(line):
                    break
                if self._msg.full():
                    print("Warning: Web socket message queue is full. Some datas could be lost")
                    self._msg.get()
                self._msg.put(line)
