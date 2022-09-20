import csv
import requests

def struct_url(function, ticker_lst, interval, slice = [], outputsize = "full", datatype = "csv", apikey = "TACZtZi8hd383vPZAVTsyxKLrbSaCdvqK6", url = "https://www.alphavantage.co/query?"): 
    if len(slice) == 0: 
        url_dict = {i: f"{url}function={function}&symbol={i}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={apikey}" for i in ticker_lst}
    elif len(slice) > 0:
        url_dict = {i: {j: f"{url}function={function}&symbol={i}&interval={interval}&slice={jalue}&outputsize={outputsize}&datatype={datatype}&apikey={apikey}" for j, jalue in enumerate(slice)} for i in ticker_lst}
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


#test case 
function = "TIME_SERIES_INTRADAY_EXTENDED"
ticker_lst = ["IBM", "AAPL"]
interval = "1min"
slice = [f"year1month{i}" for i in range(1, 4)]
outputsize = "compact"
test = struct_url(function, ticker_lst, interval, slice = slice, outputsize = outputsize)

test_url = test["IBM"][0]
test_obj = get_csv_data(test_url)


