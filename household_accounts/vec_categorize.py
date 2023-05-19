import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
class Net(nn.Module):

    def __init__(self):
        super().__init__()
        
        self.bn = nn.BatchNorm1d(768)
        self.fc1 = nn.Linear(768, 100)
        self.fc2 = nn.Linear(100, 6)


    def forward(self, x):
        h = x.unsqueeze(0) # 1次元 -> 2次元
        h = self.bn(h)
        h = self.fc1(h)
        h = F.relu(h)
        h = self.fc2(h)
        return h
    
# インスタンス化
net = Net().cpu().eval()
net.load_state_dict(torch.load('src/household_accounts/word_categorize.pt', map_location=torch.device('cpu')))
categories = ['食料', '衣服', '趣味', '日用品', '家電', '家具']
def vec_categorize(vector):
    # 予測値の算出
    with torch.no_grad():
        y = net(vector)
    # 確率値に変換
    y = F.softmax(y, dim=1)
    # 予測ラベル
    y = torch.argmax(y)
    category_number = y.to('cpu').detach().numpy().copy()
    category = categories[category_number]
    return category