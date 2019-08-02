import time
import requests
import json as json


class download(object):
    
    ''' Class to download ICD-11 data. Parameters considered:
        config: includes CLientID and ClientSecret Credentials needed to 
                get access to ICD codes
                
        token : token is generated throught request.post method
        
        single node document: it can be requested one at a time
        
        recursive walk is performed by implementing:
                - 'set walker' to start recursive walk
                - 'get node doc' to get single node document
                - 'recursive walk' to collect all node documents
    '''
    
    def __init__(self,config):
        self.config = config
        
        
        
    '''Set the token for headers'''   
    def set_headers(self):
        '''make request'''
        token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
        r = requests.post(token_endpoint,\
                  data= {'client_id': self.config["ClientId"],\
                         'client_secret': self.config["ClientSecret"],\
                         'scope': 'icdapi_access',\
                         'grant_type': 'client_credentials'},\
                          verify=True).json()

        '''get token'''
        token = r['access_token']
        
        '''HTTP header fields to set'''
        self.headers = {'Authorization':  'Bearer '+ token, 
                       'Accept': 'application/json', 
                       'API-Version':'v2',
                       'Accept-Language': 'en'}
        
        
    '''Perform a single download'''    
    def get_node_doc(self,url):
        '''make request '''          
        r = requests.get(url, headers=self.headers, verify=True)
        return r.json() 
    
    '''set the walker with initial step'''
    def set_walker(self,root_url,is_dump = True,is_foot_print=False):
        self.is_dump =is_dump
        self.is_foot_print = is_foot_print
        
        root_id = root_url.split("/")[-1]
        
        walk_path0 = root_id
        foot_print0 = root_id
        
        '''supply the address of datafiles'''
        if self.is_dump:
            self.tfile = open("data/" + root_id + ".txt",'w')
            self.jfile = open("data/" + root_id + ".json",'w')
            self.logfile = open("data/log_" + root_id + ".json",'w')
            
        return walk_path0,foot_print0
        
        
    def recursive_walk(self,url,walk_path,foot_print):
    
        '''Find ID'''
        walk_id = url.split("/")[-1]
        result = self.get_node_doc(url)
        walk_path = walk_path+"."+ walk_id
    
        self.logfile.write("Downloading : " + url)
        self.logfile.write("\n")
        
    
        if self.is_foot_print:
            foot_print = foot_print + " - "
            print(foot_print  + walk_id)
    
        if self.is_dump:
            '''Dump data to json file'''
            json.dump(result,self.jfile)
            self.jfile.write("\n")
            '''Write down all ID and titles'''
            self.tfile.write(walk_path)
            self.tfile.write("\n")
    
       
        '''Recursion over all tree branches'''
        if 'child' in result.keys():
            child_urlset = result['child']
            if len(child_urlset)>0:
                for child_url in child_urlset:
                    self.recursive_walk(child_url,walk_path,foot_print)
        return     
        
        
        
        