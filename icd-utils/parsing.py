
import time
import json as json
import collections


class parsing(object):
    
    '''This class is a single node parser with:
            id - foundation url id
            title - title of the node
            defination - defination of the node
            synonyms - synonyms found in the literature
            children nodes - list of all child nodes
            parent nodes - list of all parent nodes
            (single node falls under multiple parents)
     '''
    
    def __init__(self,raw_node,id2code):
        self.raw_node = raw_node
        self.id2code = id2code
        self.node_dict = {}
        
        
    '''get foundation id'''
    def get_id(self):
        self.id = self.raw_node["@id"].split("/")[-1]
        self.node_dict['id'] = self.id
        
        
    '''get code'''
    def get_code(self):
        self.get_id()
        self.node_dict['code'] = self.id2code[self.id]
        
        
    '''get title of the node'''
    def get_title(self):
        self.node_dict['title'] = self.raw_node['title']["@value"]
    
    '''find defination of node'''
    def get_defn(self):
        defn = self.raw_node["definition"]
        if defn != "Key Not found":
            self.node_dict['defn'] =  defn["@value"]
        else:
             self.node_dict['defn'] = defn
    
    '''collect the synonyms'''
    def get_syns(self):
        synonym = self.raw_node["synonym"]
        if synonym != "Key Not found":
            syn_list = []
            for t in synonym:
                syn_list.append(t["@value"])
        else:
            syn_list = "Key Not found"
        self.node_dict['syns'] =  syn_list
    
    
    '''get all child nodes foundation id'''
    def get_childs(self):
        child_ids = []
        child_urls = self.raw_node['child']
        if child_urls != "Key Not found":
            for url in child_urls:
                child_ids.append(url.split("/")[-1])
        else:
            child_ids = "Key Not found"
        self.node_dict['childs'] = child_ids
    
    
    '''get all parent nodes foundation id'''
    def get_parents(self):
        parent_ids = []
        parent_urls = self.raw_node['child']
        if parent_urls != "Key Not found":
            for url in parent_urls:
                parent_ids.append(url.split("/")[-1])
        else:
            parent_ids = "Key Not found"
        self.node_dict['parents'] =  parent_ids
        
        
    '''get node dictionary'''
    def get_node_doc(self):
        self.get_id()
        self.get_code()
        self.get_title()
        self.get_defn()
        self.get_syns()
        self.get_childs()
        self.get_parents()