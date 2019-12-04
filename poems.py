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


def write_atts_to_csv(labels, unique_word_ratios, poem_lengths, avg_word_lens, parts_of_speech):
    filename = 'poem_attributes.csv'
    file = open(filename, 'w')

    file.write("Century,Word Diversity,Number of Words,Average Word Length,Number of Adjectives,Number of Adpositions,"
               "Number of Adverbs,Number of Conjunctions,Number of Determiners,Number of Nouns,Number of Numerals,"
               "Number of Particles,Number of Pronouns,Number of Verbs\n")

    for i in range(len(labels)):
        file.write(str(labels[i]) + ',' + str(unique_word_ratios[i]) + ',' + str(poem_lengths[i]) + ',' +
                   str(avg_word_lens[i]) + ',' + str(parts_of_speech[i]['ADJ']) + ',' + str(parts_of_speech[i]['ADP'])
                   + ',' + str(parts_of_speech[i]['ADV']) + ',' + str(parts_of_speech[i]['CONJ']) + ',' +
                   str(parts_of_speech[i]['DET']) + ',' + str(parts_of_speech[i]['NOUN']) + ',' +
                   str(parts_of_speech[i]['NUM']) + ',' + str(parts_of_speech[i]['PRT']) + ',' +
                   str(parts_of_speech[i]['PRON']) + ',' + str(parts_of_speech[i]['VERB']) + ',\n')

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
    pos_proportion = []
    c = 0
    for poem in poems:
        tagged_poem = nltk.pos_tag(poem, tagset='universal')

        if c == 359:
            print("Tagged poem: " + str(tagged_poem))

        pos_count = {'ADJ': 0, 'ADP': 0, 'ADV': 0, 'CONJ': 0, 'DET': 0,
                     'NOUN': 0, 'NUM': 0, 'PRT': 0, 'PRON': 0, 'VERB': 0, 'X': 0, '.': 0}

        for word in tagged_poem:
            nltk_tag = word[1]
            # pos = condense_pos(nltk_tag)
            pos_count[nltk_tag] += 1

        for pos in pos_count:
            pos_count[pos] /= len(poem)

        pos_proportion.append(pos_count)

        c += 1

    return pos_proportion


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
    # poem_words = []
    avg_word_lens = []
    for poem in poems:
        total_letters = 0
        for word in poem:
            total_letters += len(word)
        avg_word_lens.append(total_letters/len(poem))
    return avg_word_lens


def main():
    file = open("short_poems.csv", 'r')
    if file.mode == 'r':
        contents = file.read()
    poem_label_pair_list = get_poem_label_pairs(contents)

    labels = []
    poem_texts = []
    for poem in poem_label_pair_list:
        poem_texts.append(poem[0])
        labels.append(poem[1])

    poem_words = []

    for poem in poem_texts:
        word_list = re.split("\s+", poem)
        last_item = word_list[len(word_list) - 1]
        if len(last_item) == 0:
            word_list.remove(last_item)
        poem_words.append(word_list)

    # poem_stanzas = split_stanzas(poem_texts)

    # for poem1 in poem_stanzas:
    #     for stanza in poem1:
    #         print("stanza: " + stanza)
    #     print("\nNEW POEM:")

    # avg_stnz_lens = avg_stanza_len(poem_stanzas)
    # print("Avg Stanza Len: " + str(avg_stnz_lens))
    # num_stanzas = get_num_stanzas(poem_stanzas)
    # print("Num Stanzas: " + str(num_stanzas))
    unique_word_ratios = get_word_diversity(poem_words)
    print("Word Diversity: " + str(unique_word_ratios))
    poem_lengths = get_poem_lens(poem_words)
    print("Poem word counts: " + str(poem_lengths))
    avg_word_lens = get_avg_word_lens(poem_words)
    print("Average word lengths: " + str(avg_word_lens))
    #print("Pos counts: " + str(pos_counts(poem_texts)))
    parts_of_speech = pos_counts(poem_words)
    print("Parts of speech: " + str(parts_of_speech[359]))

    write_atts_to_csv(labels, unique_word_ratios, poem_lengths, avg_word_lens, parts_of_speech)

main()
