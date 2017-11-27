#! /usr/bin/env python

from nltk.corpus import stopwords
import tensorflow as tf
import numpy as np
import pandas as pd
import os
import time
import datetime
import data_helpers
import category_1
import category_2
import category_3
import user_feedback
from text_cnn import TextCNN
from tensorflow.contrib import learn
import csv

# Parameters
# ==================================================

# Data Parameters
tf.flags.DEFINE_string("cat_1", "./database/1", "Data source for Category 1")
tf.flags.DEFINE_string("cat_2", "./database/2", "Data source for Category 2")
tf.flags.DEFINE_string("cat_3", "./database/3", "Data source for Category 3")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 2, "Batch Size (default: 2)")
tf.flags.DEFINE_string("checkpoint_dir", "./runs/built_model/checkpoints", "Checkpoint directory from training run")
# tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()


# Load data from keyboard:
while(True):
    input_text = input("Please type your request, type 'exit' to quit: ")
    input_text = input_text.lower()
    if input_text == 'exit':
        print('Goodbye! Have a nice day!')
        break
    x_raw = []
    x_raw.append(input_text)
    x_raw = [word for word in x_raw if word not in stopwords.words('english')]

    ## Map data into vocabulary
    vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))
    check_valid_input = np.unique(x_test, axis=1)

    ## Extract word:id mapping from the object.
    vocab_dict = vocab_processor.vocabulary_._mapping

    ## Sort the vocabulary dictionary on the basis of values(id).
    ## Both statements perform same task.

    sorted_vocab = sorted(vocab_dict.items(), key = lambda x : x[1])

    ## Treat the id's as index into list and create a list of words in the ascending order of id's
    ## word with id i goes at index i of the list.
    vocabulary = list(list(zip(*sorted_vocab))[0])
    x_text, y = data_helpers.load_data_and_labels(FLAGS.cat_1, FLAGS.cat_2, FLAGS.cat_3)

    # Build vocabulary
    max_document_length = max([len(x.split(" ")) for x in x_text])
    print('------------------------------------------------')
    for element in check_valid_input:
        non_zero = np.count_nonzero(element)
        if non_zero <= int(0.1*max_document_length):
            print("I am sorry, but I did not understand your request...")
            print('I am still learning so I can only help you with 3 things:')
            print('\t1. Checking your bank account balance.')
            print('\t2. Checking your budget this month.')
            print('\t3. Checking your affordability to buy a house.')
        else:
            checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
            graph = tf.Graph()
            with graph.as_default():
                session_conf = tf.ConfigProto(
                  allow_soft_placement=FLAGS.allow_soft_placement,
                  log_device_placement=FLAGS.log_device_placement)
                sess = tf.Session(config=session_conf)
                with sess.as_default():
                    # Load the saved meta graph and restore variables
                    saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
                    saver.restore(sess, checkpoint_file)

                    # Get the placeholders from the graph by name
                    input_x = graph.get_operation_by_name("input_x").outputs[0]
                    
                    dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                    # Tensors we want to evaluate
                    predictions = graph.get_operation_by_name("output/predictions").outputs[0]

                    # Generate batches for one epoch
                    batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

                    # Collect the predictions here
                    all_predictions = []

                    for x_test_batch in batches:
                        batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                        all_predictions = np.concatenate([all_predictions, batch_predictions])
            all_predictions = int(all_predictions[0])

            if all_predictions == 0:  ## Request belongs to Category 01          
                category_1.main(input_text)
                user_feedback.userFeedback(input_text)            
            elif all_predictions == 1: ## Request belongs to Category 02
                category_2.main()
                user_feedback.userFeedback(input_text)            
            elif all_predictions == 2: ## Request belongs to Category 03
                check = category_3.main(input_text)
                if check:
                    user_feedback.userFeedback(input_text)