import json
import logging
import os
import pickle
from pickle import UnpicklingError
import sqlite3

logging.basicConfig(
    filename='upload.log', 
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()



class Upload():
    
    def __init__(self, graph_dict=None):
        self.graph_dict = graph_dict
        self.graph = {}
        self.nodes = []
        self.links = []

    def unpickle(self, file_name):
        try:
            with open(file_name, 'rb') as pickle_file:
                self.graph_dict = pickle.load(pickle_file)
        except (OSError, IOError) as err:
            logger.info(" {}".format(err))
            return
        except UnpicklingError as err:
            logger.info(" {}".format(err))
            return
    
    def init_graph(self):
        temp = {}
        for idx, key in enumerate(self.graph_dict.keys()):
            temp[key] = idx
        for key, values in self.graph_dict.items():
            self.nodes.append({'id': temp[key], 'name': key})
            for value in values:
                if value in temp:
                    self.links.append({'source': temp[key], 'target': temp[value]})
        self.graph['nodes'] = self.nodes
        self.graph['links'] = self.links
    
    def write_file(self):
        try:
            with open ('graph.json', 'w') as node_file:
                json.dump(self.graph, node_file, indent=4)
        except (OSError, IOError) as err:
            logger.info(" {}".format(err))
            return
        
    def upload(self, db_name):
        drop_table = 'drop table if exists dictionary'
        create_table = 'create table dictionary (entry TEXT NOT NULL)'
        try:
            conn = sqlite3.connect(db_name)
            cr = conn.cursor()
            cr.execute(drop_table)
            cr.execute(create_table)
            for key in self.graph_dict.keys():
                try:
                    sql = "insert into dictionary (entry) values ('{}')".format(key)
                    cr.execute(sql)
                except:
                    sql = "insert into dictionary (entry) values ('{}')".format(key.replace("'", ""))
                    cr.execute(sql)
            conn.commit()
        except Exception as err:
            logger.info(" {}".format(err))

if __name__ == "__main__":
    up = Upload()
    up.unpickle('graph.pickle')
    up.init_graph()
    up.write_file()
   


