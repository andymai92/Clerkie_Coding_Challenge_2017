#! /usr/bin/env python

from nltk.corpus import stopwords
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from text_cnn import TextCNN
from tensorflow.contrib import learn

# Parameters
# ==================================================

# Data loading params
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("cat_1", "./database/1", "Data source for Category 1")
tf.flags.DEFINE_string("cat_2", "./database/2", "Data source for Category 2")
tf.flags.DEFINE_string("cat_3", "./database/3", "Data source for Category 3")

# # Model Hyperparameters
# tf.flags.DEFINE_integer("embedding_dim", 80, "Dimensionality of character embedding (default: 80)")
# tf.flags.DEFINE_string("filter_sizes", "2,3,4", "Comma-separated filter sizes (default: '2,3,4')")
# tf.flags.DEFINE_integer("num_filters", 80, "Number of filters per filter size (default: 80)")
# tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
# tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# # Training parameters
# tf.flags.DEFINE_integer("batch_size", 2, "Batch Size (default: 2)")
# tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
# tf.flags.DEFINE_integer("evaluate_every", 20, "Evaluate model on dev set after this many steps (default: 20)")
# tf.flags.DEFINE_integer("checkpoint_every", 20, "Save model after this many steps (default: 20)")
# tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")
# # Misc Parameters
# tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
# tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

# tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
# print("\nParameters:")
# for attr, value in sorted(FLAGS.__flags.items()):
#     print("{}={}".format(attr.upper(), value))
# print("")


# Data Preparation
# ==================================================

# Load data
print("Loading data...")
x_text, y = data_helpers.load_data_and_labels(FLAGS.cat_1, FLAGS.cat_2, FLAGS.cat_3)

# Build vocabulary
max_document_length = max([len(x.split(" ")) for x in x_text]) - 1
# vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
# x = np.array(list(vocab_processor.fit_transform(x_text)))

# ## Extract word:id mapping from the object.
# vocab_dict = vocab_processor.vocabulary_._mapping

# ## Sort the vocabulary dictionary on the basis of values(id).
# ## Both statements perform same task.

# sorted_vocab = sorted(vocab_dict.items(), key = lambda x : x[1])

# ## Treat the id's as index into list and create a list of words in the ascending order of id's
# ## word with id i goes at index i of the list.
# vocabulary = list(list(zip(*sorted_vocab))[0])

# print(vocabulary)
# print(x)

############################################################################
print('========================')

x_raw = []
input_string = input('Type your request: ')
x_raw.append(input_string.lower())
x_raw = [word for word in x_raw if word not in stopwords.words('english')]
print(x_raw)
vocab_path = os.path.join('./runs/1511133445/vocab')
vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)

## Extract word:id mapping from the object.
vocab_dict = vocab_processor.vocabulary_._mapping

## Sort the vocabulary dictionary on the basis of values(id).
## Both statements perform same task.

sorted_vocab = sorted(vocab_dict.items(), key = lambda x : x[1])

## Treat the id's as index into list and create a list of words in the ascending order of id's
## word with id i goes at index i of the list.
vocabulary = list(list(zip(*sorted_vocab))[0])

print(vocabulary)

x_test = np.array(list(vocab_processor.transform(x_raw)))
x_test = np.unique(x_test, axis=1)
# print(x_test)

# for element in x_test:
# 	non_zero = np.count_nonzero(element)
# 	if non_zero <= int(0.3*max_document_length):
# 		print("Not OK - Belongs to other classes")
# 	else:
# 		print("OK")