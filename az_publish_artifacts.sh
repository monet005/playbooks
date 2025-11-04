#!/bin/bash

ORG_URL="https://dev.azure.com/teamvelasco05/"
PROJECT="Testlab"
FEED="testlab"

for file in *.zip; do
    NAME=$(basename "$file")
    VERSION="0.0.1"

    mkdir -p tmp_publish
    cp "$file" tmp_publish/

    echo "Publishing $file ..."
    if az artifacts universal publish \
        --organization "$ORG_URL" \
        --project "$PROJECT" \
        --feed "$FEED" \
        --name "$NAME" \
        --version "$VERSION" \
        --description "$file" \
        --scope project \
        --path tmp_publish
    then
        echo "$file has been published successfully."
    else
        echo "Publishing of $file got failed. Skipping..."
    fi 

    rm -rf tmp_publish
done



