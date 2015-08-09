"""
Class to import various kinds of corpus
"""

import os as os

class WosCorpus(object):
    """
    Import WOS corpus
    """

    def __init__(self):
        self.count = 0
        self.corpus = []
        
    def add_wos(self, wosfile, directory = False):
        if not directory:
            self.corpus+=self.read_wos_file(wosfile)
        else:
            for i in os.listdir(wosfile):
                self.corpus+=self.read_wos_file(wosfile+"/"+i)
            
    def read_wos_file(self,wosfile):
        data = []
        articles = []
        with open(wosfile,"r") as f:
            data = f.readlines()
        data = [i.replace("\n","") for i in data]
        ref = self.articles(data)
        for i in ref:
            sub = data[i[0]:i[1]]
            art = self.extract(sub)
            articles.append(art)
        return articles
    
    def rank(self,code,sub):
        """
        Return the index of the first occurence of a key in a WOS structured file
        """
        return [i for i in range(0,len(sub)) if code+" " == sub[i][0:3]][0]

    def extract(self,sub):
        """
        Extract raw data from WOS unit
        """ 
        tmp = {}
        try:
            tmp["authors"] = [sub[i][3:].lower() for i in range(self.rank("AU",sub),self.rank("AF",sub))]
        except:
            tmp["authors"] = ["NA"]
        try:
            tmp["authors_full"] = [sub[i][3:].lower() for i in range(self.rank("C1",sub),self.rank("RP",sub))]
        except:
            tmp["authors_full"] = []
        try:
            tmp["bibliography"] = [sub[i][3:].lower() for i in range(self.rank("CR",sub),self.rank("NR",sub))]
        except:
            tmp["bibliography"] = []
        try:
            tmp["title"] = " ".join([sub[i][3:] for i in range(self.rank("TI",sub),self.rank("SO",sub))]).lower()
        except:
            tmp["title"] = "NA"
        try:
            tmp["journal"] = " ".join([sub[i][3:] for i in range(self.rank("SO",sub),self.rank("LA",sub))]).lower()
        except:
            tmp["journal"] = "NA"
        try:
            tmp["keywords1"] = (" ".join([sub[i][3:] for i in range(self.rank("DE",sub),self.rank("ID",sub))])).lower().split(";")
            tmp["keywords1"] = [u.strip() for u in tmp["keywords1"]]
        except:
            tmp["keywords1"] = []
        try:
            tmp["keywords2"] = (" ".join([sub[i][3:] for i in range(self.rank("ID",sub),self.rank("AB",sub))])).lower().split(";")
            tmp["keywords2"] = [u.strip() for u in tmp["keywords2"]]
        except:
            tmp["keywords2"] = []
        try:
            tmp["abstract"] = (" ".join([sub[i][3:] for i in range(self.rank("AB",sub),self.rank("C1",sub))])).lower()
        except:
            tmp["abstract"] = "NA"
        try:
            tmp["bibliography"] = [sub[i][3:].lower() for i in range(self.rank("CR",sub),self.rank("NR",sub))]
        except:
            tmp["bibliography"] = []
        try:
            tmp["year"] = " ".join([sub[i][3:] for i in range(self.rank("PY",sub),self.rank("VL",sub))]).lower()
        except:
            tmp["year"] = "0000"
        try:
            tmp["id"] = " ".join([sub[i][3:] for i in range(self.rank("DI",sub),self.rank("DI",sub)+1)]).lower()
        except:
            tmp["id"] = "NA"
        try:
            tmp["id_wos"] = " ".join([sub[i][3:] for i in range(self.rank("UT",sub),self.rank("UT",sub)+1)]).lower()
        except:
            tmp["id_wos"] = "NA"
        try:
            tmp["categories"] = (" ".join([sub[i][3:] for i in range(self.rank("WC",sub),self.rank("SC",sub))])).lower().split(";")
        except:
            tmp["categories"] = []
        return self.clean_data(tmp)
    
    def clean_data(self, article):
        """
        Clean the raw data extracted from WOS file and add meta information if needed
        """
        article["bibliography_clean"] = []
        for i in article["bibliography"]:
            tmp = i.split(",")
            if len(tmp)>3:
                article["bibliography_clean"].append("".join(tmp[0:3]))
            else:
                article["bibliography_clean"].append(i.replace(",",""))
        return article

    def articles(self,data):
        """
        Delimit the begin and the end of each articles in a plain text WOS file
        """
        starts = [i for i in range(0,len(data)) if data[i][0:3]=='PT ']
        return [(starts[i],starts[i+1]) for i in range(0,len(starts)-1)]+[(starts[-1],len(data))]
    
    def create_index(self):
        self.dict_bibliography = {}