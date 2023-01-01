import string
import re
import textwrap

#part1
def normalize(message):
    '''
    message -> string
    return result -> string
    '''
    # Remove punctuation
    message = message.translate(str.maketrans('', '', string.punctuation))
    # Remove whitespaces
    message = ''.join(message.split())
    # Make lower uppers
    message = message.upper()
    return message
    
#part2
def obfuscation(message):
    '''
    message -> string
    return result -> string
    '''
    # Just replaces each vowel with 'OB'+that vowel
    for vowel in 'AEIOUY':
        message = message.replace(vowel, 'ob'+vowel)
    
    message = message.upper()
    return message


#part3
def unobfuscation(message):
    '''
    message -> string
    return result -> string
    '''
    # Reverse of the func above
    for vowel in 'AEIOUY':
        message = message.replace('OB'+vowel, vowel)

    return message


#part4
def caesar(message, shift):
    '''
    message -> string
    return result -> string
    '''
    # I didn't used the shiftAlphabet function, because this method is much easier
    result = ''

    for i in range(len(message)):
        char = message[i]
        # Found this algorithm in internet, it's calculates the shift and just adds it to ord(char)
        result += chr((ord(char) + shift-65) % 26 + 65)

    return result

#part5
def groupify(message, groupingSize):
    '''
    message -> string
    groupingSize -> int
    return result -> string
    '''
    # Converts message into list with code groups
    message = textwrap.wrap(message, groupingSize)

    # Adds 'x' to group member if it's len not equal to groupingSize
    for i in range(len(message)):
        while len(message[i])< groupingSize:
            message[i] = message[i]+'x'

    return ' '.join(message)

def ungroupify(message):
    message = message.replace('x', '')
    message = message.replace(' ', '')

    return message

#part6
def encryption(message, shift , groupSize):
    '''
    message -> string
    return result -> string
    '''
    message = normalize(message)
    message = obfuscation(message)
    message = caesar(message, shift)
    message = groupify(message, groupSize)
    return message

#part7
def decryption(message, shift):
    '''
    message -> string
    return result ->string
    '''
    message = ungroupify(message)
    message = caesar(message, -shift)
    message = unobfuscation(message)

    return message
    
# print(obfuscation('BOBLIKESTODANCEANDEATBOBBYSBOBES'))
# print(unobfuscation('BOBOBLOBIKOBESTOBODOBANCOBEOBANDOBEOBATBOBOBBOBYSBOBOBOBES'))
# print(caesar('ILIKEZOOS', 1))
# print(groupify("HITHEREEE", 4))
print(encryption("This is some \"really\" great. (Text)!?", 2, 2))
# print(ungroupify('HI TH ER Ex'))
print(decryption('VJ QD KU QD KU UQ DQ OQ DG TQ DG QD CN NQ DA IT QD GQ DC VV QD GZ Vx', 2))

