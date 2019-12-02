import nltk
import csv

def read_from_csv(file):
    reader = csv.reader(file, delimiter=",")

    labels = []
    poems = []
    for row in reader:
        poems.append(row[0])
        labels.append(row[1])

    return poems, labels

def pos_counts(poems):
