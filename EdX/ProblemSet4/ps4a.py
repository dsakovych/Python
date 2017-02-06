# The 6.00 Word Game

import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5,
                          'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4,
                          'w': 4, 'x': 8, 'y': 4, 'z': 10
                          }

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList


def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#

def getWordScore(word, n):
    word = word.lower()
    result = 0
    for letter in word:
        result += SCRABBLE_LETTER_VALUES.get(letter, 0)
    if len(word) == n:
        return result * len(word) + 50
    else:
        return result * len(word)


#
# Problem #2: Make sure you understand how this function works and what it does!
#


def displayHand(hand):
    result = []
    for letter in hand.keys():
        for j in range(hand[letter]):
             result.append(letter)
    return ' ' .join(result)

#
# Problem #2: Make sure you understand how this function works and what it does!
#


def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#


def updateHand(hand, word):
    handcopy=hand.copy()
    for letter in word:
        if letter in handcopy.keys():
            handcopy[letter] -= 1
    return {key:handcopy[key] for key in handcopy.keys() if handcopy[key] != 0}

#
# Problem #3: Test word validity
#


def isValidWord(word, hand, wordList):
    if not word in wordList:
        return False
    for letter in word:
        if not letter in list(hand.keys()):
            return False
    dict = getFrequencyDict(word)
    for k, v in dict.items():
        if hand.get(k,0) >= dict.get(k,0):
            continue
        else:
            return False
    return True

#
# Problem #4: Playing a hand
#


def calculateHandlen(hand):
    return sum([v for k,v in hand.items()])


def playHand(hand, wordList, n):
    score = 0
    while calculateHandlen(hand) > 0:
        print(displayHand(hand))
        word = input('Enter word, or a "." to indicate that you are finished: ')
        if word == '.':
            print('Goodbye! Total score: %d points.' % score)
            return
        else:
            if isValidWord(word, hand, wordList):
                score += getWordScore(word, n)
                hand = updateHand(hand, word)
                print(' "%s"' % word, 'earned %s points.' % getWordScore(word, n), 'Total: %s points' % score)
                continue
            else:
                print(' Invalid word, please try again.')
                continue
    print('Run out of letters. Total score: %d points.' % score)


#
# Problem #5: Playing a game
# 

def playGame(wordList):
    hand = None
    n = HAND_SIZE
    while True:
        var = input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if var == 'r' and hand is None:
            print('You have not played a hand yet. Please play a new hand first!')
        elif var == 'r' and hand is not None:
            playHand(hand, wordList, n)
        elif var == 'n':
            hand = dealHand(HAND_SIZE)
            playHand(hand, wordList, n)
        elif var == 'e':
            break
        else:
            print('Invalid command.')



#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
