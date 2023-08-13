#Installation

To install, simply use
pip install -r requirements.txt

#Deploy a New Version

To build an up to date version of the website, add missing talks to talks.csv, and then run (from the root directory)
python scripts/build.py, and then push the new files to github.


#Testing the website locally
To test the website, go to the root directory and use the command

python -m http.server

Then go to here

http://0.0.0.0:8000/index.html
