#the usual suspects
import statistics
import csv
import pandas as pd

#api related
import requests
import concurrent.futures 

class alph_settings: 
    def __init__(self, apikey, site, date_range): 
        self.apikey = str(apikey) 
        self.site = str(site) 
        self.date_range = list(date_range)

class val_steps(alph_settings): 

    def get_tkers(self, function = "LISTING_STATUS", date_range = None):
        if date_range == None: 
            date_lst = sorted(self.date_range)
        else: 
            date_lst = sorted(date_range)
        #get range of tickers from dates provided
        lst_dict = {}
        for i in date_lst: 
            if i.month < 10 and i.day < 10:
                date_val = f"{i.year}-0{i.month}-0{i.day}"
            elif i.month < 10: 
                date_val = f"{i.year}-0{i.month}-{i.day}"
            elif i.day < 10:
                date_val = f"{i.year}-{i.month}-0{i.day}"
            else: 
                date_val = f"{i.year}-{i.month}-{i.day}"
            r = requests.get(f"{self.site}function={function}&date={date_val}&apikey={self.apikey}")
            decode_content = r.content.decode("utf-8")
            content = csv.reader(decode_content.splitlines(), delimiter = ",")
            lst_dict[i] = list(content)
        return lst_dict
    
    def get_valid_tkers(lst_dict): 
        key_lst = [i for i in lst_dict.keys()]
        len_lst = [len(lst_dict[i]) for i in key_lst]
        #logic to check shorter lists, can take more than two lists
        if statistics.mean(len_lst) < 1000: 
            compare_lst = lst_dict[key_lst[len_lst.index(max(len_lst))]]
            maintain_lst = []
            for i in compare_lst:
                for j, jalue in enumerate(key_lst): 
                    a_chk = []
                    if i in lst_dict[jalue]: 
                        a_chk = True
                    else: 
                        a_chk.append(jalue)
                if a_chk == True: 
                    maintain_lst.append(i)
                else: 
                    print(f"{i} was delisted in {min(a_chk)}")
        #write logic for longer lists but assume two dict keys only 
        else:
            for i in key_lst: 
                tker_mat = [lst_dict[i] for i in key_lst]
            mat1=set(tuple(x) for x in tker_mat[0])
            mat2=set(tuple(x) for x in tker_mat[1])
            maintain=set.intersection(mat1,mat2)
            delist=mat1^mat2
            maintain_lst=list(list(y) for y in maintain)
            for j in delist:
                print(f"Excluded: {j[0]}, {j[1]}")
        return maintain_lst

class alph_api_wrapper(alph_settings): 

    def get_search(self, kwd_lst, function = "SYMBOL_SEARCH"):
        url_dict = {i: f"{self.site}function={function}&keywords={i}&apikey={self.apikey}" for i in kwd_lst}
        raw_response = []
        res_dict = {}
        for j in url_dict.keys(): 
            r = requests.get(url_dict[j])
            req = r.json()
            raw_response.append(req)
            res_dict[j] = [req["bestMatches"][k]["1. symbol"] for k in range(len(req["bestMatches"]))]
        return url_dict, raw_response, res_dict

    def intraday_url(self, function, ticker_lst, interval, slice = [], outputsize = "full", datatype = "csv", output = "json"): 
        if len(slice) == 0: 
            if output == "json": 
                url_dict = {i: f"{self.site}function={function}&symbol={i}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for i in ticker_lst}
                return url_dict
            elif output == "lst": 
                url_lst = [f"{self.site}function={function}&symbol={i}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for i in ticker_lst]
                return url_lst
        elif len(slice) == 1: 
            print("here")
            if output == "json": 
                url_dict = {i: f"{self.site}function={function}&symbol={i}&slice={slice}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for i in ticker_lst}
                return url_dict
            elif output == "lst": 
                url_lst = [f"{self.site}function={function}&symbol={i}&slice={slice}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for i in ticker_lst]
        elif len(slice) > 0:
            if output == "json":
                url_dict = {i: {j: f"{self.site}function={function}&symbol={i}&interval={interval}&slice={jalue}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for j, jalue in enumerate(slice)} for i in ticker_lst}
                return url_dict
            elif output == "lst": 
                url_lst = "dummy"
                #url_lst = [[i, f"{self.site}function={function}&symbol={i}&interval={interval}&slice={jalue}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for j, jalue in enumerate(slice)] for i in ticker_lst]
                return url_lst

    def get_csv_data(url, pretty_print = False): 
        with requests.Session() as session: 
            load = session.get(url)
            decode = load.content.decode("utf-8")
            in_mem = csv.reader(decode.splitlines(), delimiter = ",")
            lst_data = list(in_mem)
            if pretty_print == False: 
                pass 
            elif pretty_print == True: 
                for row in lst_data[:50]: 
                    print(row)
            elif type(pretty_print) == int: 
                for row in lst_data[:pretty_print]: 
                    print(row)
            else: 
                print("Either bool or int, thanks. Skipping the print.")
                pass 
        return lst_data
