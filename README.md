# Lyrics Search

* A GUI tool. 
* Performs string search recursively in `<cwd>/testlyrics/`. 
* Creates `<cwd>/results/` 
* Creates text files in `<cwd>/results/`

### Purpose

To search for a given pattern in all of the lyrics files.

### Operation

* in the program's root dir, place any text file in `<root>/lyrics/`.
* run `search.py`.
* type in the exact pattern to search for.
* click the "search" button.
* a list of files where the search pattern is found will appear in `<root>/results/`.

### To do
* make a set of words from all the lryics from all the nodes
* copy that set to all the nodes
  * when searching for a pattern, check that the words exist in the set first.
* make a regex that allows for searching a pattern of words within a list
  * ex; as ... as
  * as tall as
  * as big and tall as
* standardized the dir for the data in all the files.
* make a module to put in the nodes that uses multiprocessing.py
