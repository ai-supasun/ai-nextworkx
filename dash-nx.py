import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd














df_market_basket = pd.read_csv('masket_basket.csv')
A = list(df_market_basket["LHS"].unique())
B = list(df_market_basket["RHS"].unique())
# print(list(set(A+B)))
node_list = list(set(A+B))
print(node_list)
G = nx.Graph()
for i,j in df_market_basket.iterrows():
    G.add_edges_from([(j["LHS"],j["RHS"])])
pos = nx.spring_layout(G, k=0.5, iterations=50)
for n, p in pos.items():
    G.nodes[n]['pos'] = p
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')
arrow_x0 = []
arrow_x1 = []
arrow_y0 = []
arrow_y1 = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])
    arrow_x0.append(x0)
    arrow_x1.append(x1)
    arrow_y0.append(y0)
    arrow_y1.append(y1)
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = adjacencies[0]
    node_trace['text']+=tuple([node_info])



# clique
df_market_basket['node'] = list(zip(df_market_basket['LHS'],  df_market_basket['RHS']))
import itertools
import networkx as nx
G = nx.Graph()
edges_fig_4 = df_market_basket['node'].tolist()
edges_fig_4
G.add_edges_from(edges_fig_4)
cliques = nx.find_cliques(G)
length_node = 2
cliques3 = set(sum([list(itertools.combinations(set(clq), length_node)) for clq in cliques if len(clq)>length_node],[]))
# 
G = nx.Graph()
for i in range(len(list(cliques3))):
    G.add_edges_from([(list(cliques3)[i][0],list(cliques3)[i][1])])
pos = nx.spring_layout(G, k=0.5, iterations=50)
for n, p in pos.items():
    G.nodes[n]['pos'] = p
edge_trace_clique = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')
arrow_x0 = []
arrow_x1 = []
arrow_y0 = []
arrow_y1 = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace_clique['x'] += tuple([x0, x1, None])
    edge_trace_clique['y'] += tuple([y0, y1, None])
    arrow_x0.append(x0)
    arrow_x1.append(x1)
    arrow_y0.append(y0)
    arrow_y1.append(y1)
node_trace_clique = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='Picnic',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace_clique['x'] += tuple([x])
    node_trace_clique['y'] += tuple([y])
for node, adjacencies in enumerate(G.adjacency()):
    node_trace_clique['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = adjacencies[0]
    node_trace_clique['text']+=tuple([node_info])













# app = dash.Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.H1("Network Graph")

    ], style={
        'textAlign': "center",
    }),
    html.Div([
        dcc.Graph(id="my-graph",
                  figure={
                      "data": [edge_trace, node_trace],


                      "layout": go.Layout(
                          title='Network Graph With Dash',
                          titlefont={'size': 16},
                          showlegend=False,
                          hovermode='closest',
                          margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
                          xaxis={'showgrid': False,
                                 'zeroline': False, 'showticklabels': False},
                          yaxis={'showgrid': False,
                                 'zeroline': False, 'showticklabels': False})
                  }),    
        dcc.Graph(id="my-graph-one",
                  figure={
                      "data": [edge_trace_clique, node_trace_clique],


                      "layout": go.Layout(
                          title='test-quice-two',
                          titlefont={'size': 16},
                          showlegend=False,
                          hovermode='closest',
                          margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
                          xaxis={'showgrid': False,
                                 'zeroline': False, 'showticklabels': False},
                          yaxis={'showgrid': False,
                                 'zeroline': False, 'showticklabels': False})
                  }), 
                  ]),

], className="container")

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
