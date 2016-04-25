# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# USAGE : python3 collect_data.py
# Author : Santhosh Nayak
# It will produce the list of tweets for the user in the file data/stream_apple.json
# Note : According to the Twitter api, they'll allow you to extract a maximum of 3,200 tweets, 200 at a time,


import sys
import tweepy
from tweepy import OAuthHandler
import time
import string
import config
import json
import os

from openpyxl import load_workbook

def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


# to get the time line of the user
def read_timeline(screen_name,outfile):

    # Twitter API Authentication
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)

    print("Initialising the Connection to Twitter API")
    time.sleep(2)
    print("Connection established... :)")

    print(" ")
    print("Extracting the tweets from user : %s" %screen_name)

    try:
        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #User display of status
        print(" ")
        print("Tweets downloaded....%s" %len(alltweets) , end=' ',flush=True)

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            #print("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            #if len(alltweets) > 1:
            oldest = alltweets[-1].id - 1

            print("...%s" %len(alltweets), end=' ',flush=True)


        print("")
        print("Downloaded %s tweets completed for the user %s "% (len(alltweets),screen_name))

        #transform the tweepy tweets into a json_strong and write into a json file
        print("")
        print("Writing the downloaded tweets into the file : %s" %outfile)
        for tweet in alltweets:
            json_str = json.dumps(tweet._json)
            with open(outfile, 'a') as f:
                f.write(json_str + "\n")
        return 1
    except tweepy.TweepError as e:
        print("Error Response :" + str(e.response))
        print("Tweepy Error Code :" + str(e.api_code))
        print("tweepy error occured for user %s" %screen_name)
        return 2
    except (ValueError, IndexError):
        print("Index error occured ")
        return 2
    except Exception:# pass:  # catch *all* exceptions
        print("Unkwown exception occured")
        return 2

#Method to get the data from the XLS file given in config file.
def extract_data_from_excel():

    # list to save all the twitter usernames of the Top Business Angels
    business_angels_list = []

    workbook = load_workbook(config.USERNAME_XLSX, use_iterators=True)
    first_sheet = workbook.get_sheet_names()[0]
    worksheet = workbook.get_sheet_by_name(first_sheet)

    #row_count = 1897  #worksheet.get_highest_row() - 1

    print("Fetching the username for %s from the Excel sheet" % config.PERSON)
    print("Please wait, this may take some time.")
    index = 0
    for row in range(config.MIX_ROW_SIZE,config.MAX_ROW_SIZE):

        for column in "G":
            cell_name = "{}{}".format(column, row)

            if worksheet[cell_name].value == config.PERSON:

                for column in "D":
                    cell_name = "{}{}".format(column, row)
                    screen_name = worksheet[cell_name].value

                    if screen_name[:5] == "https":
                        business_angels_list.append(screen_name[20:])
                    else:
                        business_angels_list.append(screen_name[19:])

        index = index+1

        #For status update
        if index == 100:
            print('*', end="", flush=True)
            index = 0

    print(" ")
    print("Extracted all the usernames for %s" % config.PERSON)
    return business_angels_list


#The main Program, entry point of the program
if __name__ == '__main__':
    print("Program Started...")


    #To fetch the data from the Excel Sheet
    username_list = extract_data_from_excel()

    if os.path.isfile(config.USERNAME_LIST_TXT):
        print("Old execution file found.Extracting information on already downloaded data.")
        f = open(config.USERNAME_LIST_TXT, 'r')
        read_userlist = f.readlines()
        #del read_userlist[-1]
        #f = open(config.USERNAME_LIST_TXT, 'w')
        #f.writelines(read_userlist)


    #print(read_userlist[(len(read_userlist) - 1)])

    temp_list = list(username_list)

    for user in username_list:
        for saved_user in read_userlist:
            saved_user = saved_user[:-1]
            if saved_user == user:
                temp_list.remove(saved_user)
                break
    print("Updated the file to remove redundant data")

    print("Number of people remaining to be extracted :" + str(len(temp_list)))
    print("Total number of people to be extracted :" + str(len(username_list)))


    #get the timeline of the user
    for user in temp_list:


        #include the data to the output json file
        query_username = format_filename(user)
        outfile = "%s/stream_%s.json" % (config.DATA_DIR, query_username)

        #with open(outfile, 'a') as f:
        #  f.write("{\"alltweets\":[")

        status = read_timeline(user,outfile)

        if status == 1:
            with open(config.USERNAME_LIST_TXT, 'a') as f:
                f.write(user + "\n")
                print("Updated the file %s" %config.USERNAME_LIST_TXT)
            print("Successfully written into the file for user : %s" %user)
            print("User %s data downloaded and written at Executed at : " % user + str(time.ctime()))
            print("system sleeps.. 5 minutes.")
            time.sleep(300)  # Arbitrary sleep time of 5 minutes to avoid the rate limit error
            print("system wakes")
            print("=======================================================")
            print("")

            #with open(outfile, 'a') as f:
            #   f.write("]}")
            # save the user_list in a file


        else:
            with open("data/error_list.txt", 'a') as f:
                f.write(user + "\n")
            print("Some Error happened when writing for user : %s!" % user)
            print("Error occurred at : " + str(time.ctime()))
            print("system sleeps.. 5 minutes.")
            time.sleep(300)  # Arbitrary sleep time of 5 minutes to avoid the rate limit error
            print("system wakes")
            print("=======================================================")
            print("")




    print("Program Completed")

    print("")
    print("****************************************************************")
    print("Program Developed by Santhosh Nayak (santhoshnayak0903@gmail.com)")
    print("****************************************************************")

# -------------------Program Ends here -------------------
