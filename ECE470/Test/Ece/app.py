from flask import Flask, request, render_template
import vigenere_cipher
import random
import string
from global_variables import english_language_relative_frequencies, reverse_dict
from cryptography_algebra import relative_frequencies_calculator
from ngram_score import ngram_score
from vigenere_cipher import decrypt
import numpy as np
import pandas as pd


app = Flask(__name__)

fitness = ngram_score('english_quadgrams.txt')
ct=""
kList=""


def generate_random_keys(number_of_keys, key_length):
    """
        generates random keys with a helper function
    """
    lst = []
    for i in range(number_of_keys):
        lst.append(random_key(key_length))
    return lst

def random_key(key_length):
    """
        using random choice to randomly generate english alphabet
        return randomly generated keyword of size key_length
    """
    key = ''
    for i in range(key_length):
        key = key + random.choice(string.ascii_letters).upper()
    return key

def crossover(parent_1, parent_2):
    """
        get random crossover point
        swap alphabets between two parent keys after the crossover point
    """
    key_size = len(parent_1)
    crossover_point = random.randint(1, key_size-1)
    child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
    child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
    return [child_1, child_2]

def mutation(parent_1, parent_2):
    """
        get two random numbers from parent_1 and parent_2
        swap alphabet indexed at two random numbers between two parents
    """
    key_size = len(parent_1)
    first_random_point  = random.randint(0, key_size-1)
    second_random_point = random.randint(0, key_size-1)
    temp_parent1 = list(parent_1)
    temp_parent2 = list(parent_2)
    temp_parent1[first_random_point] = parent_2[second_random_point]
    temp_parent1[second_random_point] = parent_2[first_random_point]
    temp_parent2[first_random_point] = parent_1[second_random_point]
    temp_parent2[second_random_point] = parent_1[first_random_point]
    return [''.join(temp_parent1), ''.join(temp_parent2)]

def fitness_score(decrypted_text):
    return fitness.score(decrypted_text.replace(' ', '').upper())

def run_genetic_algorithm(key_length, cipher_text, number_of_generations=100, mutation_rate=0.2):
    """
        initialize by generating random keys with given key length
        sort the random keys
        start the generations (iterations) until the top suited key is returned:
            - apply crossover, mutation, sort top keys
        finally return decrypted text using that top 1 sorted key with highest fitness score
    """
    global ct
    ct = cipher_text
    some_keywords_list = []
    lst = generate_random_keys(number_of_keys=7000, key_length=key_length)
    sorted_keywords = top_suitable_keywords(number_of_items=600, keywords_with_fitness_scores=keywords_and_suitability_score(lst, cipher_text))
    for m in range(number_of_generations):
        keywords_pairs = pair_keywords(sorted_keywords)
        keywords_pairs = crossover_and_certain_percent_mutation(keywords_pairs,mutation_percent=mutation_rate)
        lst = keywords_pairs.flatten()
        sorted_keywords = top_suitable_keywords(number_of_items=30, keywords_with_fitness_scores=keywords_and_suitability_score(lst, cipher_text))
        if m % 5 == 0:
            some_keywords_list.append(sorted_keywords)
        #print(sorted_keywords)
    return [decrypt(cipher_text, keyword=sorted_keywords[0]), some_keywords_list]

def keywords_and_suitability_score(keywords, cipher_text):
    """
        get fitness scores of each keyword
        return two lists with keywords and fitness_scores respectively
        this is for successfully getting top suitable keywords from following mentioned function!
    """
    key_fitness_scores = []
    for i in keywords:
        key_fitness_scores.append(fitness_score(decrypt(ciphertext=cipher_text, keyword=i).upper()))
    return [keywords, key_fitness_scores]

def decrypt_with_suitable_keywords(CText):
    mylist = []
    for i in kList:
        mylist.append(decrypt(CText, i))
    data3 = dict(zip(kList, mylist))
    return data3

def top_suitable_keywords(number_of_items, keywords_with_fitness_scores):
    """
        creating pandas dataframe with keywords and fitness_scores column
        return keywords with top fitness_scores
    """
    global kList
    df = pd.DataFrame(data={'keywords': keywords_with_fitness_scores[0], 'fitness_scores': keywords_with_fitness_scores[1]})
    sorted_df = df.sort_values(by=['fitness_scores'], ascending=False)
    #data2 = decrypt_with_suitable_keywords(ct)
    kList = keywords_with_fitness_scores[0]
    #print(keywords_with_fitness_scores)
    return list(sorted_df['keywords'])[:number_of_items]

def pair_keywords(keywords_list):
    """
        shuffle the list of keywords
        to randomly pair the keywords
        [could use roulette wheel to pair the keywords!]
    """
    np.random.shuffle(keywords_list)
    return np.array(keywords_list).reshape(int(len(keywords_list)/2), 2)

def crossover_and_certain_percent_mutation(keywords_pairs, mutation_percent):
    """
        applying crossover to keywords_pairs
        applying mutation to certain percent of crossovered children
        this is a helper function for genetic algo function!
    """
    mutation_rate = int(len(keywords_pairs) * mutation_percent)
    for i in keywords_pairs:
        children_after_crossover = crossover(parent_1=i[0], parent_2=i[1])
        keywords_pairs = np.concatenate((keywords_pairs, np.array([children_after_crossover])), axis=0)
    np.random.shuffle(keywords_pairs)
    for i in range(mutation_rate):
        keywords_pairs[i] = mutation(keywords_pairs[i][0], keywords_pairs[i][1])
    return keywords_pairs

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/vigenere', methods=['GET', 'POST'])
def vigenere():
    '''
        Approach: same as that of Caesar cipher listed above.
    '''
    if request.method == 'POST':
        plain_text = request.form['plain_text']
        keyword = str(request.form["keyword"])
        return render_template('vigenere.html', data=[plain_text, vigenere_cipher.encrypt(plain_text, keyword)])
    return render_template("vigenere.html", data=["", ""])

@app.route('/crack', methods=['GET','POST'])
def ga():
    '''
        render template and crack crypto system depending on choice of ciphers such as Caesar Cipher or Vigenere ciphers in our case!
    '''
    if request.method == 'POST':
        cipher_text = request.form['cipher_text']
        key_length = int(request.form['key_length'])
        num_of_generations = int(request.form['generations'])
        data = run_genetic_algorithm(key_length=key_length, cipher_text=cipher_text, number_of_generations=num_of_generations)
        data.append(cipher_text)
        data3 = decrypt_with_suitable_keywords(cipher_text)
        return render_template('crack.html', data=data, data3=data3)
    return render_template('crack.html')

if __name__ == '__main__':
	app.run()  