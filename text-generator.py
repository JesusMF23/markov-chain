import random
import string
import re

# get inputs from user and validation
user_text = input('Please provide a random text for the generator:\n')

while True:
    user_length = input('Please specify desired number of words for the output text: \n')
    try:
        user_length = int(user_length)
        break
    except:
        print("Sorry, length must be an integer, pleace introduce the value again")

while True:
    user_order = input('Please specify desired order to improve context for the Markov Chain model: \n')
    try:
        user_order = int(user_order)
        break
    except:
        print("Sorry, order must be an integer, pleace introduce the value again")

# preprocessor of text to cleanse special characters
special_chars = re.escape(string.punctuation)

def preprocessor_text(user_text):
    user_text = re.sub('[^a-zA-Z0-9 \n\.]', '', user_text)
    user_text = re.sub('['+special_chars+']', '', user_text)

    return user_text

# clean the text provided by the user
user_text_cleaned = preprocessor_text(user_text).lower()

# generator of text using markov chains
def text_generator(user_text_cleaned, order=user_order, length=user_length):
    # obtaining a list of words from provided text
    words_list = user_text_cleaned.split()
    
    # storing markov chains with variables and states
    markov_chains = {}
    for i in range(len(words_list) - order):
        # we need to create combinations of context based on the order provided
        key = tuple(words_list[i:i+order])

        # we need to store the possible values for words
        if key in markov_chains:
            markov_chains[key].append(words_list[i+order])
        else:
            markov_chains[key] = [words_list[i+order]]
    
    # selecting a random starting point from the possible values
    current_key = random.choice(list(markov_chains.keys()))
    generated_words_list = list(current_key)
    
    # append words to generate text based on possible values using random probability as transformation matrix
    while len(generated_words_list) < length:
        possible_values = markov_chains.get(current_key, [])
        if not possible_values:
            current_key = random.choice(list(markov_chains.keys()))
            generated_words_list.extend(current_key)
        else:
            next_word = random.choice(possible_values)
            generated_words_list.append(next_word)
            current_key = tuple(generated_words_list[-order:])
    
    return ' '.join(generated_words_list)

# generate text based on provided variables
novel_text = text_generator(user_text_cleaned)

# output the generated text
print(novel_text)
