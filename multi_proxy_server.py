#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process


#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
host = "www.google.com"
port = 80

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:    
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)

        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            p = Process(target=handle_proxy, args=(addr, conn))
            p.daemon = True
            p.start()
            
        proxy_start.shutdown(socket.SHUT_WR)

def handle_proxy(addr, conn):
    print("Connected by", addr)
            
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        print("Connecting to Google")

        # send data to server
        remote_ip = get_remote_ip(host)
        proxy_end.connect((remote_ip, port))
        full_data = conn.recv(BUFFER_SIZE)
        print(f'Sending recived data {full_data} to Google')
        proxy_end.sendall(full_data)

        # send returned data to client
        full_data_from_server = proxy_end.recv(BUFFER_SIZE)
        print(f'Sending reciver data {full_data_from_server} to Client')
        conn.sendall(full_data_from_server)

        proxy_end.shutdown(socket.SHUT_WR)
        conn.close()
        
if __name__ == "__main__":
    main()
