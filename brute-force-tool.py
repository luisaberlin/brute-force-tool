from itertools import product
import sys
import zipfile
from pathlib import Path
import time
from multiprocessing import Process

upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerCase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
# specialCharacters = "!#$%&'()*+,-./:;<=>?@[\]^_{|}~"
specialCharacters = "!#$%&*+,-.:;<=>?@"
pathToCommonPasswordsZipFile = "./10-million-password-list-top-1000000.txt.zip"
pathToGermanWords = "./german-words.txt.zip"
pathToEnglishWords = "./english-words.txt.zip"
  
def main():
    zipPath = sys.argv[1] if len(sys.argv) > 1  else ""
    if not Path(zipPath).is_file():
        print(f"The file '{zipPath}' does not exist.")
        sys.exit()
    if Path(Path(zipPath).stem).is_file():
        print(f"The file '{zipPath}' is already unzipped.\n")

    match sys.argv[2:]:
        case ["rp", characters, minLength, maxLength]:
            allowedChars = getAllowedChars(characters)
            print(f"Allowed characters: {allowedChars}\n")
            tryRandomPasswords(zipPath, allowedChars, minLength, maxLength)
        case ["lcp"]:
            tryList(zipPath, pathToCommonPasswordsZipFile, False)
        case ["d"]:
            tryVariationOfGermanAndEnglishWords(zipPath)
        case ["rup"]:
            print("rup")
        case ["rsn"]:
            tryLeetSpeak(zipPath)
        case _:
            print("Invalid command. Check out the README.md")


def tryVariationOfGermanAndEnglishWords(zipPath):
    print("Try if any english word matches. That will take approximatly 180s.")
    p1 = Process(target=tryEnglishSentences, args=(zipPath, ))

    print("Try if any english word matches. That will take approximatly 180s.")
    p2 = Process(target=tryList, args=(zipPath, pathToEnglishWords, False, ))

    print("Try if any german word matches. That will take approximatly 1015s.")
    p3 = Process(target=tryList, args=(zipPath, pathToGermanWords, False,))

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

    start = time.time()
    result = ""

    for subject in subjects:
        for verb in verbs:
            for object in objects:
                lowerCasePw = subject + verb + object
                upperCasePw = subject.capitalize() + verb.capitalize() + object.capitalize()
                if validPassword(zipPath, lowerCasePw):
                    result = lowerCasePw
                    break
                if validPassword(zipPath, upperCasePw):
                    result = upperCasePw
                    break

    end = time.time()

    if result:
        print(f"The password is '{result}'.")
        print(f"It took {end - start}s to find the password.")
        sys.exit()
    else:
        print("No password found.")
        print(f"It took {end - start}s.")

                


def tryList(zipPath, pathToList, leetSpeak):
    if not Path(pathToList[:-4]).is_file():
        with zipfile.ZipFile(pathToList, 'r') as zipRef:
            zipRef.extractall("./")

    start = time.time()
    result = ""

    file = open(pathToList[:-4],'r')
    while True:
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

    end = time.time()
    if not result:
        print(f"No password matched. ({pathToList})")
        print(f"It took {end - start}s.")
    else:
        print(f"The password is '{result}'. ({pathToList})")
        print(f"It took {end - start}s to find the password.")
        sys.exit()


    


def tryRandomPasswords(zipPath, chars, min, max):
    start = time.time()

    round = 1
    while True:
        print(f"Try combinations where every charecter appears {round} time(s). ")
        for i in range(int(min), int(max)+1):
            print(f"    Try combinations with length of {i}")
            for randomCombination in (product(chars, repeat=i)):
                randomPw = "".join(randomCombination)
                if validPassword(zipPath, randomPw):
                    end = time.time()
                    print(f"\nThe password is '{randomPw}'.")
                    print(f"It took {end - start}s to find the password.")
                    sys.exit()

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
    tryList(zipPath, pathToCommonPasswordsZipFile, True)
    print("Try leetspeak with list of english words")
    tryList(zipPath, pathToEnglishWords, True)
    print("Try leetspeak with list of german")
    tryList(zipPath, pathToGermanWords, True)



def applyLeetSpeak(word):
    lowerCaseWord = word.lower()
     # return lowerCaseWord.translate(str.maketrans({'a': '@', 'c': '[', 'g': '9', 'i': '1', 'o': '0', 's': '$'}))
    return lowerCaseWord.translate(str.maketrans({'a': '@', 'c': '(', 'g': '6', 'i': '!', 'o': '0', 's': '$', 'l':'1'}))


def validPassword(zipPath, password):
    with zipfile.ZipFile(zipPath) as zf:
        try:
            zf.extractall(pwd=bytes(password,'utf-8'))
        except RuntimeError:
            return False
        except zipfile.BadZipFile: # weird error, that somethimes comes up
            return False
        except zipfile.zlib.error: # another weird error, that somethimes comes up
            return False
        else:
            return True


if __name__ == "__main__":
    main()


# Todos
# - Treading
# - Function that runs all methods
# - Something that shows how long the program is running alreday
# - Random passwords: add min and max length


# Results
# 1: 98765
# 2: admin