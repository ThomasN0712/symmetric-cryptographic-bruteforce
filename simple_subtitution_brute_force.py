#Other tactics to try:
# bigrams into trigrams or trigrams into bigrams
# compare with 10k most common words at the end then restart if neccessary
# implemented timer to make sure program don't run over 2 minutes.
# use quadgrams??
# simulated annealing: https://github.com/damiannolan/simulated-annealing-playfair-cipher-breaker/blob/master/README.md



import string
import math
from itertools import permutations
import numpy as np
import random
import wordsegment

def generate_message(message, key):
    '''
    Generate message/cipher text from a key
    input: message, key (String)
    return message (dict)
    '''
    temp_message = []
    alphabet_dict = key_to_dict(key)
    for letter in message:
        temp_message.append(alphabet_dict.get(letter))
    message = "".join(temp_message)
    return message

def key_to_dict(value):
    '''
    Take in key and turn it into standard alphabet to new key dict
    input: value (String)
    return dictionary (dict)
    '''
    value = list(value)
    alphabet_list = list(string.ascii_uppercase) 
    dictionary = {alphabet_list[i]: value[i] for i in range(len(alphabet_list))}
    return dictionary


def calculate_ngram_score(ngramfile):
    '''
    Frequency Analysis for ngrams
    input: ngramfile(String): Open File
    output: 
        ngrams (dict): dictionary of all ngrams score using log probabilities
        N (int): Total of grams in file
    '''
    ngrams = {}
    N = 0 # number of trigrams in text file
    for line in ngramfile:
        key, count = line.split() 
        ngrams[key] = int(count)
        N += int(count) # number of trigrams in text file
    #calculate log probabilities
    for key in ngrams.keys():
        ngrams[key] = math.log10(float(ngrams[key])/N)
    return ngrams, N

def monogram_key(message):
    '''
    Generate first key with monogram:
    input: message(String)
    output: key from monogram
    '''
    #count single char frequency - rewriteon
    # return string key
    def char_frequency(str):
        dict = {}
        for n in str:
            keys = dict.keys()
            if n in keys:
                dict[n] += 1
            else:
                dict[n] = 1
        return dict
    
    #order
    frequency = dict(sorted(char_frequency(message).items(), key=lambda x:x[1], reverse=True))
    alphabet_list = list(string.ascii_uppercase)
    frequency_key = list(frequency.keys())
    for letter in alphabet_list:
        if letter not in frequency_key:
            frequency_key.append(letter)
    letter_frequency = ['E','T','A','O','I','N','S','H','R','D','L','C','U','M','W','F','G','Y','P','B','V','K','X','J','Q','Z']
    alphabet_dict = {frequency_key[i]:letter_frequency[i] for i in range(26)}
    sorted_alphabet_dict = dict(sorted(alphabet_dict.items()))
    return "".join(list(sorted_alphabet_dict.values()))

def score_bigrams(text, grams, N):
    ''' 
    compute the score of text using bigrams
    input:
        text (String)
        grams (dict): Output of salculate_ngrams_score
        N (int): Output of salculate_ngrams_score
    '''
    score = 0
    for i in range(len(text) - 1):
        if text[i : i + 2] in grams.keys(): 
            score += grams.get(text[i : i + 2])
        else:
            score += math.log10(0.01/N)
    return score

def score_trigrams(text, grams, N):
    ''' 
    compute the score of text using trigrams
    input:
        text (String)
        grams (dict): Output of salculate_ngrams_score
        N (int): Output of salculate_ngrams_score
    '''
    score = 0
    for i in range(len(text) - 2):
        if text[i : i + 3] in grams.keys(): 
            score += grams.get(text[i : i + 3])
        else:
            score += math.log10(0.01/N)
    return score

def swap_letters(key, trigram_score, limit_adjustment = 0):
    ''' 
    swap letters of a key randomly to generate new key
    input:
        key (String): initial key
        trigram_score (dict): trigram_score of initial key for calculating swap_limit
        limit_adjustment (int): for calculate swap_limit, initially 0
    output:
        key_str (String): new key
    '''
    key = list(key)
    swappable_range = [i for i in range(len(key))]
    swap_limit = max(1, math.ceil(-trigram_score / 60)) + limit_adjustment  #random equation to calculate swap limit
    swaps = random.randint(1, swap_limit)

    for swap in range(swaps):
        # Choose two random letter to swap
        i = np.random.choice(swappable_range)  
        j = random.choice(swappable_range)
        key[i], key[j] = key[j], key[i]
        key_str = "".join(key)
    return key_str

def segmented_text(decrypted_text):
    ''' 
    Use segmented function to segment text
    input:
        decrypted_text (String): Final output
    output:
        segments (String)
    '''
    wordsegment.load()
    segments = wordsegment.segment(decrypted_text)
    return " ".join(segments)
    
def main():
    #Bigram and Trigram set up
    bi_grams_file = open("english_bigrams.txt", 'r')
    tri_grams_file = open("english_trigrams.txt", 'r')
    
    bigrams, bigrams_N = calculate_ngram_score(bi_grams_file)
    trigrams, trigrams_N = calculate_ngram_score(tri_grams_file)

    cypher_list = []
    #Original Cypher text
    crypto_code = open("crypto_code.txt", 'r')
    for code in crypto_code:
        if code.strip():
            c = code.replace(" ", "")
            c = code.replace("\n", "")
            c = c[2:] #skip numbers and dot
            c = c.upper()
            cypher_list.append(c)
            
    for original_cypher_text in cypher_list:
        # original_cypher_text = "iyhqz ewqin azqej shayz niqbe aheum hnmnj jaqii yuexq ayqkn jbeuq iihed yzhni ifnun sayiz yudhe sqshu qesqa iluym qkque aqaqm oejjs hqzyu jdzqa diesh niznj jayzy uiqhq vayzq shsnj jejjz nshna hnmyt isnae sqfun dqzew qiead zevqi zhnjq shqze udqai jrmtq uishq ifnun siiqa suoij qqfni syyle iszhn bhmei squih nimnx hsead shqmr udquq uaqeu iisqe jshnj oihyy snaxs hqihe lsilu ymhni tyz"
        # original_cypher_text = original_cypher_text.upper().replace(" ", "")
        original_cypher_text = original_cypher_text.replace(" ", "") 
        cypher_text = original_cypher_text
        original_score = score_trigrams(cypher_text, trigrams, trigrams_N)
    
        #Generate first key with monogram:
        monogram_initial_key = monogram_key(cypher_text)
        #new message after first initial key:
        cypher_text = generate_message(cypher_text, monogram_initial_key)
        monogram_score = score_trigrams(cypher_text, bigrams, bigrams_N)

        #In case if string is already cipher:
        if monogram_score > original_score:
            initial_key = monogram_initial_key
            initial_score = monogram_score
        else:
            initial_key = string.ascii_uppercase
            initial_score = original_score

        global_counter = 1
        key_score_dict = {initial_key: initial_score}
        score = initial_score

        target_score = -50 #arbitrary number, depend on input size, leave as -50 for now
        limit_adjustment = 0
        stagnant_counter = 0
        best_key = initial_key
        stagnant_limit = 400

        while(score < target_score): 
            global_counter +=1
            initial_key = max(key_score_dict, key = key_score_dict.get)
            #convert to dictionary and generate message
            new_key = swap_letters(initial_key, initial_score, limit_adjustment) #key use score to determine swap limit
            cypher_text = generate_message(original_cypher_text, new_key)
            #score = score_bigrams(cypher_text, bigrams, bigrams_N)
            score = score_trigrams(cypher_text, trigrams, trigrams_N)

            #add score and key to dict for picking highest score
            key_score_dict[new_key] = score
            if global_counter % 10 == 0: # each 10 cycles, select best key and start there
                previous_best_key = best_key 
                best_key = max(key_score_dict, key = key_score_dict.get)
                if previous_best_key == best_key:
                    stagnant_counter += 1
                    if stagnant_counter == stagnant_limit:
                        limit_adjustment += 1
                        print("Stagnant limit reached, adjusting limit to:", limit_adjustment, "Max limit:", 5)
                        stagnant_counter = 0
                else:
                    stagnant_counter = 0
                    limit_adjustment = 0
                    key_score_dict = {best_key: key_score_dict.get(best_key)}
                    print("New best key:", best_key, "Score:", key_score_dict.get(best_key))

            if limit_adjustment == 5:
                print("Stagnant limit reached max, give up.")
                break

        best_key = max(key_score_dict, key = key_score_dict.get)
        final_cypher = generate_message(original_cypher_text, best_key)
        seg_text = segmented_text(final_cypher)
        open("output_brute_force.txt", "a").write("Orginal text:" + original_cypher_text + "\nKey:" + best_key + "\nSegmented text:" + seg_text + "\n\n")
    return 0

if __name__ == '__main__':
    main()