# Music-Royalty Date Finder

This program finds the earliest published release date for a song using the Discogs and 
Spotipy APIs. This program only reads ".csv" files, so please ensure any files you send through
this program end in ".csv". 

#IMPORTANT FORMATTING INFO:
Currently, the program will only work with columns titled "WORK_TITLE" for 
the song name and "WRITERS" for the song writers. Please ensure the column titles in the .csv file matches 
those names respectively.

This program can also only work with files that use "UTF-8" encoding. The easiest way to check/change this 
is by opening your chosen file in Notepad and clicking "Save as", ensuring the encoding is listed as "UTF-8".

#Step 1:
Install the necessary packages by entering the following into your Python terminal:

```pip install spotipy```

```pip install discogs```

If these packages are installed properly, you will see a confirmation line at the bottom of your
terminal.

#Step 2:
Open your Python terminal and change your directory to the project file (this can be done by typing ```cd xxx``` where ```xxx```
represents the folder of the project).

#Step 3:
Once in the project directory, type ```python royalty.py xxx``` where ```xxx``` is the absolute path of 
your file. Your finished file will be in a folder titled "FinalSheets".      