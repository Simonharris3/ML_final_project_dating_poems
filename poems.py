import nltk
import csv
import re

# def read_from_csv(file):
#     reader = csv.reader(file, delimiter=",")
#     labels = []
#     poems = []
#     for row in reader:
#         poems.append(row[0])
#         labels.append(row[1])
#
#     return poems, labels


def get_poem_label_pairs(poems):
    poem_list = poems.split("\n")
    poems_labels_list = []
    for poem in poem_list:
        poem_label = poem.split(",")
        poems_labels_list.append(poem_label)
    # print(poems_labels_list)
    return poems_labels_list


# Returns a list of all poems in the format of a list of stanzas
# Pass in the list of poems
def split_stanzas(poems):
    poem_stanzas = []
    for poem in poems:
        poem_stanzas.append(re.split('[^\s]\s{3}[^\s]', poem))
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
def get_word_diversity(poems):
    # Make a running list of each unique word
    word_diversities = []
    for poem in poems:
        unique_words = []
        for word in poem:
            if word not in unique_words:
                unique_words.append(word)
        word_diversities.append(len(unique_words) / len(poem))
    return word_diversities


# returns the counts of each part of speech in the poems, as determined by the nltk pos tagger
def pos_counts(poems):
    part_of_speech_counts = []
    for poem in poems:
        tagged_poem = nltk.pos_tag(poem)
        pos_count = \
            {'ADJ': 0, 'ADP': 0, 'ADV': 0, 'CONJ': 0, 'DT': 0, 'NN': 0, 'NUM': 0, 'PRT': 0, 'PRON': 0, 'VBZ': 0}

        for word in tagged_poem:
            pos_count[word[1]] += 1

        for pos in pos_count:
            pos_count[pos] /= len(poem)

        part_of_speech_counts.append(pos_count)

    return pos_counts


def get_num_stanzas(poem_stanzas):
    num_stanzas = []
    for poem in poem_stanzas:
        num_stanzas.append(len(poem))
    return num_stanzas


def get_poem_lens(poems):
    poem_lens = []
    for poem in poems:
        poem_lens.append(len(poem))
    return poem_lens


def get_avg_word_lens(poems):
    poem_words = []
    avg_word_lens = []
    for poem in poems:
        poem_words = re.split("\s",poem)
        total_letters = 0
        for word in poem_words:
            total_letters += len(word)
        avg_word_lens.append(total_letters/len(poem_words))
    return avg_word_lens


def main():
    file = open("short_poems.csv", 'r')
    if file.mode == 'r':
        contents = file.read()
    poem_label_pair_list = get_poem_label_pairs(contents)

    poem_texts = []
    for poem in poem_label_pair_list:
        poem_texts.append(poem[0])

    poem_stanzas = split_stanzas(poem_texts)

    # for poem1 in poem_stanzas:
    #     for stanza in poem1:
    #         print("stanza: " + stanza)
    #     print("\nNEW POEM:")

    avg_stnz_lens = avg_stanza_len(poem_stanzas)
    print("Avg Stanza Len: " + str(avg_stnz_lens))
    num_stanzas = get_num_stanzas(poem_stanzas)
    print("Num Stanzas: " + str(num_stanzas))
    unique_word_ratios = get_word_diversity(poem_texts)
    print("Word Diversity: " + str(unique_word_ratios))
    print("Poem word counts: " + str(get_poem_lens(poem_texts)))
    print("Average word lengths: " + str(get_avg_word_lens(poem_texts)))
    #print("Pos counts: " + str(pos_counts(poem_texts)))


    nltk.download('averaged_perceptron_tagger')
    parts_of_speech = pos_counts(poem_texts)
    print(parts_of_speech)

main()
