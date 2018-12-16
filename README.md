# Lyrics Search
* A GUI tool. 
* Performs pattern search concurrently using pi-cluster. 
* Creates `<rootdir>/results/` 
* Creates text files in `<rootdir>/results/`

### Purpose

To search for a string in all of the lyrics files.

### Operation

_The program runs a GUI in the macbook and a CLI in the pi-nodes._

Place the text files in `<rootdir>/testdata/` for now.

On the macbook;
* run `lyricsearch_mac.py`.
* type in the exact pattern to search for.
* click the "search" button.
* results show up in `<rootdir>/results/`.
* the name of the search result text file is the string you searched for.

On the pi-nodes;
* pi-nodes are headless; ssh into them.
* go to "/home/pi/lyricsearch/"
* run `lyricsearch_pi.py`
* type in the search pattern into the terminal and press "Enter".

### To do
* make a set of words from all the lyrics from all the nodes
* copy that set to all the nodes
  * when searching for a pattern, check that the words exist in the set first.
* make a regex that allows for searching a pattern of words within a list
  * ex; as ... as
  * as tall as
  * as big and tall as
* standardized the dir for the data in all the files.
* make a module to put in the nodes that uses multiprocessing.py

### Process
1. Divide all the files as evenly as possible among 4 dirs
  * run `evenlydividework.py`
2. Load the newly created dirs onto 4 USB's (because I have 4 pi-nodes)
  * do this manually for now (basically only needs to be run once)
3. Copy "evenlydividework.py" to the nodes
4. Divide all the files on each node again into 4 smaller dirs
  * run `evenlydividework.py`
  * change the file paths where they will save to
5. 

### other notes
* copy time =  12.2 hours (44000 secs) to evenly divide 616,000 files among 4 dirs on the macbook.
* Running `multi_test.py` on a pi-node took about 3.5 hours (12700 secs). At least thats better than 12 hours on the macbook.
