'''
The access credentials of your twitter developer account.
'''
access_token = "110033482-0clwPLHw4FiKub13Edq6sI7tUJr4ST7mBIsTIBDu"
access_token_secret = "q2pvCjJv9cDFRkyhxGc71vaCtVY9CgvQOAJQm5Vv2GI3B"
consumer_key = "2VBjEYcPGI4Ym2L1nEStyx7NR"
consumer_secret = "AXTHSaqXbs4B2n1HhdE8ZhLao20GHR1YKZcVXgSIDFC8jWXz14"

# Provide the directroy where the json files need to be saved
DATA_DIR = "data_223"

#Provide the xlsx file to be read / Source files with the list of
USERNAME_XLSX = "Twitter_MO.xlsx" #"all_data.XLSX" #"businessangels.xlsx

#A list of succesful download enrty
USERNAME_LIST_TXT = "data_223/users_list.txt"

# A lsit of people for whoem there was error dwnloading the files
WRITE_ERROR_LIST = "data_223/error_list.txt"

#Provide the min_row limit from where the data starts
MIX_ROW_SIZE = 2

#Provide the Maximum Row limit where the data ends
MAX_ROW_SIZE = 164

#Provide the details on person as to whom the data must be fetched
PERSON = ""

#To convert from json_to csv
csv_write_folder_windows= 'Y:/Hiwis/Santhosh/Twitter Project/Downloaded Tweets and data/Converted data/BA2/'
json_read_folder_windows= 'Y:/Hiwis/Santhosh/Twitter Project/Downloaded Tweets and data/test/'

# Just for personal use.
csv_write_folder_linux = 'csv_rest/'
json_read_folder_linux = 'data_rest/'

csv_write_folder = csv_write_folder_linux
json_read_folder =json_read_folder_linux


# List of user and their data.
user_list_folder = 'user_list_folder/'


#GEOBOX_WORLD = [-180,-90,180,90]
#GEOBOX_GERMANY = [5.0770049095, 47.2982950435, 15.0403900146, 54.9039819757]