from itertools import product
from sys import version, argv, exit
from zipfile import ZipFile, BadZipFile, zlib
from pathlib import Path
from time import time
from multiprocessing import Process
from random import randint, sample

upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerCase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
# specialCharacters = "!#$%&'()*+,-./:;<=>?@[\]^_{|}~"
specialCharacters = "!#$%&*+,-.:;<=>?@"
pathToCommonPasswordsZipFile = "./10-million-password-list-top-1000000.txt.zip"
pathToGermanWords = "./german-words.txt.zip"
pathToGermanWordsSmall = "./german-words-small.txt.zip"
pathToEnglishWords = "./english-words.txt.zip"
  
def main():
    print(f"Python version: {version}\n")

    zipPath = argv[1] if len(argv) > 1  else ""
    if not Path(zipPath).is_file():
        print(f"The file '{zipPath}' does not exist.")
        exit()
    if Path(Path(zipPath).stem).is_file():
        print(f"The file '{zipPath}' is already unzipped.\n")

    if argv[2] == "rp":
        if len(argv) != 6:
            print("Invalid command. Read the README.md.")
            exit()
        characters, minLength, maxLength = argv[3], argv[4], argv[5] 
        allowedChars = getAllowedChars(characters)
        print(f"Allowed characters: {allowedChars}\n")
        tryRandomPasswords(zipPath, allowedChars, minLength, maxLength)
    elif argv[2] == "lcp":
        tryList(zipPath, pathToCommonPasswordsZipFile, False)
    elif argv[2] == "d":
        tryEnglishAndGermanDictonary(zipPath)
    elif argv[2] == "ve":
        tryWordCombination(zipPath, pathToEnglishWords)
    elif argv[2] == "vg":
        tryWordCombination(zipPath, pathToGermanWordsSmall)
    elif argv[2] == "veg":
        tryWordCombinationTwoLanguages(zipPath, pathToEnglishWords, pathToGermanWordsSmall)
    elif argv[2] == "ls":
        tryLeetSpeak(zipPath)
    else:
        print("Invalid command. Read the README.md.")



def tryEnglishAndGermanDictonary(zipPath):
    print("Try if any english word matches. That will take approximatly 180s.")
    p1 = Process(target=tryEnglishSentences, args=(zipPath, ))

    print("Try if any english word matches. That will take approximatly 180s.")
    p2 = Process(target=tryList, args=(zipPath, pathToEnglishWords, False))

    print("Try if any german word matches. That will take approximatly 1015s.")
    p3 = Process(target=tryList, args=(zipPath, pathToGermanWords, False))

    p1.start()
    p2.start()
    p3.start()
    print("Started processes")

    p1.join()
    p2.join()
    p3.join()


def tryEnglishSentences(zipPath):
    subjects = ["i", "you", "he", "she", "it", "it-security", "computerscience", "students", "camera", "loptos", "sun", "vacation"]
    verbs = ["is", "are", "have", "has", "had", "do", "does", "did", "think", "thinks", "find", "finds", "want", "wants", "love", "eat", "like", "likes"]
    objects = ["banana", "great", "bad", "chocolate", "you", "cool", "yummy", "green", "tiered"]

    start = time()
    result = ""

    for subject in subjects:
        for verb in verbs:
            for object in objects:
                lowerCasePw = "".join([subject, verb, object]) 
                upperCasePw = "".join([subject.capitalize(), verb.capitalize(), object.capitalize()])
                if validPassword(zipPath, lowerCasePw):
                    result = lowerCasePw
                    break
                if validPassword(zipPath, upperCasePw):
                    result = upperCasePw
                    break

    end = time()

    if result:
        print(f"The password is '{result}'.")
        print(f"It took {end - start}s to find the password. (english sentences)")
        exit()
    else:
        print("No password found.")
        print(f"It took {end - start}s. (english sentences)")

def tryList(zipPath, pathToList, leetSpeak):
    if not Path(pathToList[:-4]).is_file():
        with ZipFile(pathToList, 'r') as zipRef:
            zipRef.extractall("./")

    start = time()
    result = ""

    file = open(pathToList[:-4],'r')
    while 1:
        next_line = file.readline()

        if not next_line: break

        if leetSpeak: 
            pw = next_line.strip()
        else:
            pw = next_line.strip()

        if validPassword(zipPath, pw): 
            result = pw
            break

    file.close()

    end = time()
    if not result:
        print(f"No password matched.")
        print(f"It took {end - start}s. ({pathToList})")
    else:
        print(f"The password is '{result}'.")
        print(f"It took {end - start}s to find the password. ({pathToList})")
        exit()

def tryWordCombination(zipPath, pathToList):
    if not Path(pathToList[:-4]).is_file():
        with ZipFile(pathToList, 'r') as zipRef:
            zipRef.extractall("./")

    start = time()
    result = ""

    print(f"Open dictonary {pathToList}...")
    file = open(pathToList[:-4],'r')
    words = file.readlines()
    print(f"... that took {time() - start} seconds.")


    numberOfWords = len(words)-1
    while 1:
        randomIndices = sample(range(0, numberOfWords), 2)
        pw = words[randomIndices[0]].strip().capitalize() + words[randomIndices[1]].strip().capitalize()

        if validPassword(zipPath, pw): 
            result = pw
            break

    file.close()

    end = time()
    print(f"The password is '{result}'.")
    print(f"It took {end - start}s to find the password. ({pathToList})")
    exit()

def tryWordCombinationTwoLanguages(zipPath, pathToList1, pathToList2):
    if not Path(pathToList1[:-4]).is_file():
        with ZipFile(pathToList1, 'r') as zipRef:
            zipRef.extractall("./")
    if not Path(pathToList2[:-4]).is_file():
        with ZipFile(pathToList1, 'r') as zipRef:
            zipRef.extractall("./")

    start = time()
    result = ""

    print(f"Open dictonary {pathToList1}...")
    file1 = open(pathToList1[:-4],'r')
    words1 = file1.readlines()
    print(f"... that took {time() - start} seconds.")

    print(f"Open dictonary {pathToList2}...")
    file2 = open(pathToList2[:-4],'r')
    words2 = file2.readlines()
    print(f"... that took {time() - start} seconds.")


    numberOfWords1 = len(words1)-1
    numberOfWords2 = len(words2)-1
    while 1:
        randomIndex1 = randint(0, numberOfWords1)
        randomIndex2 = randint(0, numberOfWords2)
        randomWord1 =  words1[randomIndex1].strip().capitalize()
        randomWord2 =  words2[randomIndex2].strip().capitalize()

        if randint(0, 1) == 0:
            pw = "".join([randomWord1, randomWord2])
            if validPassword(zipPath, pw): 
                result = pw
                break
        else:
            pw = "".join([randomWord2, randomWord1])
            if validPassword(zipPath, pw): 
                result = pw
                break     

    file1.close()
    file2.close()

    end = time()
    print(f"The password is '{result}'.")
    print(f"It took {end - start}s to find the password.")
    exit()

    


def tryRandomPasswords(zipPath, chars, min, max):
    start = time()

    round = 1
    while 1:
        print(f"Try combinations where every charecter appears {round} time(s). ")
        for i in range(int(min), int(max)+1):
            print(f"    Try combinations with length of {i}")
            for randomCombination in (product(chars, repeat=i)):
                randomPw = "".join(randomCombination)
                if validPassword(zipPath, randomPw):
                    end = time()
                    print(f"\nThe password is '{randomPw}'.")
                    print(f"It took {end - start}s to find the password.")
                    exit()

        chars += chars
        round += 1
    


def getAllowedChars(characters): 
    charactersArray = list(characters)
    chars = ""

    if 'u' in charactersArray: chars += upperCase
    if 'l' in charactersArray: chars += lowerCase
    if 'n' in charactersArray: chars += numbers
    if 's' in charactersArray: chars += specialCharacters

    return chars

def tryLeetSpeak(zipPath):
    print("Try leetspeak with list of common passwords")
    p1 = Process(target=tryList, args=(zipPath, pathToCommonPasswordsZipFile, True))

    print("Try leetspeak with list of english")
    p2 = Process(target=tryList, args=(zipPath, pathToEnglishWords, True))

    print("Try leetspeak with list of german")
    # p3 = Process(target=tryList, args=(zipPath, pathToGermanWords, True))
    p3 = Process(target=tryList, args=(zipPath, pathToGermanWordsSmall, True))

    p1.start()
    p2.start()
    p3.start()
    print("Started processes")

    p1.join()
    p2.join()
    p3.join()



def applyLeetSpeak(word):
    lowerCaseWord = word.lower()
    # return lowerCaseWord.translate(str.maketrans({'a': '@', 'c': '(', 'g': '6', 'i': '!', 'o': '0', 's': '$', 'l':'1'})) # veriation 1
    return lowerCaseWord.translate(str.maketrans({'a': '@', 'c': '[', 'g': '9', 'i': '1', 'o': '0', 's': '$'}))  # variation 2


def validPassword(zipPath, password):
    with ZipFile(zipPath) as zf:
        try:
            zf.extractall(pwd=bytes(password,'utf-8'))
        except RuntimeError:
            return False
        except BadZipFile: # weird error, that somethimes comes up
            return False
        except zlib.error: # another weird error, that somethimes comes up
            return False
        else:
            return True


if __name__ == "__main__":
    main()


# Results
# 1: 98765
# 2: admin

# Tested: 

# +++ zip4 +++
# Random
    # where every charecter appears 1 time(s). Try combinations with length of 4
# Leet Speek
    # variation 1 X
    # variation 2 X
# Dictonary
    # english: 
    # german:
    # english sentences: 
# Variation of Words
    # english:
    # german:
    # english/german:

# +++ zip3 +++
# Random
# Leet Speek
    # variation 1
        # english-words: No password matched. It took 317.59994101524353s.
    # variation 2
# Dictonary
    # english: 
    # german:
    # english sentences: 
# Variation of Words
    # english:
    # german:
    # english/german:

# Try List with CPU: It took 554.4357798099518s. 
