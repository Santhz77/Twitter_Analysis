import json
import json
import csv
import os
import config

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


#The main Program, entry point of the program
if __name__ == '__main__':
    # Create a file and include the header for Receptivity scores.
    writer = csv.writer(open("Tech-company founders list/Receptivity_set1.csv", 'w'))
    writer.writerow(csv_header_receptivity)

    # Create a file and include the header for LIWC_scores
    writer = csv.writer(open("Tech-company founders list/LIWC_set1.csv", 'w'))
    writer.writerow(csv_header)

    index = 0
    receptivity_row = []
    try:
        # Open the file where json data is stored and then load the json file
        with open("Analysis_json/tech-company-founders.txt") as file:
            for each_line in file:
                parsed_json = json.loads(each_line.rstrip())
                #print(parsed_json)
                liwc_row = get_liwc_scores(parsed_json)
                writer = csv.writer(open("Tech-company founders list/LIWC_set1.csv", 'a'))
                writer.writerow(liwc_row)

                receptivity_row = get_receptiviti_scores(parsed_json)
                writer = csv.writer(open("Tech-company founders list/Receptivity_set1.csv", 'a'))
                writer.writerow(receptivity_row)

                index = index + 1
    except:
        with open("error_list_tech-company.txt", 'a') as f:
            f.write("Error occurred while getting data from file %s"  + "\n")
        print("Error is : " + str(sys.exc_info()[0]))

    print(str(index))