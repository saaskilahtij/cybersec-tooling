#### argon_crack.py

Simple Argon2 cracker which cracks hashes given a wordlist and an Argon configuration.
Currently hardcoded add digits range [0-9] to the start and the end of the word.

The tool which I used to crack an argon2d hash
The parameters have been changed locally to match the correct conf so if ran on another machine, note that params are different. Masking is hard coded by now, cursed, but it works. Prints the cracked password and additionally writes it to a file named 'cracked.pot' Only cracks one hash at a time

Tool is ran with the following command:
  python3 argon_crack.py <wordlist> <argon2 hash>

Example:
  python3 argon_crack.py wordlist.txt argon2_hash.txt

Expect UX updates in the near future.
