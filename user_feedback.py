import numpy as np
import pandas as pd
import data_helpers
from nltk.corpus import stopwords
import subprocess


def textProcessing(input_text):	
    processed_text = ''
    ## We process the raw text to eliminate unnecessary information such as banking information
    for i in input_text:
        if not ('0' <= i <= '9'):
        	processed_text += i
    processed_text = data_helpers.clean_str(processed_text).split()
    ## Remove all stop words in raw text
    processed_text = [word for word in processed_text if word not in stopwords.words('english')]
    result = ' ',join(processed_text)
    return result

def userFeedback(input_text):
    print('\n')
    print('*****************')
    print('>>>Am I right?<<<')
    print("'1' - Correct \t '2' - Not correct \t '3' - Skip")
    feedback = input()
    if feedback == '1':
        print('Thank you for your cooperation. May I help you with anything else?')
    elif feedback == '2':
        print('>>> I am sorry for my misunderstanding your request <<<')
        print('Which category is your request?')
        print('\t1. Checking your balance in savings and checking accounts [1]')
        print('\t2. Checking your budget this month [2]')
        print('\t3. Calculating your affordability to buy a house [3]')
        cat_improve = input('Please type the category number here, then ENTER to improve my knowldge: ')      
        processed_text = textProcessing(input_text)
        if cat_improve == '1':
            cat_1 = open('./database/1', 'a')
            cat_1.write(processed_text + '\n')
        elif cat_improve == '2':
            cat_2 = open('./database/2', 'a')
            cat_2.write(processed_text + '\n')
        else:
            cat_3 = open('./database/3', 'a')
            cat_3.write(processed_text + '\n')
        #subprocess.call(['python3', './train.py'])
        print('\n\n')
        print('**************************************')
        print('Thank you so much for your indication. All your correction has been saved to improve next time results.')
        print('**************************************')