#Installation

To install, simply use
pip install -r requirements.txt

#Generating talks.csv

How I made the list of all Bhante G's talks was by saving them in a bookmarks folder on firefox, and then exporting those bookmarks.
The parse booksmarks script will process that and do some title normalization, as well as generate talks.csv.

#Deploy a New Version

To build an up to date version of the website, add missing talks to talks.csv, and then run (from the root directory)
python scripts/build.py, and then push the new files to github.


#Testing the website locally
To test the website, go to the root directory and use the command

python -m http.server

Then go to here

http://0.0.0.0:8000/index.html
