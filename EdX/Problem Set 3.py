import string

def getAvailableLetters(lettersGuessed):
    alphabet = string.ascii_lowercase
    for letter in lettersGuessed:
        if letter in alphabet:
            alphabet = alphabet.replace(letter,'')
    return alphabet

def isWordGuessed(secretWord, lettersGuessed):
    for letter in lettersGuessed:
        if letter in secretWord:
            secretWord = secretWord.replace(letter, '')
    if len(secretWord) > 0:
        return False
    else:
        return True

def getGuessedWord(secretWord, lettersGuessed):
    answer = list('_' * len(secretWord))
    for letter in lettersGuessed:
        for i in range(len(secretWord)):
            if secretWord[i] == letter:
                answer[i] = secretWord[i]
    return ''.join(answer)


def hangman(secretWord):
    print('Welcome to the game, Hangman!')
    print('I am thinking of a word that is %d letters long.' % len(secretWord))
    print('-------------')
    guesses = 8
    lettersGuessed = []
    while guesses > 0:
        print('You have %d guesses left' % guesses)
        print('Available letters:', getAvailableLetters(lettersGuessed))
        letter = input('Please guess a letter: ')

        if letter in lettersGuessed:
            print("Oops! You've already guessed that letter:", getGuessedWord(secretWord, lettersGuessed))
        elif letter in secretWord:
            lettersGuessed.append(letter)
            print('Good guess:', getGuessedWord(secretWord, lettersGuessed))
        else:
            lettersGuessed.append(letter)
            guesses -= 1
            print('Oops! That letter is not in my word:', getGuessedWord(secretWord, lettersGuessed))
        print('-------------')
        if isWordGuessed(secretWord, lettersGuessed) is True:
            print('Congratulations, you won!')
            break
    if guesses == 0:
        print('Sorry, you ran out of guesses. The word was %s.' % secretWord)

secretWord = 'apple'
hangman(secretWord)
