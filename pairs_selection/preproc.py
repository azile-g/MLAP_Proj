import statistics 
import pandas as pd
from datetime import datetime

from api_wrapper import alph_settings

class filters(alph_settings): 

    def daily_filter(self, daily_data, pandas = True, ts_idx = 0, close_idx = 5, vol_idx = 6, header_row = 0): 
        start = self.date_range[0] 
        end = self.date_range[1]
        data_dict = {i: [[j[0], float(j[5]), int(j[6])] for j in daily_data[i][header_row+1:]] for i in daily_data.keys()}
        for i in data_dict.keys(): 
            data_dict[i] = pd.DataFrame(data_dict[i][header_row+1:], columns = [daily_data[i][header_row][0], daily_data[i][header_row][5], daily_data[i][header_row][6]])
            data_dict[i]["timestamp"] = pd.to_datetime(data_dict[i]["timestamp"])
            data_dict[i] = data_dict[i].query("@start <= timestamp <= @end")
        day_except = filters.debug_days(data_dict)
        for i in data_dict.keys(): 
            data_dict[i] = data_dict[i].query("timestamp != @day_except")
            data_dict[i] = data_dict[i].reset_index()
            if pandas == False:
                data_dict[i] = data_dict[i].values.tolist()
            else: 
                pass
        return data_dict

    def debug_days(data_dict, set_index = "timestamp"): 
        for i in data_dict.keys(): 
            #print(data_dict[i].columns)
            data_dict[i] = data_dict[i].set_index(set_index)
        debug_df = pd.concat([data_dict[i] for i in data_dict.keys()], axis = 1)
        debug_df = debug_df[debug_df.isnull().any(axis = 1)]
        debug_days = debug_df.reset_index()
        debug_days = debug_days["timestamp"].tolist()
        return debug_days

    def filter_by_feature(data, threshold = 0.5): 
        #clean out features
        feature_dict = {}
        for i in range(len(data[list(data.keys())[0]])):
            feature_dict[i] = [float(data[j][i]) for j in data.keys()]
        print(feature_dict)
        #for i in len(data[list(data.keys())[0]]):
        #    print(i)
        #size = len(data)
        #return sorted(data)[int(math.ceil((size * perc) / 100)) - 1]

class make_dfs(): 

    def make_pca_df(data_dict, feature_dict): 
        pca_df = pd.DataFrame()
        return pca_df
