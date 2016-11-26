from requests import *
import json
import csv
import time
from expects import *
from openpyxl import load_workbook
import config
import os

BASEURL= "https://app.receptiviti.com"
apikey = "5807461720a25d05ba70138a" #""57dbc1888f974a05aa1af46c"
apisecret = "ldANecnXiQKeazhIIQIXqxG8F3i4FCI5Mu8m56sM0x8" #""K1aBm6H2vnllI7WREE2ct5HasuMyUHEY8hfhtc4huho"

csv_header = ['Twitter Account','Word Count','Analytical Thinking','Clout','Authentic','Emotional tone','Words/sentence','Words > 6 letters', 'Dictionary words', 'Total function words',
              'Total pronouns' , 'Personal pronouns', '1st pers singular', '1st pers plural', '2nd person', '3rd pers singular', '3rd pers plural', 'Impersonal pronouns', 'Articles','Prepositions' ,'Auxiliary verbs',
              'Common Adverbs', 'Conjunctions','Negations', 'Common verbs','Common adjectives', 'Comparisons' , 'Interrogatives', 'Numbers','Quantifiers','Affective processes',
              'Positive emotion', 'Negative emotion','Anxiety' , 'Anger' , 'Sadness' , 'Social processes', 'Family','Friends', 'Female references','Male references', 'Cognitive processes',
              'Insight','Causation', 'Discrepancy' , 'Tentative' , 'Certainty', 'Differentiation', 'Perceptual processes','See','Hear','Feel', 'Biological processes','Body',
              'Health','Sexual','Ingestion', 'Drives','Affiliation','Achievement','Power','Reward','Risk','Past Focus', 'Present Focus', 'Future Focus' ,'Relativity',
              'Motion','Space', 'Time','Work', 'Leisure' , 'Home' , 'Money' , 'Religion' , 'Death' , 'Informal Language' , 'Swear words' , 'Netspeak' , 'Assent' , 'Nonfluencies' ,
              'Fillers' , 'All Puntuations','Periods' , 'Commas' , 'Colons' , 'Semicolons' , 'Question marks' , 'Exclamation marks' , 'Dashes' , 'Quotation marks' , 'Apostrophes' ,
              'Parentheses','Other punctuation' ]

csv_header_receptivity = ['Twitter Account','raw_scores achievement_driven','raw_scores adjustment', 'raw_scores agreeable', 'raw_scores body_focus', 'raw_scores cold' ,
                          'raw_scores conscientious',  'raw_scores depression', ' raw_scores extraversion', 'raw_scores family_oriented', 'raw_scores food_focus',
                          'raw_scores friend_focus', 'raw_scores happiness', 'raw_scores health_oriented','raw_scores impulsive', 'raw_scores independent',
                          'raw_scores insecure', 'raw_scores leisure_oriented', 'raw_scores money_oriented', 'raw_scores netspeak_focus', 'raw_scores neuroticism',
                          'raw_scores openness', 'raw_scores persuasive','raw_scores power_driven',  'raw_scores religion_oriented' , 'raw_scores reward_bias',
                          'raw_scores sexual_focus', 'raw_scores social_skills','raw_scores thinking_style','raw_scores type_a','raw_scores work_oriented',
                          'raw_scores workhorse' ,

                          'percentiles achievement_driven', 'percentiles adjustment', 'percentiles agreeable',
                          'percentiles body_focus', 'percentiles cold', 'percentiles conscientious', 'percentiles depression',
                          'percentiles extraversion', 'percentiles family_oriented', 'percentiles food_focus', 'percentiles friend_focus', 'percentiles happiness',
                          'percentiles health_oriented', 'percentiles impulsive', 'percentiles independent', 'percentiles insecure',
                          'percentiles leisure_oriented', 'percentiles money_oriented', 'percentiles netspeak_focus', 'percentiles neuroticism', 'percentiles openness',
                          'percentiles persuasive', 'percentiles power_driven', 'percentiles religion_oriented',
                          'percentiles reward_bias', 'percentiles sexual_focus', 'percentiles social_skills', 'percentiles thinking_style', 'percentiles type_a', 'percentiles work_oriented',
                          'percentiles workhorse']

header = {}


twitter_handle = ""

def twitter_import_user_api_url(baseurl):
    return "{}/import/twitter/user".format(api_base_url(baseurl))

def api_base_url(baseurl):
    return "{}/api".format(baseurl)

def import_twitter_user(url, headers, handle):
    other_data = {'screen_name': handle}
    other_data = json.dumps(other_data)
    return  post(url, data=other_data, headers=headers, allow_redirects=False)

def get_user_analysis_data(response):

    status_check_url = "{}{}".format(BASEURL, response.json()["_links"]["self"]["href"])
    latest_response = response.json()
    idx = 1
    while latest_response["status"] not in ["Finished", "Failed", "Error"]:
        time.sleep(5)
        response = get(status_check_url, headers=header)
        expect(response.status_code).to(equal(200))
        latest_response = response.json()
        print("Retry {}: Status - {}. Last updated = {}".format(idx, latest_response["status"],
                                                                latest_response["updated"]))
        idx += 1
    expect(latest_response["search_key"]).to(equal(twitter_handle))

    people_url = "{}{}".format(BASEURL, response.json()["_links"]["people"]["href"])
    response = get(people_url, headers=header)

    if (latest_response["status"] == "Error" or latest_response["status"] == "Failed"):
        json_response = None
    else:
        json_response = response.json()
    return json_response


def get_liwc_scores(data):
    # initialize an array
    row = []

    # add every 'cell' to the row list, identifying the item just like an index in a list
    row.append(data[0]['person_handle'])

    row.append(data[0]['liwc_scores']['wc'])

    #Summary Language Variables
    row.append(data[0]['liwc_scores']['analytic'])
    row.append(data[0]['liwc_scores']['clout'])
    row.append(data[0]['liwc_scores']['authentic'])
    row.append(data[0]['liwc_scores']['tone'])
    row.append(data[0]['liwc_scores']['wps'])
    row.append(data[0]['liwc_scores']['sixLtr'])
    row.append(data[0]['liwc_scores']['dic'])

    #Linguistic Dimensions
    row.append(data[0]['liwc_scores']['categories']['function'])
    row.append(data[0]['liwc_scores']['categories']['pronoun'])
    row.append(data[0]['liwc_scores']['categories']['ppron'])
    row.append(data[0]['liwc_scores']['categories']['i'])
    row.append(data[0]['liwc_scores']['categories']['we'])
    row.append(data[0]['liwc_scores']['categories']['you'])
    row.append(data[0]['liwc_scores']['categories']['shehe'])
    row.append(data[0]['liwc_scores']['categories']['they'])
    row.append(data[0]['liwc_scores']['categories']['ipron'])
    row.append(data[0]['liwc_scores']['categories']['article'])
    row.append(data[0]['liwc_scores']['categories']['prep'])
    row.append(data[0]['liwc_scores']['categories']['auxverb'])
    row.append(data[0]['liwc_scores']['categories']['adverb'])
    row.append(data[0]['liwc_scores']['categories']['conj'])
    row.append(data[0]['liwc_scores']['categories']['negate'])

    #Other Grammar
    row.append(data[0]['liwc_scores']['categories']['verb'])
    row.append(data[0]['liwc_scores']['categories']['adj'])
    row.append(data[0]['liwc_scores']['categories']['compare'])
    row.append(data[0]['liwc_scores']['categories']['interrog'])
    row.append(data[0]['liwc_scores']['categories']['number'])
    row.append(data[0]['liwc_scores']['categories']['quant'])

    #Psychological Processes
    row.append(data[0]['liwc_scores']['categories']['affect'])
    row.append(data[0]['liwc_scores']['categories']['posemo'])
    row.append(data[0]['liwc_scores']['categories']['negemo'])
    row.append(data[0]['liwc_scores']['categories']['anx'])
    row.append(data[0]['liwc_scores']['categories']['anger'])
    row.append(data[0]['liwc_scores']['categories']['sad'])
    row.append(data[0]['liwc_scores']['categories']['social'])
    row.append(data[0]['liwc_scores']['categories']['family'])
    row.append(data[0]['liwc_scores']['categories']['friend'])
    row.append(data[0]['liwc_scores']['categories']['female'])
    row.append(data[0]['liwc_scores']['categories']['male'])
    row.append(data[0]['liwc_scores']['categories']['cogproc'])
    row.append(data[0]['liwc_scores']['categories']['insight'])
    row.append(data[0]['liwc_scores']['categories']['cause'])
    row.append(data[0]['liwc_scores']['categories']['discrep'])
    row.append(data[0]['liwc_scores']['categories']['tentat'])
    row.append(data[0]['liwc_scores']['categories']['certain'])
    row.append(data[0]['liwc_scores']['categories']['differ'])
    row.append(data[0]['liwc_scores']['categories']['percept'])
    row.append(data[0]['liwc_scores']['categories']['see'])
    row.append(data[0]['liwc_scores']['categories']['hear'])
    row.append(data[0]['liwc_scores']['categories']['feel'])
    row.append(data[0]['liwc_scores']['categories']['bio'])
    row.append(data[0]['liwc_scores']['categories']['body'])
    row.append(data[0]['liwc_scores']['categories']['health'])
    row.append(data[0]['liwc_scores']['categories']['sexual'])
    row.append(data[0]['liwc_scores']['categories']['ingest'])
    row.append(data[0]['liwc_scores']['categories']['drives'])
    row.append(data[0]['liwc_scores']['categories']['affiliation'])
    row.append(data[0]['liwc_scores']['categories']['achieve'])
    row.append(data[0]['liwc_scores']['categories']['power'])
    row.append(data[0]['liwc_scores']['categories']['reward'])
    row.append(data[0]['liwc_scores']['categories']['risk'])

    #Time orientations
    row.append(data[0]['liwc_scores']['categories']['focuspast'])
    row.append(data[0]['liwc_scores']['categories']['focuspresent'])
    row.append(data[0]['liwc_scores']['categories']['focusfuture'])
    row.append(data[0]['liwc_scores']['categories']['relativ'])
    row.append(data[0]['liwc_scores']['categories']['motion'])
    row.append(data[0]['liwc_scores']['categories']['space'])
    row.append(data[0]['liwc_scores']['categories']['time'])

    #Personal concerns
    row.append(data[0]['liwc_scores']['categories']['work'])
    row.append(data[0]['liwc_scores']['categories']['leisure'])
    row.append(data[0]['liwc_scores']['categories']['home'])
    row.append(data[0]['liwc_scores']['categories']['money'])
    row.append(data[0]['liwc_scores']['categories']['relig'])
    row.append(data[0]['liwc_scores']['categories']['death'])
    row.append(data[0]['liwc_scores']['categories']['informal'])
    row.append(data[0]['liwc_scores']['categories']['swear'])
    row.append(data[0]['liwc_scores']['categories']['netspeak'])
    row.append(data[0]['liwc_scores']['categories']['assent'])
    row.append(data[0]['liwc_scores']['categories']['nonflu'])
    row.append(data[0]['liwc_scores']['categories']['filler'])

    #Puntuations
    row.append(data[0]['liwc_scores']['categories']['AllPunc'])
    row.append(data[0]['liwc_scores']['categories']['Period'])
    row.append(data[0]['liwc_scores']['categories']['Comma'])
    row.append(data[0]['liwc_scores']['categories']['Colon'])
    row.append(data[0]['liwc_scores']['categories']['SemiC'])
    row.append(data[0]['liwc_scores']['categories']['QMark'])
    row.append(data[0]['liwc_scores']['categories']['Exclam'])
    row.append(data[0]['liwc_scores']['categories']['Dash'])
    row.append(data[0]['liwc_scores']['categories']['Quote'])
    row.append(data[0]['liwc_scores']['categories']['Apostro'])
    row.append(data[0]['liwc_scores']['categories']['Parenth'])
    row.append(data[0]['liwc_scores']['categories']['OtherP'])
    return row


def get_receptiviti_scores(data):
    # initialize an array
    row = []

    # add every 'cell' to the row list, identifying the item just like an index in a list
    row.append(data[0]['person_handle'])

    #Raw Scores
    row.append(data[0]['receptiviti_scores']['raw_scores']['achievement_driven'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['adjustment'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['agreeable'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['body_focus'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['cold'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['conscientious'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['depression'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['extraversion'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['family_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['food_focus'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['friend_focus'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['happiness'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['health_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['impulsive'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['independent'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['insecure'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['leisure_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['money_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['netspeak_focus'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['neuroticism'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['openness'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['persuasive'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['power_driven'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['religion_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['reward_bias'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['sexual_focus'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['social_skills'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['thinking_style'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['type_a'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['work_oriented'])
    row.append(data[0]['receptiviti_scores']['raw_scores']['workhorse'])

    # Percentile Scores
    row.append(data[0]['receptiviti_scores']['percentiles']['achievement_driven'])
    row.append(data[0]['receptiviti_scores']['percentiles']['adjustment'])
    row.append(data[0]['receptiviti_scores']['percentiles']['agreeable'])
    row.append(data[0]['receptiviti_scores']['percentiles']['body_focus'])
    row.append(data[0]['receptiviti_scores']['percentiles']['cold'])
    row.append(data[0]['receptiviti_scores']['percentiles']['conscientious'])
    row.append(data[0]['receptiviti_scores']['percentiles']['depression'])
    row.append(data[0]['receptiviti_scores']['percentiles']['extraversion'])
    row.append(data[0]['receptiviti_scores']['percentiles']['family_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['food_focus'])
    row.append(data[0]['receptiviti_scores']['percentiles']['friend_focus'])
    row.append(data[0]['receptiviti_scores']['percentiles']['happiness'])
    row.append(data[0]['receptiviti_scores']['percentiles']['health_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['impulsive'])
    row.append(data[0]['receptiviti_scores']['percentiles']['independent'])
    row.append(data[0]['receptiviti_scores']['percentiles']['insecure'])
    row.append(data[0]['receptiviti_scores']['percentiles']['leisure_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['money_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['netspeak_focus'])
    row.append(data[0]['receptiviti_scores']['percentiles']['neuroticism'])
    row.append(data[0]['receptiviti_scores']['percentiles']['openness'])
    row.append(data[0]['receptiviti_scores']['percentiles']['persuasive'])
    row.append(data[0]['receptiviti_scores']['percentiles']['power_driven'])
    row.append(data[0]['receptiviti_scores']['percentiles']['religion_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['reward_bias'])
    row.append(data[0]['receptiviti_scores']['percentiles']['sexual_focus'])
    row.append(data[0]['receptiviti_scores']['percentiles']['social_skills'])
    row.append(data[0]['receptiviti_scores']['percentiles']['thinking_style'])
    row.append(data[0]['receptiviti_scores']['percentiles']['type_a'])
    row.append(data[0]['receptiviti_scores']['percentiles']['work_oriented'])
    row.append(data[0]['receptiviti_scores']['percentiles']['workhorse'])
    #print (row);
    return row


def write_json_text(js):
    json_str = json.dumps(js)
    with open("Analysis_json/all_result_json.txt", 'a', encoding="utf-8") as f:
        f.write(json_str + "\n")
    print("wrote the data to text file")

def write_error_list(user):
    with open("Analysis_json/error_list", 'a', encoding="utf-8") as f:
        f.write(user + "\n")
    print("wrote the data to error list file")

#Method to get the data from the XLSX file given in config file.
def extract_data_from_excel():

    # list to save all the twitter usernames of the Top Business Angels
    business_angels_list = []

    workbook = load_workbook(config.USERNAME_XLSX)
    first_sheet = workbook.get_sheet_names()[0]
    worksheet = workbook.get_sheet_by_name(first_sheet)

    #row_count = 1897  #worksheet.get_highest_row() - 1

    print("Fetching the username for %s from the Excel sheet" % config.PERSON)
    print("Please wait, this may take some time.")
    index = 0
    for row in range(config.MIX_ROW_SIZE,config.MAX_ROW_SIZE):
        for column in "H":
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
    print("Extracted all the usernames")
    return business_angels_list

def extract_data_from_csv():
    csv.register_dialect(
        'mydialect',
        delimiter=',',
        quotechar='"',
        doublequote=True,
        skipinitialspace=True,
        lineterminator='\r\n',
        quoting=csv.QUOTE_MINIMAL)

    first_item = []

    with open('Analysis_json/LIWC_results1.csv', 'r') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')
        for row in thedata:
            first_item.append(row[0])
    return first_item



#The main Program, entry point of the program
if __name__ == '__main__':

    #Create a file and include the header for Receptivity scores.
    writer = csv.writer(open("Analysis_json/Receptivity_scores_Forbes4002.csv", 'w'))
    writer.writerow(csv_header_receptivity)

    # Create a file and include the header for LIWC_scores
    writer = csv.writer(open("Analysis_json/LIWC_results_Forbes4002.csv", 'w'))
    writer.writerow(csv_header)

    all_LIWC_rows = []
    all_receptivity_rows = []


    # to get the user list from the Excel sheet
    user_list = extract_data_from_excel()

    # to get the user list from already downloaded data
    #extracted_user_list = extract_data_from_csv()

    # data for Receptivity API
    if apikey:
        header['X-API-KEY'] = apikey
    if apisecret:
        header['X-API-SECRET-KEY'] = apisecret
    header['Content-type'] = 'application/json'

    error_list = []

    # Process to clear the redunt user names after process.
    temp_list = list(user_list)

    #seen = set()
    #seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    #seen_twice = set(x for x in extracted_user_list if x in seen or seen_add(x))

    #print("Seen_twice in the extracted data: " )
    #print(list(seen_twice ))


    # To clean the list of already extraceted user details
    '''for user in user_list:
        for saved_user in extracted_user_list:
            if saved_user == user:
                temp_list.remove(saved_user)
                break'''


    print("user list : "+ str(len(user_list)))
    #print("Len_extracred_user_list : " + str(len(extracted_user_list)))
    print("temp list : " + str(len(temp_list)))



    # Process to create the clean list into batches
    batch_user_list = []
    small_list = []
    index = 0

    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print (temp_list)

    '''for user in temp_list:
        small_list.append(user)
        index = index + 1
        if ( index > 25):
            batch_user_list.append(small_list)
            small_list = []
            index = 0
    # to aappend the last set of user data
    batch_user_list.append(small_list)
    print("batch user list length " + str(len(batch_user_list)))'''

    count = 0



        #for user in user_list: #batch_user_list:
        #print("User :" + user)
        #for user in batch:
        #print("Extracting data for the user : " + user)

    twitter_handle = "jack"

        #manage the response of the user via the API
    response = import_twitter_user(twitter_import_user_api_url(BASEURL), header, twitter_handle)

    data = get_user_analysis_data(response)

    if (data == None):
        print("null")
        error_list.append(user)
        write_error_list(user)
    else:
        write_json_text(data)
        all_LIWC_rows.append(get_liwc_scores(data))
        all_receptivity_rows.append(get_receptiviti_scores(data))



        #to write the data onto the files (written as a batch of 25 usernames once)
    for row in all_LIWC_rows:
        writer = csv.writer(open("Analysis_json/LIWC_results_Forbes4002.csv", 'a'))
        writer.writerow(row)
    all_LIWC_rows = []
    print ("LIWC scores are written onto a file ")


    for row in all_receptivity_rows:
        writer = csv.writer(open("Analysis_json/Receptivity_scores_Forbes4002.csv", 'a'))
        writer.writerow(row)
    all_receptivity_rows = []
    print("Receptiviti scores are written onto a file")


    #count = count + 1
        #print("Batch number " + str(count) + " finished")
        #print("Sleeping now :)")
        #time.sleep(100)'''