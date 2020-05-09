import paramiko  # TODO May 08, 2020: Install Paramiko
import os.path
import time
import sys
import re

#Checking username/password file
#Prompting user for input - USERNAME/PASSWORD FILE
print('\n')
user_file = input("# Enter user file path and name (e.g. \\Python\\NetworkApp\\credentials.txt)")

#Verifying the validity of the USERNAME/PASSWORD FILE
if os.path.isfile(user_file) == True:
    print('\n')
    print(" * Password file is valid \n")
else:
    print('\n')
    print("* File {} does not exist. Please check and try again. \n".format(user_file))
    sys.exit()

#Checking commands file
#Prompting user for input - COMMANDS FILE
print('\n')
cmd_file = input("# Enter commands file path and name (e.g. \\Python\\NetworkApp\\commands.txt)")

#Verifying the validity of the COMMANDS FILE
if os.path.isfile(cmd_file) == True:
    print('\n')
    print("* Command file is valid \n")
else:
    print('\n')
    print("* File {} does not exist. Please check and try again. \n".format(cmd_file))
    sys.exit()

#Open SSHv2 connection to the device
def ssh_connection(ip):

    global user_file
    global cmd_file

    #Creating SSH CONNECTION
    try:

        #Define SSH parameters
        selected_user_file = open(user_file, 'r')

        #Starting from the beginning of the file
        selected_user_file.seek(0)

        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")

        #Starting from the beginning of the file
        selected_user_file.seek(0)

        #Reading the username from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n") 

        #Logging into device
        session = paramiko.SSHClient()

        #For testing purposes, this allows auto-accepting unknown host keys
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Connect to the device using username and password
        session.connect(ip.rstrip("\n"), username=username, password=password)

        #Start an interactive shell session on th router
        connection = session.invoke_shell()

        #Setting terminal length for entire output - disable pagination
        connection.send("enable \n")
        connection.send("terminal length 0 \n")
        time.sleep(1)

        #Entering global config mode
        connection.send("\n")
        connection.send("config terminal \n")
        time.sleep(1)

        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')

        #Starting from the beginning of the file
        selected_cmd_file.seek(0)

        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        #Closing the user file
        selected_user_file.close()

        #Closing the command file
        selected_cmd_file.close()

        #Checking command output for IOS syntax errors
        router_output = connection.recv(65535)

        if  re.search(b"% Invalid input", router_output):
            print('\n')
            print("* There was at least one IOS syntax error on device {}".format(ip))
        else:
            print('\n')
            print(" Done for the device {}\n".format(ip))
        
        #Test for reading command output
        print(str(router_output)+"\n")

        #Test for reading command output for just IP addresses
        # print(re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str(router_output)))

        #Closing the connaction
        session.close()

    except paramiko.AuthenticationException:
        print("* Invalid username or password \n * Please check the username/password file or the device configuration")
        print("* Closing program... Bye!")

