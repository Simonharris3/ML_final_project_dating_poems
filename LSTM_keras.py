#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 02:48:42 2019

@author: liujiachen
"""
import StemmingUtil
import math
import os
import sys
import random
import time 
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from pprint import pprint 
import copy
import nltk
from nltk.corpus import stopwords
from string import punctuation
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint

def split_data(data, tr_size, val_size, seed):
    """Divides into a training set, validation set, and test set.
    tr_size is % of total to make the training set, and val_size is % of the remainder to make the validation set.
    Returns the training, validation, and test sets as pandas dataframes. """
    tr_set = data.sample(frac=tr_size, random_state=seed) #get a train set from data
    remain_data = data.drop(tr_set.index).reset_index(drop=True) #drop train set rows from data and reset remain_data index
    tr_set = tr_set.reset_index(drop=True) #reset train set index
    val_set = remain_data.sample(frac=(val_size*data.shape[0])/remain_data.shape[0], random_state=seed) #get a val set from remain set
    test_set = remain_data.drop(val_set.index).reset_index(drop=True) #remove val set rows from remain set to obtain test set and reset test set index 
    val_set = val_set.reset_index(drop=True)
    return tr_set, val_set, test_set

def recall(confusion_matrix,labels):
    recall_dict = {}
   
    for l in labels:
        idx = labels.index(l)
        numerator=confusion_matrix[idx][idx]
        if numerator == 0:
            recall = 0
        else:
            recall = confusion_matrix[idx][idx]/(sum(confusion_matrix[idx]))
        print("recall for "+str(l),recall)
        recall_dict[l]=recall
    best_recall = max(recall_dict, key = recall_dict.get)
    print("best recall",best_recall)
    worst_recall = min(recall_dict, key = recall_dict.get)
    print("worst recall",worst_recall)
    
def precision(confusion_matrix,labels):
    precision_dict = {}
    for l in labels:
        idx = labels.index(l)
        numerator=confusion_matrix[idx][idx]
        if numerator == 0:
            precision = 0
        else:
            precision = confusion_matrix[idx][idx]/(sum([confusion_matrix[row][idx]for row in range(len(confusion_matrix))]))
        print("precision for "+str(l),precision)
        precision_dict[l] = precision
    best_precision=max(precision_dict,key=precision_dict.get)
    print("best precision", best_precision)
    worst_precision=min(precision_dict,key=precision_dict.get)
    print("worst precision", worst_precision)
    
def print_matrix_CI(path,labels,confusion_matrix,test_accuracy,test_set):
    #print out confusion matrix    
    [print(l, end=", ") for l in labels] #print out all predicted labels
    print()
    #print out results with actual label
    for r in range(0, len(confusion_matrix)):
        [print(l, end=", ") for l in confusion_matrix[r]]
        print(labels[r])
        
    file_name = path.split("/")[-1]
    file_name = file_name.split(".csv")[0]
    
    
    outputfile = "./results_"+"LSTM_keras_"+file_name+".csv"
    
    with open(outputfile, mode='w',newline='') as out:
        writer = csv.writer(out)
    
        writer.writerow([l for l in labels]+[""])
        for r in range(0, len(confusion_matrix)):
            writer.writerow([(str(l)) for l in confusion_matrix[r]]+[labels[r]])
    
    p = test_accuracy
    #print("accuracy",test_accuracy)
    n= test_set.shape[0] #number of test cases
    CI = [p - 2.24*((p*(1-p)/n))**0.5,p + 2.24*((p*(1-p)/n))**0.5]
    print("CI",CI) 


def main():
    
    start = time.time()
    seed = 30
    random.seed(seed)
    np.random.seed(seed)
    train_percent = 0.7
    val_percent = 0.15
    
    words_to_remove =  ["\n","\s"]
    
    path = "poems_reordered_further_cleaned.csv"
    
    df = pd.read_csv(path)
    
    
    
    
    #shuffle dataset
    df = df.sample(frac=1, random_state = seed).reset_index(drop=True)
    
    
    
    all_words =[]
    
    
    count = 0
    for i in range (0, df.shape[0]):
        line = df.iloc[i,1]
        
        
        
        words = StemmingUtil.parseTokens(line)
        words=[w for w in words if w not in words_to_remove]
        newline = " ".join(words)
        df.iloc[i,1] = newline
        count += len(words)
        
        #print(len(words))
        
        
            
        
        all_words = all_words + words
        
    average_len = int(count/df.shape[0])    
    all_words = set(all_words)
    vocab_size = len(all_words)
    
    #print(max_length)
    
    max_length = 500
    
    
    
    train_set,val_set, test_set = split_data(df,train_percent,val_percent,seed)
    
    print("train_set shape:",train_set.shape)
    print("test_set shape:",test_set.shape)
    print("val_set shape:",val_set.shape)
    
    
    
    
    train_set = train_set.to_numpy()
    test_set = test_set.to_numpy()
    val_set = val_set.to_numpy()
    dataset = df.to_numpy()
    
    labels = list(np.unique(dataset[:,0]))
    num_label = len(labels)
    
    X_train = train_set[:,1:]
    Y_train = train_set[:,0]
    
    
    
    dummy_Y_train = np.zeros((Y_train.shape[0],num_label))
    for i in range(0,Y_train.shape[0]):
        idx = labels.index(Y_train[i])
        dummy_Y_train[i,idx]=1
        
 
    
    
    

    X_test = test_set[:,1:]
    Y_test = test_set[:,0]
    
    dummy_Y_test = np.zeros((Y_test.shape[0],num_label))
    for i in range(0,Y_test.shape[0]):
        idx = labels.index(Y_test[i])
        dummy_Y_test[i,idx]=1
        
        
        
        
    X_val = val_set[:,1:]
    Y_val = val_set[:,0]
    
    dummy_Y_val = np.zeros((Y_val.shape[0],num_label))
    for i in range(0,Y_val.shape[0]):
        idx = labels.index(Y_val[i])
        dummy_Y_val[i,idx]=1
    
    #one hot encode the words
    
    X_train = [one_hot(line[0], vocab_size) for line in X_train]
    
    X_test = [one_hot(line[0], vocab_size) for line in X_test]
    
    X_val = [one_hot(line[0], vocab_size) for line in X_val]
    
  
    
    
    
       
    #padding
    
    X_train = pad_sequences(X_train, maxlen=max_length, padding='post')
    
    X_test = pad_sequences(X_test, maxlen=max_length, padding='post')
    
    X_val = pad_sequences(X_val, maxlen=max_length, padding='post')
    
    
 
    model = tf.keras.Sequential()
    #Typical nnlm models on google hub have the embedding size of 128.
    #embedding layer is the first layer
    #number of neurons in the embedding layer equals to the number of values in the encoded vector obtained from embedding, i.e. number of words
    #input_length is how many words/units you want to embed 
    model.add(layers.Embedding(vocab_size, 128, input_length=max_length))
    model.add(layers.LSTM(512, dropout=0.5, recurrent_dropout=0.5,return_sequences=True)) #output_dim is the number of neurons in the recurrent layer #256 neurons
    model.add(layers.LSTM(512, dropout=0.5, recurrent_dropout=0.5,return_sequences=True))
    model.add(layers.LSTM(512, dropout=0.5, recurrent_dropout=0.5))
    model.add(layers.Dense(num_label, activation='softmax'))
    model.compile(optimizer=tf.keras.optimizers.Adam(0.01),loss='categorical_crossentropy',metrics=['accuracy'])
    
    callbacks = [EarlyStopping(monitor='val_loss', patience=50),
             ModelCheckpoint(filepath='best_LSTM_keras.h5', monitor='val_loss', save_best_only=True)]
    
    
    
   
    history=model.fit(X_train, dummy_Y_train, epochs=500, callbacks=callbacks,batch_size=128,validation_data = (X_val,dummy_Y_val))
    
    
    #run test set
    confusion_matrix = [[0]*num_label for m in range(0,num_label)]
    
    for instance in range(0, test_set.shape[0]): #iterate over test cases
        inputs = X_test[instance,:]
        
        
        
        target = dummy_Y_test[instance,:]
        
        
       
        
        
        prediction = model.predict_classes(inputs.reshape(1, max_length),batch_size=None,verbose=0)
        
        
        
        iactual = np.where(target==1)[0][0] #row index
        ipredict = prediction[0] #column index
        confusion_matrix[iactual][ipredict] += 1
    
    n_accurate_test=sum([confusion_matrix[idx][idx] for idx in range(len(confusion_matrix))])
    
    test_accuracy = n_accurate_test/test_set.shape[0]
    print("test accuracy", test_accuracy)
    
    print_matrix_CI(path,labels,confusion_matrix,test_accuracy,test_set)
    
    recall(confusion_matrix,labels)  
    
    precision(confusion_matrix,labels)
    
    
    end = time.time()
    
    print("run time", (end-start)/60,"min")

main()