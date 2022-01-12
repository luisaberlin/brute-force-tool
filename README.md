Requires at least Python 3.10

## Run

`python3 brute-force-tool.py <pathToZipFile> <action> <option>`

e.g.  
`python3 brute-force-tool.py ./ZipFiles/5.zip rp uls 5 8`

## Actions
* `rp`   Try random variations of characters. This command requires a second parameter to set the allowed characters e.g. ul for upper- and lowercase, and requires a 3rd (min length) and a 4th (max length).  
    Options:
    * `u` Uppercase
    * `l` Lowercase
    * `n` Numbers
    * `s` Special characters
* `lcp`  Try passwords of the [list of common passwords](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt).
* `d`  Try variations of words and sentences of the [german](https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4) and [english](https://github.com/dwyl/english-words/blob/master/words_alpha.zip) dictionary.
* `rup`  Try passwords, which are already known of the user.
* `rsn`  Try passwords where letters where replaces by special chars or numbers

