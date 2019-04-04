# Lyrics Search
A CLI tool that performs an exact pattern search in lyrics text files.

## Purpose
To get a list of songs that contain a pattern.

## Operation
Run `$ ./main.py pattern` where "pattern" is the exact string you are searching for.

# Developer notes
_Edit this_
* The overall structure of the program is illustrated in "diagram.mdj"
* The search function hierarchy is;
  * mac search      (searches only on the mac, sequential)
  * cluster search  (sends search commands to all nodes from the mac)
  * pi search       (starts the worker subprocesses on a node, concurrent)
  * worker search   (the actual search that is performed in a node's core)
* Creates `<programroot>/results/` 
* Creates text files in `<programroot>/results/`

## High level overview
### Preparing the data
The pi-nodes have 1GB RAM, therefore the data needs to be set up before a search is performed.
There are 616,323 text files.
The text files are divided into 16 dirs (4 for each pi-node).
Each pi-node will have 4 dirs, and these 4 dirs are divided into 100 mini sets kept in shelve databases in `SET_DIR`.

### Setup process
#### Distribute the files among the nodes
1. Divide all the files as evenly as possible among 4 dirs
  * run `python3 fairlydivide.py`
2. Load the newly created dirs onto 4 USB's (because I have 4 pi-nodes)
  * done manually (finished, one-time operation) 
3. Copy "fairlydivide.py" to the nodes
  * done manually (finished, one-time operation) 
4. Divide all the files on each node again into 4 smaller dirs
  * run `python3 fairlydivide.py`

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
  * Run `$ ./fairlydividesets.py 100`
  * This takes less about 3 hours to complete.
  * This is to prevent running out of RAM on the pi.

## Known issues
* The pi-nodes slow down after having searched around 20 - 30 sets, so I clear the OS's buffer and cache to prevent this.
* Clearing the buffer and cache works well for dividing the lyrics into the block sets, but I suspect an issue may occur when performing many pattern searches later.

## Searching on macbook
* Turn on pi-cluster.
* Connect "MONTHLY" external device.
* Check `constants.DEBUG == False`.
* Check `constants.VERBOSE == True`.
* Run `./main.py <pattern>`.
  * For now, it only performs an exact search.
* Results are written to `<MONTHLY>/pilyricsresults/`.
  * New text files are created here.
  * The name of the file is `timestamp + pattern`

## Searching on pi-node
* SSH into a node from macbook.
  * Pi-nodes are headless.
* Go to "/home/pi/lyricsearch/"
* Run `python3 clisearch.py`
  * The gui will not run on the pi-node directly.
* Type in the search pattern into the terminal and press "Enter".

## To do
* presearch for some common strings in anticipation of future requests.
* make a regex that allows for searching a pattern of words within a list and the pattern does not need to be an unbroken string.
  * ex; as ... as
  * as tall as
  * as big and tall as

## Other notes
_Personal Note: This program combines code taken from musicdatabase/ and raspberrypicluster/_
* Searching through all the sets on the pi-cluster usually takes less than 5 minutes.
* The exact search part of the process takes the longest as it opens up each text file. 
  * If there are a lot of exact matches, then it could take hours.
  * When searching, it is best to have more than one word.
  * If you have a common pattern to search for, then it will increase the chances of having more possible matches, which means that more exact match searches will be performed which increases the time to return a list of results.
* New, set-search method:
  * Creating the block-sets on a pi-node took less than 2000 seconds.
  * Searching through 100 block-sets for a possible match on a pi-node took about 110 seconds.
  * Searching, overall, takes less than five minutes which is a big leap down from the original 3.5 hours.
* The progress bar code was taken from somewhere on Stack Overflow. It is much better than what I was using and I can't remember where I found it. Should I find it again, then I will include a link to it here.
