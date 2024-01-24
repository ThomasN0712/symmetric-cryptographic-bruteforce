#encrypter
import random
import string

def substitution_encrypter(plaintext, key):
    ''' 
    Encrypyer using simple subsitution
    input:
        plaintext (String)
        key (String)
    output:
        ciphertext (String)
    '''
    ciphertext = ""
    ALPHABET_LIST = string.ascii_uppercase
    for letter in plaintext:
        if letter.upper() in ALPHABET_LIST:
            substitution_letter = key[ALPHABET_LIST.index(letter.upper())]
            if letter.isupper():
                ciphertext += substitution_letter.upper()
            else:
                ciphertext += substitution_letter.lower()
        else:
            ciphertext += letter
    return ciphertext

def main():
    plaintext = input("Enter plaintext: ")
    choice = int(input("1. Use your own key.\n2. Generate random key.\nEnter your choice: "))
    if choice == 1:
        key = input("Enter your key: ")
    else:
        key = list(string.ascii_lowercase)
        random.shuffle(key)
        key = ''.join(key)
        print("Your random generated key is:", key)
    print(substitution_encrypter(plaintext, key))
    return 0

if __name__ == '__main__':
    main()