
# my-elasticsearch
## Overview

The goal of this project is to implement a primitive version of the elasticsearch. This project is purely for educational purposes and is not to be used in any production environment.

While simplistic, this projects should be very modular and open for future extensions, even if none will come.

## The Requirements

The project consists out of x main parts:

1. Database - functionality to store data and use it for search purposes.
	1. Add documents.
	2. Delete documents.
	3. Clear the entire database.
	   
2. Search engine - functionality to query the database with a specific query and return the result.
   For simplicity, only one type of search will be available - word match, which will return documents with the closest word match, where longer words have more weight.
   
	1. The algorithm to handle the search
	2. Search across all documents.
	3. Search across a specific document.
	4. Limit query output.
	   
3. CLI interface - the program will be accessed from the cli interface.

