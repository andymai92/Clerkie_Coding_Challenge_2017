import pandas as pd
import numpy as np
import data_helpers
import math

budget = data_helpers.budget
user = data_helpers.user
house_keyword = list(open('./database/house_synonyms', "r").readlines())
house_keyword = [data_helpers.clean_str(i) for i in house_keyword]

def housePriceCal(input_text):
    house_price = ''
    t = 1 ## suffix of numbers in million or thousand   
    for word in input_text.split():
        for j in range(len(word)):
            if '0' <= word[j] <= '9' or word[j] == '.':
                house_price += word[j]
                if j+1 <= len(word) - 1:
                    if word[j+1].lower() == 'm':
                        t = math.pow(10,6)
                    elif word[j+1].lower() == 'k':
                        t = math.pow(10,3)
        if word.lower() in ['million', 'millions']:
            t = math.pow(10,6)
        elif word.lower in ['thousand', 'thousands']:
            t = math.pow(10,3)
    house_price = float(house_price)*t
    return house_price

def monthlyMortgage(house_price): ## Calculate monthly mortgage that Mary needs to pay.
    remaining = 0.8 * house_price ## The amount need to lend from bank after 20% down-payment
    n = 30 * 12 ## Number of payments = 30 years * 12 months/year
    i = 0.05/12 ## monthly interest rate - 5% per year
    mortgage = round(remaining*((math.pow(1+i,n)*i)/(math.pow(1+i,n)-1)),2)
    return mortgage

def downPayment(house_price): ## Check if Mary can afford the 20% down-payment
    flag = True ## True means can afford, False means cannot afford
    down_payment = 0.2 * house_price
    balance = user['checking_amount'].iloc[0] + user['saving_amount'].iloc[0] + user['saving_amount'].iloc[1]
    if balance < down_payment:
        flag = False
    return flag

def main(input_text):
    print('\n\n\n')
    print('------------------------------------------------')
    print('------------------------------------------------')
    keyword_flag = False ## flag check if input text includes keyword related to 'house'
    for word in input_text.lower().split():
        word = data_helpers.clean_str(word)
        if word in house_keyword:
            keyword_flag = True
            break
    if keyword_flag:
        mortgage = monthlyMortgage(housePriceCal(input_text))
        if mortgage > 0.94*budget['income'].iloc[0]: ## Minimum $300 monthly credit-card payment is 6% of her income
            print('Oops... You cannot afford this house. The following details will explain:')
            print('------------------------')
            print('- Your monthly income is ${}'.format(budget['income'].iloc[0]))
            print('- Your minimum monthly credit-card payment is $300')
            print('- Every month you have ${} left'.format(budget['income'].iloc[0] - 300))
            print('- Monthly mortgage for this house is ${}'.format(mortgage))
            print('Conclusion: Monthly mortgage exceeds your monthly remaining. Therefore, you cannot afford this house.')
        elif not downPayment(housePriceCal(input_text)):
            print('Oops... You cannot afford this house. The following details will explain:')
            print('------------------------')
            print('- Your balance in bank accounts: ${}'.format(user['checking_amount'].iloc[0] + user['saving_amount'].iloc[0] + user['saving_amount'].iloc[1]))
            print('- You need to pay at least 20% down-payment, which is ${}'.format(0.2 * housePriceCal(input_text)))
            print('Conclusion: You are not able to pay 20% down-payment. Therefore, you cannot afford this house.')
        else:
            print('Congratulations! You are qualified for this monthly mortgage.')
            print('You need to pay ${} monthly for your dream house.'.format(mortgage))        
    else:
        print("I am sorry, but I did not understand your request...")
        print('I am still learning so I can only help you with 3 things:')
        print('\t1. Checking your bank account balance.')
        print('\t2. Checking your budget this month.')
        print('\t3. Checking your affordability to buy a house.')
    return keyword_flag
