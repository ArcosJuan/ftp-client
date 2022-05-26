import os
from ftplib import FTP
from display import Display
from ftp_option import FTPOption


class FTPClient:
    
    def __init__(self):
        self.host = str()
        self.port = int()
        self.user = str()
        self.password = str()
        
        self.ftp = FTP()
        self.ftp_methods = {
            FTPOption.CHANGE_DIRECTORY: self.change_dir,
            FTPOption.LIST_DIRECTORY: self.ftp.dir,
            FTPOption.MAKE_DIRECTORY: self.make_dir,
            FTPOption.REMOVE_DIRECTORY: self.remove_dir,
            FTPOption.FILE_SIZE: self.size,
            FTPOption.RENAME_FILE: self.rename,
            FTPOption.DELETE_FILE: self.delete,
            FTPOption.DOWNLOAD_FILE: self.download,
            FTPOption.UPLOAD_FILE: self.upload,
        }
        
        Display.add_exit_methods([self.ftp.quit])

        try:
            self.connect()
            self.main()

        except KeyboardInterrupt:
            Display.exit()

      
    def execute_operation(self, msg, method, *args):
        print(f"{msg}...\r", end='') 
        result = method(*args)
        print("Operation completed!")
        Display.clear()
        return result
        
    
    def connect(self):
        while 1:
            try:
                host = Display.ask_question("Enter the host:")
                assert host.strip(), "Invalid host."

                port = Display.ask_question("Enter the port (default 21):")
                port = int(port) if port else 21 #FTP Default port
                welcome = Display.execute_operation('Conecting', self.ftp.connect, host, port)
                self.host, self.port = host, port

                user = Display.ask_question("Enter the user (default anonymous):")
                if user.strip():
                    password = Display.ask_question("Enter the password:")
                    Display.execute_operation('Login', self.ftp.login, user, password)
                    self.user, self.password = user, password

                else: Display.execute_operation('Login', self.ftp.login)
                
                print(welcome)
                break
            except Exception as error:
                print(f"Operation failed: {error}")
    
    
    def main(self):
        while 1:
            try:
                print(f"\nYour current directory is: {self.ftp.pwd()}")
                print("Options:")
                print(Display.list_to_str(Display.enum_to_list(FTPOption)))
                option = Display.ask_question("Select an option or type a ftp command:")
                try:
                    self.ftp_methods[int(option)]() 
                except:
                    self.ftp.putcmd(option) 
                    print(f'Response: {self.ftp.voidresp()}')
                    
            except Exception as error:
                Display.clear()
                print(f"Operation failed: {error}")


#region ftp-methods
    def change_dir(self):
        dir = Display.ask_question("Enter a directory:")
        self.ftp.cwd(dir)  
        Display.clear()


    def make_dir(self):
        dir = Display.ask_question("Enter the name of the new directory:")
        self.ftp.mkd(dir)  
        Display.clear()


    def remove_dir(self):
        dir = Display.ask_question("Enter the name of the directory to delete:")
        self.ftp.rmd(dir)  
        Display.clear()


    def size(self):
        file = Display.ask_question("Enter the name of a file:")
        print(f'{self.ftp.size(file)} Bytes')


    def rename(self):
        original_file = Display.ask_question("Enter the name of a file:")
        new_name =  Display.ask_question("Enter the new name:")
        self.ftp.rename(original_file, new_name)  
        Display.clear()


    def delete(self):
        file = Display.ask_question("Enter the name of a file:")
        self.ftp.delete(file)  
        Display.clear()

    def download(self):
        file_name = Display.ask_question("Enter the name of a file:")
        save_ubication = Display.ask_question("Enter a save location:")

        # If you receive a directory as a response save the response 
        # to a file with the same name as the original.
        if os.path.isdir(save_ubication):  save_ubication += f'/{file_name}'
        with open(save_ubication, 'wb') as new_file:
            self.ftp.retrbinary(f'RETR {file_name}', new_file.write) 
        Display.clear()


    def upload(self):
        file_path = Display.ask_question("Enter the path of a file:")
        save_ubication = Display.ask_question("Enter a save location:")

        with open(file_path, 'rb') as file:
            self.ftp.storbinary(f'STOR {save_ubication}', file) 
        Display.clear()


#endregion

ftp_client = FTPClient()