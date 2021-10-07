from bs4 import BeautifulSoup as BS
import json
from json.decoder import JSONDecodeError
import logging
import pickle
import requests
from requests.exceptions import *
import sys
import time

logging.basicConfig(
    filename='./logs/graph.log', 
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

class Graph():
    """ 
    Graph class to build graph using Wikipedia API.
    """
    def __init__(self):
        self.adj_list = {}
        self.window = []
        self.url = 'https://en.wikipedia.org/w/api.php?format=json&action=parse&prop=sections&page='
        self.parse_url = 'https://en.wikipedia.org/w/api.php?action=parse&page='
        self.json_url = '&format=json&section='
        self.not_ascii = []

    class GraphError(Exception):
        """
        GraphError class for all errors related to adj_list.
        """
        def __init__(self, *args):
            self.message = args[0]
            super().__init__(self.message)

        def __str__(self):
            return 'Graph Error: {0} '.format(self.message)
    
    def write_adj_list(self, output_file="HW1/Q1/python/graph.pickle"):
        """ 
        Write adj_list to pickle file
        """
        if not self.adj_list:
            raise self.GraphError("Graph is empty.")
        with open(output_file, 'wb') as output_file:
            pickle.dump(self.adj_list, output_file)

    def start(self, origin='Book of Genesis', end='Book of Revelation'):
        """
        Initialize web api search.
        """
        self.search(origin, end)

    def search(self, origin, end):
        """
        Enqueue origin.
        Current entry must be str in ascii.
        While queue, explore current entry for list of edge links (See also). 
        """
        
        def explore(entry):
            """
            Enqueue entry links (See also).
            """
            try:
                idx = get_index(entry)
                get_url = self.parse_url + entry + self.json_url + idx
                page = requests.get(get_url)
                j_page = page.json()
                j_links = j_page['parse']['text']['*']
                soup = BS(j_links, 'html.parser')
                links = soup.find_all('ul')[-1]
                arr = []
                for link in links.find_all('li'):
                    arr.append(link.get_text())
                    if len(self.adj_list) < 5000:
                        stack.append(link.get_text())
                self.adj_list[entry] += arr
            except JSONDecodeError as info:
                logger.info(info)
                return
            except RequestException as err:
                logger.error(err)
                return
            except KeyError as err:
                logger.info(err)
                return
            except TypeError as err:
                logger.error( " NoneType error: {} - {}".format(entry, idx))
                return
            except IndexError as err:
                logger.error(" IndexError {}".format(err))
                return
        
        
        def get_index(entry):
            """
            To retrieve the links (See also), the Wikipedia API needs the section index.
            """
            entry_url = self.url + entry
            """ Error on requests. Error on JSON decode. """
            try:
                request = requests.get(entry_url)
                request.raise_for_status()
                sections = request.json()['parse']['sections']
                for section in sections:
                    if section['anchor'] == 'See_also':
                        return section['index']
            except RequestException:
                raise RequestException(" Entry Request Error: {0}".format(entry))
            except JSONDecodeError:
                raise JSONDecodeError(" Entry JSON decode error: {0}".format(entry), request.text, 0)
            except KeyError:
                raise KeyError(" Entry KeyError: {0}".format(entry_url))
        
        stack = [origin]
        while stack:
            entry = stack.pop(0)
            if entry == end:
                break
            if entry.isascii() and entry not in self.adj_list:
                self.adj_list[entry] = []
                """
                TO DO: Implement error handling and error catching
                """
                explore(entry)
                time.sleep(2)
            elif not entry.isascii():
                logger.info(" Not ascii: {}".format(entry))
            elif entry in self.adj_list:
                logger.info(" Duplicate: {}".format(entry))
            print("The size of the dictionary is {} bytes".format(sys.getsizeof(self.adj_list)))        

if __name__ == "__main__":
    g = Graph()
    g.start()
    g.write_adj_list()
   
   