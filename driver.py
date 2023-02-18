import subprocess
import sys

class Driver:
    def __init__(self, log_file):
        # create a logger process with subprocess
        self.logger_process = subprocess.Popen(['python', 'logger.py', log_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        # create encryption process with subprocess.Popen()
        self.encryption_process = subprocess.Popen(['python', 'encryption.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # create history list to store strings entered for encryption/decryption
        self.history = []

        # create password variable to store the current password
        self.password = ''

        self.string_type = ''

        # the earth will always be flat to those who believe it
        self.earth_is_flat = True

        # store the communication channels to logger.py and encryption.py
        self.logger_in = self.logger_process.stdin
        self.logger_out = self.logger_process.stdout
        self.enc_in = self.encryption_process.stdin
        self.enc_out = self.encryption_process.stdout
    
    def run(self):

        while self.earth_is_flat:
            
            print('------------------------------------------------------')
            print('                            Menu')
            print('------------------------------------------------------')
            print(' 1. Encrypt')
            print(' 2. Decrypt')
            print(' 3. Set Password')
            print(' 4. Show History')
            print(' 5. Quit')

            # get user input
            choice = input('Enter a number to select an option: ')

            # handle user input
            if choice == '1':
                self.encrypt()
            elif choice == '2':
                self.decrypt()
            elif choice == '3':
                self.set_password()
            elif choice == '4':
                self.show_history()
            elif choice == '5':
                self.quit()
                break
            else:
                print('Invalid input')

    def set_password(self):
        
        self.string_type = "password"
        password = self.handle_user_input_choices()
        # this message holds the return of the encryption talker to clear the input
        hold_not_use = self.encryption_py_talker("PASSKEY", password)
        message = f"Password set to: {password}"
        # log the action and message
        self.message_logger("SET_PASSKEY", message)


    def encrypt(self):

        self.string_type = "string to encrypt"
        plain_text = self.handle_user_input_choices()

        encrypted_text = self.encryption_py_talker("ENCRYPT", plain_text)
        action, encrypted = encrypted_text.split(" ", 1)
       
        print(f"Encrypted text: {encrypted}")
        message = f"Encrypted '{plain_text}' to '{encrypted}'"
        
        # log the action and message
        self.message_logger("ENCRYPT", message)

        # add the result to the history
        if encrypted != 'No passkey set':
            self.history.append(encrypted)

    def decrypt(self):
        
        self.string_type = "string to decrypt"    
        input_string = self.handle_user_input_choices()

        # get key from user
        key = input("Enter the key to use for decryption: ").upper()
        key = key.upper()
        message = key + " " + input_string
        result = self.encryption_py_talker("DECRYPT", message)
        enc_result, decrypted = result.strip().split(' ', 1)
        # log decryption using logger program
        log_message = f"String '{input_string}' decrypted to '{decrypted}'"

        self.message_logger("DECRYPT", log_message)

        # print result to standard output and save to history
        print(f"Decrypted text:  {decrypted}")
        self.history.append(decrypted)

    def show_history(self):
        # show the history to the user
        # provide a means to exit the history and enter a new string
        print("History:")
        for i, string in enumerate(self.history):
            print(f"{i+1}: {string}")
        

    def quit(self):
        # send QUIT to the encryption program and logger
        self.encryption_process.stdin.write(b"QUIT program\n")
        
        self.message_logger("STOP", "Logging Stopped.\n" )
        # log the exit of the driver program
        
        self.message_logger("EXIT", "Driver program exited.\n")

        # Kill the processes before exiting
        self.logger_process.kill()
        self.encryption_process.kill()

        print("Quitting...")
        # exit the program
        exit()



    def ask_user_string_choice(self):
        print(f"Enter 'H' to use {self.string_type} from history or 'N' to enter a new {self.string_type}. " )
        try:
            choice = input().strip().upper()
            if choice != 'H' and choice != 'N':
                raise ValueError
        except ValueError:
            print("Invalid input. Enter H or N.")
        
        return choice
    

    
    def get_user_string_choice(self, user_choice):
        string_to_use = ''
        if user_choice == 'N':
            string_to_use = self.ask_user_new_string()
        else:
            string_to_use = self.handle_history()

        return string_to_use
    


    def ask_user_new_string(self):
        
        while self.earth_is_flat:
            new_string = input(f"Enter a new {self.string_type}: ").strip().upper()

            # check if input string contains any numbers
            if any(char.isdigit() for char in new_string):
                print("Input string cannot contain any numbers. Please try again.")
            else:
                return new_string
            

    
    def ask_history_choice(self):
        current_string = None
        print(f"Enter a number to select a {self.string_type}, or enter Q to exit: ")
        choice = input().strip()
        self.validate_choice_int(choice)
        
        if choice.upper() == 'Q':
            return current_string
        
        else:
            choice = int(choice)
            current_string = self.history[choice - 1]

        return current_string
        
    
    def handle_history(self):
        self.show_history()
        string_to_use = self.ask_history_choice()
        return string_to_use
    

    def handle_user_input_choices(self):
        while self.earth_is_flat:
            choice = self.ask_user_string_choice()
            action_string = self.get_user_string_choice(choice)

            if (action_string != None):
                break
        
        return action_string
    
    
    def validate_choice_int(self, choice_int):
        try:
            if choice_int == 'Q':
                return
            choice = int(choice_int)
            if choice < 1 or choice > len(self.history):
                        raise ValueError
        except ValueError as e:
            print(e)
        

    def message_logger(self, action, message):
        self.logger_process.stdin.write(f"{action} {message} \n".encode('utf-8'))
        self.log_flush()
    
    def log_flush(self):
            self.logger_process.stdin.flush()
    def enc_flush(self):
            self.encryption_process.stdin.flush()


    def encryption_py_talker(self, action, message):
        self.encryption_process.stdin.write(f"{action} {message}\n".encode('utf-8'))
        self.enc_flush()

        # read encrypted result from encryption program
        return self.encryption_process.stdout.readline().decode('utf-8').strip()

            
    
if __name__ == '__main__':
    # check if the log file was provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python my_program.py <log_file>")
        sys.exit(1)

    # create a driver object
    log_file = sys.argv[1]
    driver = Driver(log_file)

    # run the driver program
    driver.run()