import nltk
import csv
import re


def read_from_csv(file):
    reader = csv.reader(file, delimiter=",")
    labels = []
    poems = []
    for row in reader:
        poems.append(row[0])
        labels.append(row[1])

    return poems, labels


def get_poem_label_pairs(poems):
    poem_list = poems.split("\n")
    poems_labels_list = []
    for poem in poem_list:
        poem_label = poem.split(",")
        poems_labels_list.append(poem_label)
    print(poems_labels_list)
    return poems_labels_list

# Returns a list of all poems in the format of a list of stanzas
# Pass in the list of poems
def split_stanzas(poems):
    poem_stanzas = []
    for poem in poems:
        poem_stanzas.append(re.split('\S {3}\S', poem))
    return poem_stanzas


# Returns list of average stanza length for each poem
def avg_stanza_len(poem_stanzas):
    avg_stnz_lens = []
    for poem in poem_stanzas:
        total_words = 0
        num_stanzas = 0
        for stanza in poem:
            total_words += len(stanza)
        avg_stnz_lens.append(total_words / len(poem))
    return avg_stnz_lens


# Returns ratio of unique words to total words in poem
def word_diversity(poem):
    # Make a running list of each unique word
    unique_words = []
    for word in poem:
        if word not in unique_words:
            unique_words.append(word)
    return len(unique_words) / len(poem)


def pos_counts(poems):
    pos_counts = []
    for poem in poems:
        tagged_poem = nltk.pos_tag(poem)
        pos_count = \
            {'ADJ': 0, 'ADP': 0, 'ADV': 0, 'CONJ': 0, 'DET': 0, 'NOUN': 0, 'NUM': 0, 'PRT': 0, 'PRON': 0, 'VERB': 0}

        for word in tagged_poem:
            pos_count[word[1]] += 1

        pos_counts.append(pos_count)

    return pos_counts


def main():
    file = open("short_poems.csv", 'r')
    if file.mode == 'r':
        contents = file.read()
    poems_labels = get_poem_label_pairs(contents)


main()