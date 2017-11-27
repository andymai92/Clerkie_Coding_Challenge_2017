import numpy as np
import pandas as pd
import data_helpers

user = data_helpers.user
bank = data_helpers.bank

def printBalanceWithoutAccNum(bank_name, savings, checking, user): ## To display balance from all bank accounts without account ending numbers
    official_name = ''
    account_number = 0        
    if bank_name == 'boa':
        official_name = 'Bank of America'
    else:
        official_name = 'JPMorgan Chase'    
    if checking:
        index_checking_bank_name = user.index[user['checking_bank'] == bank_name].tolist()
        if len(index_checking_bank_name) == 0:
            print("You don't have any checking account at {}".format(official_name))
        else:
            for i in index_checking_bank_name:            
                if np.isnan(user['checking_acc'].iloc[i]):
                    account_number = ''
                else:
                    account_number = 'ending in x' + str(int(user['checking_acc'].iloc[i])) + ' '
                print('Your balance at {} checking account {}is: ${}'.format(official_name, account_number, user['checking_amount'].iloc[i]))
    if savings:
        index_savings_bank_name = user.index[user['saving_bank'] == bank_name].tolist()
        if len(index_savings_bank_name) == 0:
            print("You don't have any savings account at {}".format(official_name))
        else:
            for i in index_savings_bank_name:
                if np.isnan(user['saving_acc'].iloc[i]):
                    account_number = ''
                else:
                    account_number = 'ending in x' + str(int(user['saving_acc'].iloc[i])) + ' '
                print('Your balance at {} savings account {}is: ${}'.format(official_name, account_number, user['saving_amount'].iloc[i]))

def main(input_text):
	print('\n\n\n')
	checking = False
	savings = False
	for i in input_text.split(): ## Understand user requests information about either checking or savings account(s)
	    if i == 'checking' or i == 'checkings':
	        checking = True
	    elif i == 'saving' or i == 'savings' or i == 'save' or i == 'saved':
	        savings = True

	bank_name = [] 
	bankName = False
	for word in bank: ## Get all the bank names from request
	    if word in input_text:
	        bank_name.append(word)
	        bankName = True        
	        
	for i in range(len(bank_name)): ## Recognize BoA and Bank of America are the same bank
	    if bank_name[i] == 'bank of america':
	        bank_name[i] = 'boa'

	acc_num = []
	accNum = False
	four_digit_ending = ''
	j = 4
	for i in input_text: ## Get the account ending numbers from request
	    if j > 0:
	        if '0' <= i <= '9':
	            four_digit_ending += i
	            j -= 1            
	            accNum = True            
	acc_num.append(four_digit_ending)
	print('------------------------------------------------')
	print('------------------------------------------------')
	if not accNum: ## User does not mention about account number
	    if not(savings or checking): ## Request does not mention checking/savings account
	        if bankName: ## Request mentions about Bank Name
	            for i in bank_name:               
	                printBalanceWithoutAccNum(i, True, True, user)                
	        else: ## Request does not mention about Bank Name
	            print('These are your current bank accounts balance:')
	            print('\t- Bank of America:')
	            print('\t\t+ Checking account ending in x{}: ${}'.format(int(user['checking_acc'].iloc[0]), user['checking_amount'].iloc[0]))
	            print('\t\t+ Savings account: ${}'.format(user['saving_amount'].iloc[0]))
	            print('\t- JPMorgan Chase:')
	            print('\t\t+ Savings account ending in x{}: ${}'.format(int(user['saving_acc'].iloc[1]), user['saving_amount'].iloc[1]))
	            print('**In total, you have: ${}'.format(user['checking_amount'].iloc[0]+user['saving_amount'].iloc[0]+user['saving_amount'].iloc[1]))

	    elif savings == True and checking == False: ## Request mentions about savings account only
	        if bankName: ## Request also mentions about Bank Name
	            for i in bank_name:
	                printBalanceWithoutAccNum(i, True, False, user)
	        else: ## Request does not mention about Bank Name
	            print('Your balance in Bank of America savings account is: ${}'.format(user['saving_amount'].iloc[0]))
	            print('Your balance in JPMorgan Chase savings account ending in x{} is: ${}'.format(int(user['saving_acc'].iloc[1]), user['saving_amount'].iloc[1]))

	    elif savings == False and checking == True: ## Request mentions about checking account only
	        if bankName:
	            for i in bank_name:
	                printBalanceWithoutAccNum(i, False, True, user)
	        else:
	            print('Your balance in Bank of America checking account ending in x{} is: ${}'.format(int(user['checking_acc'].iloc[0]), user['checking_amount'].iloc[0]))

	    else:
	        print('I am sorry, currently I can handle single request only. Thank you!')
	        
	else: ## User mentions about account number
	    if not bankName:
	        for i in acc_num:
	            num = int(i)
	            if (num not in user['checking_acc'].unique()) or (num not in user['saving_acc'].unique()):
	                print('I am sorry, there is no account ending in x{} in database'.format(num))
	            else:
	                print('The balance in your checking account ending in x{} in Bank of America is: ${}'.format(num, user['checking_amount'].iloc[0]))
	                print('The balance in your savings account ending in x{} in JPMorgan Chase is: ${}'.format(num, user['saving_amount'].iloc[1]))
	    else:       
	        for i in acc_num:
	            num = int(i)           
	            if (num not in user['checking_acc'].unique()) or (num not in user['saving_acc'].unique()):
	                print('I am sorry, there is no account ending in x{} in database'.format(num))
	            else:               
	                for i in bank_name:
	                    if i == 'boa':
	                        print('The balance in your checking account ending in x{} in Bank of America is: ${}'.format(num, user['checking_amount'].iloc[0]))
	                    else:
	                        print('The balance in your savings account ending in x{} in JPMorgan Chase is: ${}'.format(num, user['saving_amount'].iloc[1]))
	            