#!/bin/bash

# === Config ===
DATASET_URL="https://www.kaggle.com/api/v1/datasets/download/pavansanagapati/images-dataset"
ZIP_FILE="dataset.zip"
TARGET_DIR="data/clean"

# === Download ===
echo "Downloading dataset from $DATASET_URL..."
curl -L -o "$ZIP_FILE" "$DATASET_URL"

# === Clean directory ===
if [ -d "$TARGET_DIR" ]; then
    echo "Cleaning existing directory: $TARGET_DIR"
    rm -rf "$TARGET_DIR"
fi
mkdir -p "$TARGET_DIR"

# === Extract ===
echo "Extracting $ZIP_FILE into $TARGET_DIR..."
unzip -q "$ZIP_FILE" -d "$TARGET_DIR"

# === Flatten directory structure if needed ===
NESTED_DIR="$TARGET_DIR/data"
if [ -d "$NESTED_DIR" ]; then
    echo "Flattening directory structure..."
    mv "$NESTED_DIR"/* "$TARGET_DIR"/
    rm -rf "$NESTED_DIR"
fi

echo "Removing zip file..."
rm -f $ZIP_FILE

echo "Creating directory for stego'd data..."
mkdir "data/stego"

echo "Done!"
