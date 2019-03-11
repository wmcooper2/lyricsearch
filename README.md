# Lyrics Search
_Personal Note: This program combines code taken from musicdatabase/ and raspberrypicluster/_

### Purpose

A GUI tool to search for patterns all the lyrics text files.

### Operation

_The program runs a GUI in the macbook and a CLI in the pi-nodes._

### Performing search from the macbook
* Turn on pi-cluster.
* Connect "MONTHLY" external device.
* Check `constants.DEBUG == False`.
    * if True: performs lyric search on smaller set of data in "MONTHLY".
* Run `python3 guisearch.py`.
* Type in the exact pattern to search for.
    * for now, it only performs an exact search.
* Click the "search" button.
* Results are written to `<programroot>/results/`.
    * new text files are created here.
    * the name of the file is the pattern that was searched for.

### Performing search from the pi-nodes
* SSH into a node.
    * pi-nodes are headless.
    * if you want to use a gui, then connect a monitor to the node directly before turning on the node.
* go to "/home/pi/lyricsearch/"
* run `python3 clisearch.py`
    * `python3 guisearch.py` will just run `python3 clisearch.py` anyway if run directly on a node.
* type in the search pattern into the terminal and press "Enter".

### To do
* change "run" command in root dir to point to "lyricsearch.py"
* make a set of words from all the lyrics from all the nodes
    * make module that searches for the pattern in a collection of files that may already have the results previously searched for.
    * presearch for some common strings in anticipation of future requests.
    * copy that set to all the nodes
      * when searching for a pattern, check that the words exist in the set first.
      * an exact match cannot be found if a word does not exist in the set, so search that set first for faster results.
* make a regex that allows for searching a pattern of words within a list
    * ex; as ... as
    * as tall as
    * as big and tall as

## Setup Process
### Distribute the files among the nodes
1. Divide all the files as evenly as possible among 4 dirs
    * run `python3 fairlydivide.py`
2. Load the newly created dirs onto 4 USB's (because I have 4 pi-nodes)
    * done manually (finished, one-time operation) 
3. Copy "fairlydivide.py" to the nodes
    * done manually (finished, one-time operation) 
4. Divide all the files on each node again into 4 smaller dirs
    * run `python3 fairlydivide.py`

### Manual Search 
__not finished after this point__
1. run the search through the `run` command in the root dir or directly through the main programs as listed below;
    * This takes about 3 to 3.5 hours on the cluster.
    * run on a pi-node
      * run `${HOME}/lyricsearch/clisearch.py`
    * run on the macbook
      * run `${HOME}/lyricsearch/clisearch.py`
2. After the search is complete;
    * run `python3 src/simplecluster.py -c`
3. At this point, the results are combined on each node.
    * run `python3 src/simplecluster.py -t`
    * transfers/combines cluster results to the macbook.

### Automatic Search
1. run `python3 src/guisearch.py`

### Developer Notes
* The overall structure of the program is illustrated in "diagram.mdj"
* The search function hierarchy is;
    * mac search      (searches only on the mac, sequential)
    * cluster search  (sends search commands to all nodes from the mac)
    * pi search       (starts the worker subprocesses on a node, concurrent)
    * worker search   (the actual search that is performed in a node's core)
* Creates `<programroot>/results/` 
* Creates text files in `<programroot>/results/`

### other notes
* file copy time =  12.2 hours (44000 secs) to evenly divide 616,000 files among 4 dirs on the macbook.
* lyric search time using `clisearch.py` on a pi-node took about 3.5 hours (12700 secs). 
* Searching through sets of the songs words is faster for finding potential matches. After a set search, then perform an exact match search.
