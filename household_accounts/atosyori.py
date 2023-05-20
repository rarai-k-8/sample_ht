import re
import pandas as pd
import torch
from word2vec import word2vec_BERT
from vec_categorize import vec_categorize
class Atosyori:
    def __init__(self, txt):
        # 行を分割してリストにする
        self.lines = txt.split('\n')

    # 日付と時刻を取得
    def date(self):
        #購入した日付
        dates = []
        times = []
        for line in self.lines:
            date = re.match(r'(\d+)年\s*(\d+)月\s*(\d+)日\s*\((.)\)\s*(\d+):(\d+)', line)
            if date:
                dates.append([date.group(1), date.group(2), date.group(3), date.group(4)])
                times.append([date.group(5), date.group(6)])
        return dates, times
    def store(self):
        store = self.lines[0]
        return store
    def nen_gatu_hi(self):
        date = []
        for line in self.lines:
            if '年' and '月' and '日' in line:
                date.append(line)
            elif re.search(r"\d+/\d+", line):
                date.append(line)
            elif re.search(r"\d+:\d+", line):
                date.append(line)
        if date == []:
            date.append('unknown')
        return date[0]
    
    def item_cost(self):
        item_cost_list = []
        ryosyusyo = 5
        stop = -5
        for i, line in enumerate(self.lines):
            if  ('収' in line) or ('証' in line):
                ryosyusyo = i
                break
        for i, line in enumerate(self.lines):
            if ('小' in line) or ('合' in line) or ('計' in line) or ('対象' in line):
                stop = i
                break
        for j, line in enumerate(self.lines[ryosyusyo:stop]):
            if ('¥' in line) or ("\\" in line) or ('y' in line) or ('※' in line):
                item_cost_list.append(line)
        return item_cost_list
    
    def item_cost_split(self, item_cost_list):
        item_list = []
        cost_list = []
        for item_cost in item_cost_list:
            if ('.' in item_cost) or (',' in item_cost):
                item_cost = item_cost.replace('.', '')
                item_cost = item_cost.replace(',', '')
            if "\\" in item_cost:
                item_cost_splited = item_cost.split("\\")
            if 'y' in item_cost:
                item_cost_splited = item_cost.split('y')
            if '¥' in item_cost:
                item_cost_splited = item_cost.split('¥')
            if '※' in item_cost:
                item_cost = item_cost.replace('※', '')
                item_cost_splited = item_cost.split()
            item_list.append(item_cost_splited[0])
            cost_list.append(item_cost_splited[-1])
        return item_list, cost_list

    def total_cost(self):
        total_cost = []
        for line in self.lines:
            if ('.' in line) or (',' in line):
                line = line.replace('.', '')
                line = line.replace(',', '')
            if ('合' in line) or ('計' in line) or ('台' in line):
                if "\\" in line:
                    total_cost.append(line.split("\\")[-1])
                else:
                    total_cost.append(line.split()[-1])
        if total_cost == []:
            total_cost.append('unknown') 
        return total_cost[-1]
    
    def word_categorize(self, item_list):
        #単語分類
        categorize_list = []
        for item in item_list:
            vector = word2vec_BERT(item) # word2vec.pyのword2vec関数を呼び出す
            vector = torch.tensor(vector, dtype=torch.float32)
            result = vec_categorize(vector)
            categorize_list.append(result)
        return categorize_list
    
    def item_categorize_cost(self, item_list, categorize_list, cost_list):
        item_categorize_cost_list = []
        for item, categorize, cost in zip(item_list, categorize_list, cost_list):
            item_categorize_cost_list.append([item, categorize, cost])
        return item_categorize_cost_list