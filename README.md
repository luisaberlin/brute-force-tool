Requires at least Python 3.10

## Actions
* `rp`   Try random variations of characters.  
       This command requires a second parameter to set the allowed characters e.g. ul for upper- and lowercase  
    * `u` Uppercase
    * `l` Lowercase
    * `n` Numbers
    * `s` Special characters
* `lcp`  Try passwords of the list of common passwords.
* `d`  Try variations of words and sentences of the german and english dictionary.
* `rup`  Try passwords, which are already known of the user.

## Run

`python3 brute-force-tool.py <pathToZipFile> <action> <option>`

e.g.  
`python3 brute-force-tool.py ./ZipFiles/5.zip rp uls`

## Features
* **RandomPassword**: Vollkommen zufällige Passwörter, wobei die Arten der verwendeten Zeichen (Großbuchstaben, Kleinbuchstaben, Zahlen, Sonderzeichen, etc.) eingestellt werden kann.
* **ListOfCommonPasswords**: Probieren der Liste von häufigen Passwörtern
    [GitHub link](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt)
* **Dictonary**: Nutzung von Wörterbüchern in Deutsch und Englisch zur Generierung von Passwörtern und Sätzen
* **RandomUserPassword**: Funktion, die Passwörter durchprobiert die über einen Benutzer bekannt sind
* **?**: Funktion, die Variationen von Passwörtern erzeugt in dem u. A. Zahlen sowie Sonderzeichen eingefügt oder angehängt werden, die Groß- und Kleinschreibung alterniert wird oder leetspeak verwendet wird


## Fragen
1. Wie lang soll max. das Passwort sein? Sollen wir für jede Länge ausprobieren? 
2. Die zip Datein lassen sich nicht downloaden in gemini