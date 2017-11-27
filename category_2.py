import numpy as np
import pandas as pd
import data_helpers
import datetime


budget = data_helpers.budget
monthly_budget = budget['income'].iloc[0] - (budget['rent'].iloc[0] 
	+ budget['utility'].iloc[0] + budget['shopping'].iloc[0] + budget['restaurant'].iloc[0])

def suggestionSaving(shopping_percentage, restaurant_percentage):
    suggestion = budget['income'].iloc[0] - (budget['rent'].iloc[0] + budget['utility'].iloc[0] + shopping_percentage*budget['shopping'].iloc[0]
                                            + restaurant_percentage*budget['restaurant'].iloc[0])
    return suggestion

def main():
	print('\n\n\n')
	print('------------------------------------------------')
	print('------------------------------------------------')
	if monthly_budget > 0:
	    print('Congratulations! This month you save ${}'.format(monthly_budget))
	    print('If you keep spending like this, you will save in total of ${} from now to the end of {}.'.format((12 - datetime.date.today().month + 1)*monthly_budget, datetime.date.today().year))
	elif monthly_budget == 0:
	    print("It seems that you spent all your earnings this month. No worries! Let's save more next month!")
	else:
	    print('Oops... this month you spent more than your earnings!')
	    print('Your budget is now -${}'.format(monthly_budget*-1))
	    print('>>>>>>>>>>>>><<<<<<<<<<<<<<<')
	    print('Do you need my suggestion to save more for the next month?')
	    suggest = input("Please type 'yes' or 'no': ").lower()
	    suggest_flag = False
	    if suggest == 'yes':
	        suggest_flag = True
	    if suggest_flag:
	        print('You are now spending more for shopping and restaurant.')
	        print(' + Suggestion 1:')
	        print('\tIf you reduce 55% your budget for shopping, you can save ${} each month.'.format(suggestionSaving(0.45,1)))
	        print(' + Suggestion 2:')
	        print('\tIf you reduce 60% your budget for shopping, you can save ${} each month.'.format(suggestionSaving(0.4,1)))
	        print(' + Suggestion 3:')
	        print('\tIf you reduce 40% your budget for shopping and 30% for restaurant, you can save ${} each month.'.format(suggestionSaving(0.4,1)+suggestionSaving(0.6,0.7)))
