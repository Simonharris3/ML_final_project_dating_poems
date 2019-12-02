

<<<<<<< HEAD
# Returns a list of all poems in the format of a list of stanzas
# Pass in the list of poems
def split_stanzas(poems):
    poem_stanzas = []
    for poem in poems:
        poem_stanzas.append(re.split('\S   \S', poem))
    return poem_stanzas

# Returns ratio of unique words to total words in poem
def word_diversity(poem):
    # Make a running list of each unique word
    unique_words = []
    for word in poem:
        if word not in unique_words:
            unique_words.append(word)

    return len(unique_words)/len(poem)

def get_length()
=======

>>>>>>> e02f6888489f884a48d9debe1819b77e76eec628
