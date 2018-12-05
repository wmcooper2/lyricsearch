# Lyrics Search
_Old, need to update to include picluster_
* A GUI tool. 
* Performs pattern search concurrently using pi-cluster. 
* Creates `<cwd>/results/` 
* Creates text files in `<cwd>/results/`

### Purpose

To search for a given pattern in all of the lyrics files.

### Operation
_Old, need to update_

_The program runs a GUI in the macbook and a CLI in the pi-nodes._

On the macbook;
* run `lyricsearch.py`.
* type in the exact pattern to search for.
* click the "search" button.






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
* copy time =  44095 seconds to evenly divide 616,000 files
