from argon2 import PasswordHasher
import base64
import sys
import re


# TODO: Implement masking logic.
# TODO: Crack multiple hashes at once.


def parse_argon2_conf(argon2_conf):
    """
    Parses the argon2 configuration string.
    :param conf: The argon2 configuration string.
    :return: The parsed configuration as a dictionary.
    """

    match = re.search(r"\$v=(\d+)\$m=(\d+),t=(\d+),p=(\d+)\$(.+)\$(.+)", argon2_conf)
    
    keys = ["version", "memory", "iterations", "parallelism", "salt", "hash"]
    values = [0,0,0,0,0,0]
    
    j = 0
    for i in range(1, 7):
        values[j] = match.group(i)
        j += 1

    argon2_dict = dict(zip(keys, values))
    return argon2_dict


def read_argon2_hash(filename):
  """
  Read the Argon2 hash from a file.
  Args:
    filename (str): The path to the file containing the Argon2 hash.
  Returns:
    str: The Argon2 hash read from the file.
  """
  with open(filename, "r") as f:
    argon2_hash = f.read()
  return argon2_hash


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
  Corrects the padding of the given salt string to ensure it has a length that is a multiple of 4.

  Args:
    salt (str): The salt string to correct the padding for.

  Returns:
    str: The salt string with corrected padding.
  """
  missing_padding = len(salt) % 4
  if missing_padding:
    salt += '='* (4 - missing_padding)
  return salt


def main():
  """
  Main function for cracking Argon2 hashed passwords.

  This function takes a wordlist file, and an Argon2 hash configuration file.
  It iterates through each word in the wordlist, combines it with a prefix and suffix character, and hashes the resulting password using Argon2.
  If the hashed password matches the provided Argon2 hash configuration, the password is considered cracked and written to a file named "cracked.pot".
  """

  ph = PasswordHasher()
  
  wordlist = read_wordlist(sys.argv[1])

  argon2_conf = read_argon2_hash(sys.argv[2])
  parsed_conf = parse_argon2_conf(argon2_conf)
  salt = parsed_conf["salt"]
  salt = correct_padding(salt)
  salt = base64.b64decode(salt)

  if len(sys.argv) == 4:
    mask = sys.argv[3]
    print("Masking not implemented yet.")

  for word in wordlist:
    for i in range(0, 10):
      for j in range(0, 10):
        prefix = str(i)
        suffix = str(j)
        password = prefix + word + suffix
        password_conf = ph.hash(password, salt=salt)
        password_conf = parse_argon2_conf(password_conf)
        password_hash = password_conf["hash"]
        hashToCompare = parsed_conf["hash"]
        print("Testing password: " + password)
        if password_hash == hashToCompare:
          print("Password cracked: " + password)
          with open("cracked.pot", "w") as f:
            f.write(password)
          return
  print("Password not found.")


if __name__ == "__main__":
    main()