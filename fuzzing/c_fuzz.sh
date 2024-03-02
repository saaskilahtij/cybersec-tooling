#!/bin/bash

# This script performs fuzzing on a single program c program using radamsa.
# First install radamsa, for example `sudo apt install radamsa` or `brew install radamsa`.
# Make sure you have rights to execute the program and the input files (chmod +x <program_name>).
# Run: ./c_fuzz.sh <program_name> <fuzz-string> <seed-int> <input-file-count>

USAGE="Usage: $0 <program_name> <fuzz-string> <seed-int> <input-file-count>"

if [ "$#" -lt 3 ]; then
  echo "$USAGE"
  exit 1
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "$USAGE"
  exit 1
fi

PROGRAM_NAME="$1"
FUZZ_STRING="$2"
SEED="$3"
INPUT_FILE_COUNT="$4"

FUZZ_DIR="$PROGRAM_NAME-fuzzes"
CRASH_DIR="$FUZZ_DIR/crash-files"
OUTPUT_DIR="$FUZZ_DIR/fuzz-output-files"
INPUT_DIR="$FUZZ_DIR/fuzz-input-files"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$CRASH_DIR"
mkdir -p "$INPUT_DIR"

# Create input files using radamsa
echo "Fuzzing $PROGRAM_NAME with $FUZZ_STRING and seed $SEED"
echo -n "$FUZZ_STRING" | radamsa -o $FUZZ_DIR/fuzz-%n.txt -n $INPUT_FILE_COUNT -s $SEED

# Feed fuzz input files to the program
for f in $FUZZ_DIR/fuzz-*.txt; do
  echo "Processing: $f"
  ./"$PROGRAM_NAME" "$f" > $OUTPUT_DIR/$(basename $f)
  
  # Check if the program crashed
  if [ $? -gt 127 ]; then
    cp "$OUTPUT_DIR/$(basename $f)" "$CRASH_DIR/$(basename $f)"
    echo "Program crashed on $(basename $f)"
  fi
done
