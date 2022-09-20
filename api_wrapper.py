import csv
import requests

class alph_settings: 
    def __init__(self, apikey, site): 
        self.apikey = str(apikey) 
        self.site = str(site) 

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