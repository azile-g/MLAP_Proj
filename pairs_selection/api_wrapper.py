import csv
import requests
import copy

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
            r = requests.get(f"{self.site}function={function}&date={i}&apikey={self.apikey}")
            decode_content = r.content.decode("utf-8")
            content = csv.reader(decode_content.splitlines(), delimiter = ",")
            lst_dict[i] = list(content)
        return lst_dict

    def tker_maintain(lst_dict):
        key_lst = [i for i in lst_dict.keys()]
        maintain_lst = copy.copy(lst_dict[key_lst[0]])
        counter_lst = [0 for i in range(len(key_lst))]
        for j in range(len(lst_dict[key_lst[0]])): 
            chk_lst = [lst_dict[key_lst[i]][j][0] for i in range(len(key_lst))]
            for k in range(1, len(chk_lst)):
                if chk_lst[0] == chk_lst[k]: 
                    print(chk_lst[k])
                    pass
                else:
                    #maintain_lst.pop(j)
                    pass
        return maintain_lst

    def get_valid_tkers(lst_dict): 
        key_lst = [i for i in lst_dict.keys()]
        maintain_lst = []
        len_lst = [len(lst_dict[i]) for i in key_lst]
        compare_lst = lst_dict[key_lst[len_lst.index(max(len_lst))]]
        
        return compare_lst

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

    def intraday_url(self, function, ticker_lst, interval, slice = [], outputsize = "full", datatype = "csv"): 
        if len(slice) == 0: 
            url_dict = {i: f"{self.site}function={function}&symbol={i}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for i in ticker_lst}
        elif len(slice) > 0:
            url_dict = {i: {j: f"{self.site}function={function}&symbol={i}&interval={interval}&slice={jalue}&outputsize={outputsize}&datatype={datatype}&apikey={self.apikey}" for j, jalue in enumerate(slice)} for i in ticker_lst}
        return url_dict

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