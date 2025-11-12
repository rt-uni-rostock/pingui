import numpy as np
import socket
import struct
import threading
from Core import *
from Core.Datastore import datastore


# Thread to manage network communication (receiving and sending).
class NetworkManager(threading.Thread):
    def __init__(self, group='239.192.168.11', local_port=11077, dest_port=11088):
        super().__init__(daemon=True)
        self.group = group
        self.local_port = int(local_port)
        self.dest_port = int(dest_port)
        self._running = threading.Event()
        self._running.set()
        self._sock = None

    # Thread entry point: receive multicast data and write to global storage.
    # Note: This thread is started when the start() method is called.
    def run(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            try:
                self._sock.bind(('', self.local_port))
            except OSError:
                self._sock.bind((self.group, self.local_port))
            mreq = struct.pack('4sl', socket.inet_aton(self.group), socket.INADDR_ANY)
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception:
            return

        while self._running.is_set():
            try:
                data, addr = self._sock.recvfrom(65507)
            except OSError:
                break
            if len(data) < 4:
                continue
            input_data_index = np.frombuffer(data[0:4], dtype=np.uint32)[0]
            datastore.write_input(input_data_index, data[4:])
        try:
            self._sock.close()
        except Exception:
            pass

    # Stop the thread
    def stop(self):
        self._running.clear()
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass

    # Send a binary message to the multicast group
    def sendOutputData(self):
        try:
            msg_bytes = datastore.get_output()
            self._sock.sendto(msg_bytes, (self.group, self.dest_port))
        except Exception:
            pass
