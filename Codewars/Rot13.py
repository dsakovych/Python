import string

def rot13(message):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    answer = ""
    for letter in message:
        if letter.isupper():
            answer += alphabet[alphabet.index(letter.lower()) - 13].upper()
        elif letter not in alphabet:
            answer += letter
        else:
            answer += alphabet[alphabet.index(letter) - 13]
    return answer
