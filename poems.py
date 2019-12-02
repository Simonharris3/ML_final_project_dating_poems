import nltk
import csv
import re

def read_from_csv(file):
    reader = csv.reader(file, delimiter=",")

# Returns a list of all poems in the format of a list of stanzas
# Pass in the list of poems
def split_stanzas(poems):
    poem_stanzas = []
    for poem in poems:
        poem_stanzas.append(re.split('\S   \S', poem))
    return poem_stanzas


# Returns list of average stanza length for each poem
def avg_stanza_len(poem_stanzas):
    avg_stnz_lens = []
    for poem in poem_stanzas:
        total_words = 0
        num_stanzas = 0
        for stanza in poem:
            total_words += len(stanza)
        avg_stnz_lens.append(total_words/len(poem))
    return avg_stnz_lens

# Returns ratio of unique words to total words in poem
def word_diversity(poem):
    # Make a running list of each unique word
    unique_words = []
    for word in poem:
        if word not in unique_words:
            unique_words.append(word)
    return len(unique_words)/len(poem)

def get_length():
    labels = []
    poems = []
    for row in reader:
        poems.append(row[0])
        labels.append(row[1])

    return poems, labels


def pos_counts(poems):
