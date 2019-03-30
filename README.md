# Lyrics Search
_Personal Note: This program combines code taken from musicdatabase/ and raspberrypicluster/_

### Purpose
Works as a GUI or CLI tool on the Macbook and as a CLI on the Raspberry Pi.
Searches for patterns in all the lyrics text files.

### Operation
#### High Level Overview
Macbook:
  * A gui is opened (manually have to open the CLI).
  * Enter a sentence.
  * The sentence is sent to each pi-node as a string through a subprocess.
Pi-nodes:
  * A cli program is started.
  * Enter a sentence (enclose the sentence in double quotes).
  * The sentence is converted to a string.
  * The string is converted to a set of words (punctuation included).
  * There are 100 mini shelve databases that contain the sets. These are searched for subset matches of the pattern.
  * If a match is possible (a subset exists), then a path is saved for the next step.
  * An exact match search is performed on all the saved paths where a subset was found.
  * If an exact match is found, then the song's path is saved to a file in `SET_DIR`.

### Preparing the Data
The pi-nodes have 1GB RAM, therefore the data needs to be set up before a search is performed.
There are 616,323 text files.
The text files are divided into 16 dirs (4 for each pi-node).
Each pi-node will have 4 dirs, and these 4 dirs are divided into 100 mini sets kept in shelve databases in `SET_DIR`.

#### On macbook
To divide the text files;
  * Run fairlydivide.py
    * This will divide all of the text files into the number of directories you specify.
    * Choose 16 blocks.
Divide the data among the pi-nodes.
  * 4 (block) dirs to each pi-node.
  * Manually copy to the nodes with `scp -r <dir> $<pi>:<dest>`
#### On the pi-nodes
  * Make sure any shelve databases transferred from the macbook to the pi have been deleted from the pi (db.gnu error?).
  * Run `python3.7 fairlydividesets.py 100`
  * This takes less than one hour to complete.
  * This is to prevent running out of RAM on the pi.

### Issues
* wxpython - need to read more on this one. This library is not like Tkinter, in my opinion.
  * Make the gui cleaner, nicer to look at.






(rework the instructions below)
### Normal search on macbook
* Turn on pi-cluster.
* Connect "MONTHLY" external device.
* Check `constants.DEBUG == False`.
* Run `python3.7 guisearch.py`.
  * Working on changing to `python3.7 wxgui.py`.
* Type in the exact pattern to search for.
  * For now, it only performs an exact search.
* Click the "search" button.
* Results are written to `<programroot>/results/`.
  * New text files are created here.
  * The name of the file is the pattern that was searched for.

### Debug search on macbook
* Connect "MONTHLY" external device.
* Check `constants.DEBUG == True`.
* Run the gui script.
* Type in the exact pattern to search for.
* Click the "search" button.
* Results are written to `<MONTHLY>/pylyricresults/`.
  * New text files are created here.
  * The name of the file is the pattern that was searched for prepended with an asctime stamp.

### Performing search on pi-node
* SSH into a node from macbook.
  * Pi-nodes are headless.
* Go to "/home/pi/lyricsearch/"
* Run `python3 clisearch.py`
  * The gui will not run on the pi-node directly.
* Type in the search pattern into the terminal and press "Enter".

### To do
* change "run" command in root dir to point to "lyricsearch.py"
* presearch for some common strings in anticipation of future requests.
* make bash script that copies dirs to all the pi-nodes.
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
* Searching through all the sets on the pi-cluster usually takes less than 5 minutes.
* The exact search part of the process takes the longest as it opens up each text file. 
  * If there are a lot of exact matches, then it could take hours.
  * When searching, it is best to have more than one word.
  * If you have a common pattern to search for, then it will increase the chances of having more possible matches, which means that more exact match searches will be performed which increases the time to return a list of results.
* New, set-search method:
  * Creating the block-sets on a pi-node took less than 2000 seconds.
  * Searching through 100 block-sets for a possible match on a pi-node took about 110 seconds.
  * Searching, overall, takes less than five minutes which is a big leap down from the original 3.5 hours.
