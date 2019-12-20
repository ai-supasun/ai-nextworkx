import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# import pandas as pd


# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
# # import plotly.graph_objects as go
# from  plotly.offline import plot
# import itertools

df_sum_item = pd.read_csv('clean_datav2.csv')

df_choose_item = df_sum_item
# print('--------------------------------------------------------------------------------------------------------------------')
def choose_income_quality(choose_income_quality):
  # print(choose)
  df_choose_item = df_sum_item.sort_values(f"{choose_income_quality}",ascending=False)
  df_choose_item[f'total_{choose_income_quality}'] = df_choose_item[f'{choose_income_quality}'].sum()
  df_choose_item[f'percent_{choose_income_quality}'] = df_choose_item[f'{choose_income_quality}']/df_choose_item[f'total_{choose_income_quality}'] * 100
  df_choose_item[f'cumulative_{choose_income_quality}'] = df_choose_item[f'percent_{choose_income_quality}'].cumsum()
  return df_choose_item
df_choose_item = choose_income_quality('sum_price')
# df_choose_item = choose_income_quality('Quantity')

# print('--------------------------------------------------------------------------------------------------------------------')
def split_cumulative(percent):
  return df_choose_item[-int(len(df_choose_item) / 100 * percent):]
df_choose_item = split_cumulative(10)
# df_choose_item = split_cumulative(80)

# print('--------------------------------------------------------------------------------------------------------------------')
# เลือกวันที่
def between_date(start_date, end_date):
  return df_choose_item.loc[(df_choose_item['Date'] > start_date) & (df_choose_item['Date'] <= end_date)]
df_choose_item = between_date('2018-01-01','2018-12-12')
# print('--------------------------------------------------------------------------------------------------------------------')
# เลือกรายได้หรือปริมาณเเละเลือกจำนวนtopที่จะออกมา
def top_item(total_list,choose_income_quality):
    list_top = df_choose_item.groupby('Item No').sum().reset_index().sort_values(f'{choose_income_quality}',ascending=False)['Item No'].tolist()[:10]
    if total_list == 5:
      df_list_item = df_choose_item[(df_choose_item['Item No'] == list_top[0]) | 
                      (df_choose_item['Item No'] == list_top[1]) | 
                      (df_choose_item['Item No'] == list_top[2]) | 
                      (df_choose_item['Item No'] == list_top[3]) | 
                      (df_choose_item['Item No'] == list_top[4])]
    elif total_list == 10:
      df_list_item = df_choose_item[(df_choose_item['Item No'] == list_top[0]) | 
                      (df_choose_item['Item No'] == list_top[1]) | 
                      (df_choose_item['Item No'] == list_top[2]) | 
                      (df_choose_item['Item No'] == list_top[3]) | 
                      (df_choose_item['Item No'] == list_top[4]) | 
                      (df_choose_item['Item No'] == list_top[5]) | 
                      (df_choose_item['Item No'] == list_top[6]) |
                      (df_choose_item['Item No'] == list_top[7]) | 
                      (df_choose_item['Item No'] == list_top[8]) | 
                      (df_choose_item['Item No'] == list_top[9])]
    return df_list_item
# df_choose_item = top_item(10,'sum_price')
# df_choose_item = top_item(5,'Quantity')

# df_basket = (df_choose_item
#           .groupby(['Receipt No', 'Item No'])['Quantity']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('Receipt No'))
# df_basket
df_basket =df_choose_item.pivot_table(values = 'Quantity',index='Receipt No' , columns = 'Item No')
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = df_basket.applymap(encode_units)
frequent_itemsets = apriori(basket_sets, min_support=0.00001, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules['LHS'] = [",".join(tuple(rules['antecedents'][i])) for i in range(len(rules['antecedents']))]
rules['RHS'] = [",".join(tuple(rules['consequents'][i])) for i in range(len(rules['consequents']))]
df_market_basket = rules[['LHS','RHS','antecedent support','consequent support','support','confidence','lift','leverage','conviction']]


      

