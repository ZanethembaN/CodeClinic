#File handler for creating and fetching data
import logging
import os,sys
import csv
import json


options=["wethinkcode","mbuja","lulama01"]
current_system=options[0]
user_path=os.path.expanduser("~")
appData_path="/.appData/code_clinics_jhb51_1/"
pre_path=user_path+appData_path

ICAL_DATA_PATH=F"/home/{current_system}/Desktop/calendar_data.ics"
DATA_PATH = F"/home/{current_system}/.appData/code_clinics_jhb51/data"
ALTERNATE_PATH = F"{pre_path}data"
CREDENTIALS_PATH = F"{pre_path}data/credentials.json"
TOKEN_PATH = F"{pre_path}data/token.json"
CALENDAR_DATA_PATH = F"{pre_path}.userData/.calendar_data.csv"
TOKENS_FOLDER_PATH = F"{pre_path}/data/tokens/"
USER_INFOS_FOLDER_PATH = F"{pre_path}.userData/.userInfo/"
USER_INFOS = F"{pre_path}.userData/.userInfo/.config_details.json"
LOGIN_STATE = F"{pre_path}.userData/LOGIN_STATE.txt"

folders = [ALTERNATE_PATH,TOKENS_FOLDER_PATH,USER_INFOS_FOLDER_PATH]
files = [CREDENTIALS_PATH,CALENDAR_DATA_PATH,USER_INFOS,LOGIN_STATE]
sys.path.append(DATA_PATH)
credentials = {"installed":{"client_id":"894156690185-rmm3ir4un6gmmgj3hk9aelgj4epf3olq.apps.googleusercontent.com",
                          "project_id":"code-clinics-jhb51",
                          "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                          "token_uri":"https://oauth2.googleapis.com/token",
                          "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                          "client_secret":"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",
                          "redirect_uris":["http://localhost"]}}


def check_path():
    if(os.path.exists(DATA_PATH)):
        print("path verified")
        logging.info("path exists")
        return True
    else:
        print("Path to be created")
        return False
    
    
def create_folder(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print(path,"path exists")
    

def write_creds():
        file = open(CREDENTIALS_PATH,"w")
        creds=json.dumps(credentials,indent=4)
        file.writelines(creds)
        file.close()
        
    
def create_files_prev():
    creds=json.dumps(credentials,indent=4)
    
    current_directory=os.getcwd()
    os.chdir(ALTERNATE_PATH)
    file = open(".calendar_data.csv",'w')
    file.close()
    
    file = open("credentials.json","w")
    file.write(creds)
    file.close()
    
    file = open(".users.csv","w")
    file.close()
    os.chdir(current_directory)


def create_file(file_path):
    try:
        file = open(file_path,"w")
         
    except FileExistsError:
        print(file_path,"- Already Exists")
        
    finally:
        file.close()


def create_folders(paths:list):
    for path in paths:
        create_folder(path)

        
def create_files(file_paths:list):
    for file in file_paths:
        create_file(file)

        
def initialise_system():

    print("Creating folders")
    create_folders(folders)
    print("Creating files")
    create_files(files)
    print("Writing creds")
    write_creds()
    
if __name__=="__main__":
    print("Initialising system")
    initialise_system()
        