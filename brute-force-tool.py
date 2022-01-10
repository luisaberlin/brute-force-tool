import random
import sys
import zipfile
from pathlib import Path
import time

upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerCase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
specialCharacters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
pathToCommonPasswordsZipFile = "./10-million-password-list-top-1000000.txt.zip"


def main():
    zipPath = sys.argv[1] if len(sys.argv) > 1  else ""
    if not Path(zipPath).is_file():
        print(f"The file '{zipPath}' does not exist.")
        sys.exit()
    if Path(Path(zipPath).stem).is_file():
        print(f"The file '{zipPath}' is already unzipped.\n")

    match sys.argv[2:]:
        case ["rp", characters]:
            allowedChars = getAllowedChars(characters)
            print(f"Allowed characters: {allowedChars}\n")
            tryRandomPasswords(allowedChars, 4, zipPath)
        case ["lcp"]:
            tryList(zipPath, pathToCommonPasswordsZipFile)
        case ["d"]:
            tryVariationOfGermanAndEnglishWords(zipPath)
        case ["rup"]:
            print("rup")
        case _:
            print("Invalid command. Check out the README.md")

#def tryVariationOfGermanAndEnglishWords(zipPath):


def tryList(zipPath, pathToList):
    if not Path(pathToList[:-4]).is_file():
        with zipfile.ZipFile(pathToList, 'r') as zipRef:
            zipRef.extractall("./")

    start = time.time()
    result = ""

    file = open(pathToList[:-4],'r')
    while True:
        next_line = file.readline()

        if not next_line: break
        if validPassword(zipPath, next_line.strip()): 
            result = next_line.strip()
            break

    file.close()

    end = time.time()
    if not result:
        print("No password matched.")
        print(f"It took {end - start}s.")
    else:
        print(f"The password is '{result}'.")
        print(f"It took {end - start}s to find the password.")

    


def tryRandomPasswords(chars, length, zipPath):
    start = time.time()

    while True:
        randomCharsArray = random.choices(chars, k=length)
        randomPw = "".join(randomCharsArray)
        if validPassword(zipPath, randomPw): break

    end = time.time()
    print(f"The password is '{randomPw}'.")
    print(f"It took {end - start}s to find the password.")


def getAllowedChars(characters): 
    charactersArray = list(characters)
    chars = ""

    if 'u' in charactersArray: chars += upperCase
    if 'l' in charactersArray: chars += lowerCase
    if 'n' in charactersArray: chars += numbers
    if 's' in charactersArray: chars += specialCharacters

    return chars


def validPassword(zipPath, password):
    with zipfile.ZipFile(zipPath) as zf:
        try:
            zf.extractall(pwd=bytes(password,'utf-8'))
        except RuntimeError:
            return False
        except zipfile.BadZipFile: # weird error, that somethimes comes up
            return False
        else:
            return True


if __name__ == "__main__":
    main()