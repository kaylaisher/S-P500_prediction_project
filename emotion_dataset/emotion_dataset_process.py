'''
這邊我要處理只剩下word、positive、negative的Loughran-McDonald Dictionary

下面的程式碼需要讀取整個csv(row by row)並且顯示目前的讀取進度(讀到哪個字了、他有情緒嗎)

如果讀到的自的positive column有年份，就把它放到emotion.json的positive類型裡面

如果讀到的自的negative column有年份，就把它放到emotion.json的negative類型裡面
'''

import pandas as pd
import json

#open emotion.json file and ready to write emotion categories into it
with open("emotion.json", "r", encoding="utf-8") as f:
  data = json.load(f)

#open the dictionary and ready to read the content, check if iteration find and word belongs to negative or positive categories
df = pd.read_csv('clean_Loughran-McDonald_MasterDictionary.csv')
time = 0
for index, row in df.iterrows():
  if (row.Negative > 0):
    print("word: ", row.Word)
    print("negative: ", row.Negative)
    print("positive: ", row.Positive)
    data["negative"].append(row.Word)
  elif (row.Positive > 0):
    print("word: ", row.Word)
    print("negative: ", row.Negative)
    print("positive: ", row.Positive)
    data["positive"].append(row.Word)

#open emotion.json again and write data back
with open("emotion.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
