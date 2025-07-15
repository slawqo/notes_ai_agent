
#!/bin/bash

# Usage: ./process_documents.sh /path/to/directory

DIR="${1:-.}"

find "$DIR" -type f -name "*.md" | while read -r file; do
    echo "Processing: $file"
    notes_ai_agent "$file"
done
