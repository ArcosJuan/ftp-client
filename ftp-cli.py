from ftplib import FTP
from display import Display


class FTPCli:
    
    def __init__(self):
        self.host = str()
        self.port = int()
        self.user = str()
        self.password = str()
        
        self.ftp = FTP()
        Display.add_exit_methods([self.ftp.quit])
        self.connect()
      
    def execute_operation(self, msg, method, *args):
        print(f"{msg}...") 
        method(*args)
        print("Operation completed!")
        Display.clear()
        
    
    def connect(self):
        while 1:
            try:
                host = Display.ask_question("Enter the host:")
                assert host.strip(), "Invalid host."

                port = Display.ask_question("Enter the port (default 21):")
                port = int(port) if port else 21 #FTP Default port
                self.execute_operation('Conecting', self.ftp.connect, host, port)
                self.host, self.port = host, port

                user = Display.ask_question("Enter the user (default anonymous):")
                if user.strip():
                    password = Display.ask_question("Enter the password:")
                    self.execute_operation('Login', self.ftp.login, user, password)
                    self.user, self.password = user, password

                else: self.execute_operation('Login', self.ftp.login)
                
                break
            except Exception as error:
                print(f"Operation failed: {error}")
    
    
ftp = FTPCli()