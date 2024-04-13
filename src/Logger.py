import os
from datetime import datetime
from constants import LOG_FILE_BASE_NAME, LOG_FILE_DIR

class Logger:

    def __init__(self):
        self._check_and_create_logs_folder()
        self.file_name = self.get_name_next_log_file()


    
    def _check_and_create_logs_folder(self):
        parent_directory = os.path.abspath(os.path.join(os.getcwd(), "."))
        logs_folder_path = os.path.join(parent_directory, "logs")
        if not os.path.exists(logs_folder_path):
            os.makedirs(logs_folder_path)
            print(f"The 'logs' folder has been created at: {logs_folder_path}")
        else:
            print(f"The 'logs' folder already exists at: {logs_folder_path}")


    def write_log(self, title, *content):
        file_path = LOG_FILE_DIR + self.file_name
        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        try:
            with open(file_path, 'a') as file:
                file.write(f'{timestamp} {title:} {str(content)}\n')
        except Exception as e:
            print(f"Error occurred writing to {file_path}: {e}")


    def get_name_next_log_file(self):
        files = [f for f in os.listdir(LOG_FILE_DIR)]

        if files:
            last_file = files[-1]
            number = int(last_file.split('_')[1].split('.')[0])
            next_file_name = f'logs_{"{:03d}".format(number + 1)}.txt'
            return next_file_name
        elif not files:
            return LOG_FILE_BASE_NAME
