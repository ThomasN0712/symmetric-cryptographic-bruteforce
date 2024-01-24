#encrypter
import random
import string

def substitution_decrypter(ciphertext, key): 
    ''' 
    Decrypyer using simple subsitution
    input:
        ciphertext (String)
        key (String)
    output:
        plaintext (String)
    '''
    plaintext = ""
    key = key.upper()
    ALPHABET_LIST = string.ascii_uppercase
    for letter in ciphertext:
        if letter.upper() in key:
            substitution_letter = ALPHABET_LIST[key.index(letter.upper())]
            #Maintain upper and lower cases 
            if letter.isupper():
                plaintext += substitution_letter.upper() 
            else:
                plaintext += substitution_letter.lower()
        else:
            #If special character or spaces
            plaintext += letter
    return plaintext

def main():
    cipher_text = input("Enter cipher text: ")
    key = input("Enter the key: ")
    print(substitution_decrypter(cipher_text, key))
    return 0

if __name__ == '__main__':
    main()