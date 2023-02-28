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

# generator of text using markov chains
def text_generator(user_text_cleaned, order=user_order, length=user_length):
    # obtaining a list of words from provided text
    words = user_text_cleaned.split()
    
    # storing markov chains with variables and states
    chains = {}
    for i in range(len(words) - order):
        # we need to create combinations of context based on the order provided
        key = tuple(words[i:i+order])

        # we need to store the possible values for words
        if key in chains:
            chains[key].append(words[i+order])
        else:
            chains[key] = [words[i+order]]
    
    # selecting a random starting point
    current_key = random.choice(list(chains.keys()))
    generated_words = list(current_key)
    
    # append words to generate text based on possible values
    while len(generated_words) < length:
        possible_values = chains.get(current_key, [])
        if not possible_values:
            current_key = random.choice(list(chains.keys()))
            generated_words.extend(current_key)
        else:
            next_word = random.choice(possible_values)
            generated_words.append(next_word)
            current_key = tuple(generated_words[-order:])
    
    return ' '.join(generated_words)

# clean the text provided by the user
user_text_cleaned = preprocessor_text(user_text).lower()

# generate text based on provided variables
generated_text = text_generator(user_text_cleaned)

# output the generated text
print(generated_text)
