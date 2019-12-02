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
    pos_counts = []
    for poem in poems:
        tagged_poem = nltk.pos_tag(poem)
        pos_counts.append(
            {'ADJ': 0, 'ADP': 0, 'ADV': 0, 'CONJ': 0, 'DET': 0, 'NOUN': 0, 'NUM': 0, 'NUM': 0, 'PRON': 0, 'VERB': 0})
