# Lyrics Search

### Purpose

A GUI tool to search for patterns all the lyrics text files.

### Operation

_The program runs a GUI in the macbook and a CLI in the pi-nodes._

Place the text files in `<programroot>/testdata/` for now.

On the macbook;
* run `lyricsearch_mac.py`.
* type in the exact pattern to search for.
* click the "search" button.
* results show up in `<programroot>/results/`.
* the name of the search result text file is the string you searched for.

On the pi-nodes;
* pi-nodes are headless; ssh into them.
* go to "/home/pi/lyricsearch/"
* run `lyricsearch_pi.py`
* type in the search pattern into the terminal and press "Enter".

### To do
* change "run" command in root dir to point to "lyricsearch.py"
* make a set of words from all the lyrics from all the nodes
* make module that searches for the pattern in a collection of files that may already have the results previously searhced for.
* presearch for some common strings in anticipation of future requests.
* copy that set to all the nodes
  * when searching for a pattern, check that the words exist in the set first.
* make a regex that allows for searching a pattern of words within a list
  * ex; as ... as
  * as tall as
  * as big and tall as
* Run "multicoresearch_mac.py" on one fourth of the full data to compare against the pi-nodes. 
* save the results files with the name of the given search pattern.

### Process
#### Distribute the files among the nodes
1. Divide all the files as evenly as possible among 4 dirs
  * run `evenlydividework.py`
2. Load the newly created dirs onto 4 USB's (because I have 4 pi-nodes)
  * done manually (finished, one-time operation) 
3. Copy "evenlydividework.py" to the nodes
  * done manually (finished, one-time operation) 
4. Divide all the files on each node again into 4 smaller dirs
  * run `evenlydividework.py`


#### Begin a search (manual way)
__not finished after this point__
1. run the search through the `run` command in the root dir or directly through the main programs as listed below;
  * This takes about 3 to 3.5 hours on the cluster.
  * run on a pi-node
    * run `${HOME}/lyricsearch/mulitcoresearch_pi.py`
  * run on the macbook
    * run `${HOME}/lyricsearch/multicoresearch_mac.py`
2. After the search is complete;
  * run `python3 src/simplecluster.py -c`
3. At this point, the results are combined on each node.
  * run `python3 src/simplecluster.py -t`
  * transfers/combines cluster results to the macbook.

#### Begin a search (automated way)
1. run `src/mainlryicsearch.py`
  * need to create subprocesses at line 64 in customcluster.py?
    * to start the other nodes?

# Developer Notes
* The overall structure of the program is illustrated in "diagram.mdj"
* The search functions are, in order;
  * mac search      (searches only on the mac)
  * cluster search  (sends search commands to all nodes from the mac)
  * pi search       (starts the worker subprocesses on a node)
  * worker search   (the actual search that is performed in a node's core)
* Performs pattern search concurrently using pi-cluster. 
* Performs pattern search sequentially using macbook.
* Creates `<programroot>/results/` 
* Creates text files in `<programroot>/results/`

### other notes
* file copy time =  12.2 hours (44000 secs) to evenly divide 616,000 files among 4 dirs on the macbook.
* running the search on the mac (with debug = True), took <= 2 hours
* lyric search time using `multicoresearch_pi.py` on a pi-node took about 3.5 hours (12700 secs). 
