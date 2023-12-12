#!/bin/bash

clean_items=("__pycache__")

for item in "${clean_items[@]}"; do
    if [ -e "$item" ]; then
        if [ -d "$item" ]; then
            rm -r "$item"
            echo "Removed: $item"
        elif [ -f "$item" ]; then
            rm "$item"
            echo "Removed: $item"
        else
            echo "Unknown type: $item"
        fi
    fi
done

echo "Cleaned successfully."