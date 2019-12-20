import pandas as pd
# from mlxtend.frequent_patterns import apriori
# from mlxtend.frequent_patterns import association_rules
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from  plotly.offline import plot
import itertools
df_choose_item = pd.read_csv('clean_data.csv',parse_dates=['Date'])
# with pd.ExcelFile('../dataSet4 (2)-newFromITaaS.xlsx') as reader:
# print(reader.sheet_names)
    # df_two = pd.read_excel(reader, sheet_name=reader.sheet_names[1])

print(df_choose_item)
