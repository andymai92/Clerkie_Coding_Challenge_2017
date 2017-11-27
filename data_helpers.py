import numpy as np
import re
import itertools
from collections import Counter
import pandas as pd


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    Modified to fit this exercise
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", "", string)
    string = re.sub(r"\'ve", "", string)
    string = re.sub(r"n\'t", "", string)
    string = re.sub(r"\'re", "", string)
    string = re.sub(r"\'d", "", string)
    string = re.sub(r"\'ll", "", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", "", string)
    string = re.sub(r"\)", "", string)
    string = re.sub(r"\?", "", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

## Initiate all variables that will be used in several files
user = pd.read_csv('./database/Mary.csv')
bank = list(open('./database/banks', "r").readlines())
bank = [clean_str(i) for i in bank]
budget = pd.read_csv('database/Mary_budget.csv')

def load_data_and_labels(cat_1, cat_2, cat_3):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    cat_1_examples = list(open(cat_1, "r").readlines())
    cat_1_examples = [s.strip() for s in cat_1_examples]
    cat_2_examples = list(open(cat_2, "r").readlines())
    cat_2_examples = [s.strip() for s in cat_2_examples]
    cat_3_examples = list(open(cat_3, "r").readlines())
    cat_3_examples = [s.strip() for s in cat_3_examples]
    # Split by words
    x_text = cat_1_examples + cat_2_examples + cat_3_examples
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    cat_1_labels = [[1, 0, 0] for _ in cat_1_examples]
    cat_2_labels = [[0, 1, 0] for _ in cat_2_examples]
    cat_3_labels = [[0, 0, 1] for _ in cat_3_examples]
    y = np.concatenate([cat_1_labels, cat_2_labels, cat_3_labels], 0)    
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
