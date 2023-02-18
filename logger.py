import sys
import time
import os

# Define a constant for the date/time format
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'

"""
The Logger class provides a simple way to log messages to a file. 
It takes the name of a log file as a parameter and creates the file if it does not already exist. 
The class provides three main methods: 
    start() to log the start of the logging session, 
    log() to log a single message, 
    stop() to log the end of the session and close the log file. 
The log messages are formatted to include the current date and time, 
the action being taken (e.g. "INFO", "ERROR"), and the message itself.

"""

class Logger:
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name

        # Check if the log file exists, create it if it doesn't
        if not os.path.exists(log_file_name):
            open(log_file_name, 'w').close() # Create a new log file if it doesn't exist
        
    
        self.log_file = open(log_file_name, 'a')

        self.keep_running = True

    # Log that the logger is starting up.
    def start(self):
        # Log "START Logging Started."
        self.log_file.write(time.strftime(DATE_TIME_FORMAT) + ' [START] Logging Started.\n')

    # Log messages from standard input
    def log(self, log_message):
        if not log_message: # Check for empty input
            return

        if log_message == 'STOP Logging Stopped.':
            self.stop()
            self.keep_running = False
            return # Exit the method if the log message is "QUIT"

        try:
            # Extract the action and message from the log message
            action, message = log_message.split(None, 1)
        except ValueError:
            print(f"Invalid log message: {log_message}")
            return

        # Log the current time, action, and message to the log file
        self.log_file.write(time.strftime(DATE_TIME_FORMAT) + f' [{action}] {message}\n')

    # Log that the logger is shutting down.
    def stop(self):
        
        # Log "STOP Logging Stopped."
        self.log_file.write(time.strftime(DATE_TIME_FORMAT) + ' [STOP] Logging Stopped.\n')
        sys.stdout.flush()  # flush any remaining output before redirecting
        self.log_file.close() # Close the log file
      

    # Retrieve the keep_running variable to determine whether or not to keep running the program
    def keep_looping(self):
        if self.keep_running == False:
            return False
        else:
            return True
    
if __name__ == '__main__':
    try:
        log_file_name = sys.argv[1] # Get the log file name from the command-line argument

        logger = Logger(log_file_name)
        logger.start()

        while logger.keep_running == True:
            log_message = input() # Read a log message from standard input

            logger.log(log_message)

    except IndexError:
        print("Please provide the name of the log file as a command-line argument.")

    except OSError as e:
        print(f"Error opening log file: {e}")