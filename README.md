# my-elasticsearch

## Overview

The goal of this project is to implement a primitive version of the elasticsearch. This project is purely for educational purposes and is not to be used in any production environment.

While simplistic, this projects should be very modular and open for future extensions, even if none will come.

## How to run

1. Install the project with `poetry install`
2. Use the `poetry run cli` to access the CLI. It will show you the schema of
   the project. The thing that interests you the most is the `COMMANDS` section.

3. Pick a command from the `COMMAND` section and run it.

   For example:
   `poetry run cli insert_document --name='MyDocument' --content='I love reading
tutorials'`

   If the command you want to run requires some arguments, it will let you know.

The basic commands are the `insert_document` and `search`. The `insert_document`
populates the database with documents, and the `search` command allows you to
search through your documents with a query.

## The Requirements

The project consists out of x main parts:

1. Database - functionality to store data and use it for search purposes.
   1. Add documents.
   2. Delete documents.
   3. Clear the entire database.
2. Search engine - functionality to query the database with a specific query and return the result.
   For simplicity, only one type of search will be available - word match, which will return documents with the closest word match, where longer words have more weight.

   1. The algorithm to handle the search
   2. Search across a specific collection.
   3. Limit query output.

3. CLI interface - the program will be accessed from the cli interface.
