from argon2 import PasswordHasher
import sys
import base64

"""
This script generates a rainbow table for Argon2 hashes.
The rainbow table is written to a file named "argon2_rainbow_table.txt".
Wordlist and salt are provided as command line arguments and salt is optional.

Usage: python3 argon2_rainbow_table.py <wordlist> <salt>

Example: python3 argon2_rainbow_table.py wordlist.txt fQZmRnaMPkdZaqwOJKludA
"""

def read_wordlist(wordlist):
    """
    Reads the wordlist file.
    :param wordlist: The wordlist file.
    :return: The wordlist as a list.
    """
    with open(wordlist, "r") as f:
        wordlist = f.readlines()
    wordlist = [word.strip() for word in wordlist]
    return wordlist


def correct_padding(salt):
  """
  Corrects the padding of the salt string to ensure it has a length that is a multiple of 4.

  Args:
    salt (str): The salt string to be padded.

  Returns:
    str: The salt string with correct padding.
  """
  missing_padding = len(salt) % 4
  if missing_padding:
    salt += '='* (4 - missing_padding)
  return salt


def main():

  ph = PasswordHasher()
  
  wordlist = read_wordlist(sys.argv[1])
  if (sys.argv[2]):
    salt = sys.argv[2]
    salt = correct_padding(salt)
    salt = base64.b64decode(salt)

  for word in wordlist:
    for i in range(0, 10):
      for j in range(0, 10):
        prefix = str(i)
        suffix = str(j)
        password = prefix + word + suffix
        hash = ph.hash(password, salt=salt)
        with open("argon2_rainbow_table.txt", "a") as f:
          f.write(hash + ":" + password + "\n")


if __name__ == "__main__":
    main()