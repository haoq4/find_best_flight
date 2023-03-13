import json
import pandas as pd
import os


def json_outs(file_path):
    """
    将json格式转换为xlsx格式
    :param path:
    :return:
    """
    path_lists = file_path
    list_data = []
    for path in path_lists:
        try:
            with open(path, "r", encoding='utf-8') as f:
                data = json.load(f)
                print(data)
                data = pd.DataFrame(data)
                list_data.append(data)
        except Exception as e:
            print("读取错误:",e)
    total_data = pd.concat(list_data)
    total_data.to_excel('flights.csv', index=None)

if __name__ == '__main__':
    file_path = 'best_flights.json'
    json_outs(file_path)