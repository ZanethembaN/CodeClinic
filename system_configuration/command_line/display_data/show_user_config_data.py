import json
import os
from view_calendars.file_sytem_setup import USER_INFOS

def user_info_file_name(user_email):
    #NO longer Valid
    #folder_path = 'users_info'
    folder_path=USER_INFOS
    username = user_email.split('@')[0]
    user_info_file = '.'+username+'_user.json'
    user_info = os.path.join(folder_path, user_info_file )
    return user_info

def configuration_file(email, password):
    data = access_configuration_data()
    new_user = {"Email": email, "Password": password}
    data.append(new_user)
    path=USER_INFOS
    with open(path, 'w') as file:
        json.dump(data, file,indent=2)

def edit_configuration_password(data,password):

    for user in data:
        if user["Email"]:
            user["Password"] = password

    with open(USER_INFOS, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def one_user_file(email, password):
    #No longer Valid
    user_info = user_info_file_name(email)
    new_user = {"Email": email, "Password": password}

    with open(user_info, 'w') as file:
        json.dump(new_user, file,indent=2)
  
    
def access_configuration_data(flag = "False"):
    data = []
    
    try:
        with open(USER_INFOS, 'r') as file:
            json_data = json.load(file)
            
            for row in json_data:
                data.append(row)
            #print("From show user config\n",data)
    except json.JSONDecodeError:
        if not flag:
            print("No users have signed up yet.")
    except FileNotFoundError:
        print("User Not signed up yet")
    return data



def read_one_user_file(email):
    #Join path to user_info directory
    user_info = user_info_file_name(email)
    #with open(user_info,'r') as file:
    data=[]
    if email=="":
        print("invalid user")
        return
    with open(USER_INFOS,'r') as file:
        data = json.load(file)
        print("Data loaded",data)
    if data:
        print("Data present",data)
        for user in data:
            if user["Email"]==email:
                print(user)
                return
        print("User not found")
    else:
        print("No Users signed up yet")
