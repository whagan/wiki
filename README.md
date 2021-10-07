# Wiki API Scrape

* `git clone git@github.com:whagan/wiki.git`
* `cd wiki`
* `virtualenv venv && source venv/bin/activate` (optional python virtual environment)
* `pip install -r requirements.txt`
* `python graph.py`

This program uses Wikipedia's API to collect *See also* links for individual Wikipedia pages. These pages and links represent a directed graph. For instance, a user may reach *Predictive Analytics* from *Data visualization* using only Wikipedia's *See also* links:

*Data visualization* -> *Data analysis* -> *Predictive analysis* 

The program is a long-running script. If an endpoint is specified, the program terminates when it is found. Otherwise the program may continue searching without end. The program creates and records to *graph.log* as it executes:

![graph.log](./img/graph_log.PNG)

The graph it produces is stored in *wiki_nodes_links.json* and looks like this:

![](./img/wiki_nodes_links_json.PNG)

A pickle file is also created.

Let's get biblical: Does a path exist between *Book of Genesis* and *Book of Revelation*? 

The program is a long-running script. It creates and records to *graph.log* as it executes. The BFS can grow 