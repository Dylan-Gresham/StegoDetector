#!/bin/bash

INPUT_FILE="sample_files.txt"
if [ ! -f "$INPUT_FILE" ]; then
    echo "Run the sample_files.py script to generate the list of files to sample and the messages."

    exit 1
else
    echo "Found $INPUT_FILE!"
fi

echo 'Creating stego files...'
while IFS="," read -r FILE_PATH STRING; do
    FILE_PATH=$(echo "$FILE_PATH" | xargs)
    STRING=$(echo "$STRING" | xargs)

    mkdir -p "$(dirname data/stego/$FILE_PATH)"

    stegano-lsb hide -i "data/clean/$FILE_PATH" -m "$STRING" -o "data/stego/$FILE_PATH"
done < "$INPUT_FILE"

echo 'Done!'
