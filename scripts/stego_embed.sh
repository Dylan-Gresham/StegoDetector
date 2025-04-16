#!/bin/bash

# === Verify sample file exists ===
INPUT_FILE="sample_files.txt"
if [ ! -f "$INPUT_FILE" ]; then
    echo "Run the sample_files.py script to generate the list of files to sample and the messages."

    exit 1
else
    echo "Found $INPUT_FILE!"
fi

# === Embed the randomly generated text into the clean files ===
echo 'Creating stego files...'
while IFS="," read -r FILE_PATH STRING; do
    FILE_PATH=$(echo "$FILE_PATH" | xargs)
    STRING=$(echo "$STRING" | xargs)

    mkdir -p "$(dirname data/stego/$FILE_PATH)"

    stegano-lsb hide -i "data/clean/$FILE_PATH" -m "$STRING" -o "data/stego/$FILE_PATH"
done < "$INPUT_FILE"

echo 'Done!'
