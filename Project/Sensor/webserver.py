import socket

import routes
import util
from routing import Request
import machine


class WebServer:

    def __init__(self):
        util.start_ap()
        self.router = routes.router

    def start(self):
        print('Webserver started')
        while True:
            try:
                self.run()
            except Exception as e:
                print('Web server crashed, restarting: ' + str(e))
                machine.reset()
        print('Webserver stopped')

    def run(self):
        print('TEST')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 80))
            s.listen(1)
        except OSError as e:
            print(str(e))
            print('Web server broke')
            return
        print('TEST')
        conn, addr = s.accept()
        print('TEST')
        print('Got a connection from %s' % str(addr))
        request = Request(conn.recv(1024).decode("utf-8"))
        print(request)
        response = self.router.handle_request(request)
        print(response)
        conn.send(response)
        conn.close()
        s.close()

