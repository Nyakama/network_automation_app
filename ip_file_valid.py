import os.path
import sys

#Checking IP address file and content validity
def ip_file_valid():

    #Prompting user for input
    print('\n')
    ip_file = input("# Enter IP file path and name (e.g. D:\\Python\\NetworkApp\\ip_add.txt): ")

    #Checking if the file exists
    if os.path.isfile(ip_file) == True:
        print('\n')
        print("* IP file is valid. \n")
    else:
        print('\n')
        print("* File {} does not exist. Please check and try again. \n".format(ip_file))
        sys.exit()
    
    #Open user selected file for reading (IP addresses file)
    selected_ip_file = open(ip_file, 'r')

    #Starting from the beginning of the file
    selected_ip_file.seek(0)

    #Reading each line (IP address) in the file
    ip_list = selected_ip_file.readlines()

    #Closing the file
    selected_ip_file.close()
    
    #Return IP list for later use
    return ip_list