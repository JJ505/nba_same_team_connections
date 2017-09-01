import plotly
from plotly.graph_objs import *
from collections import defaultdict
import igraph as ig
import csv
import random

#for making an arbirtrary dictionary which will be a nested dict
player_names = {}
teams = defaultdict(dict)
player_count = 0
with open('nba_season_data.csv') as nba_data:
    csv_reader = csv.reader(nba_data)
    for row in csv_reader:
        #assigns names using the player_id
        player_names[row[31]] = row[2]
        #sort all data by team->year->playerids on that team year
        teams[row[1]].setdefault(row[0],[]).append(row[31])


player_num = {}
for pid, _ in player_names.items():
    player_num[pid]=player_count
    player_count +=1

#set is used to remove duplicates
edges = set()
#for each element in teams, make edge connections between it and the remaining elements
for _, year in teams.items():
    for _, playerIds in year.items():
        #create edges between each player
        for i in range (0, len(playerIds)-1):
            for j in range (i, len(playerIds)):
                edges.add((player_num[playerIds[i]], player_num[playerIds[j]]))

#begin creating graph
print ("Building graph.  This may take awhile...")
G = ig.Graph(list(edges), directed = False)
labels = []
group =[]

for playerId, _ in player_names.items():
    #in the same order i created the player numbers, create the labels
    labels.append(player_names[playerId])
    #todo generate random group numbers
    group.append(random.random())

layt = G.layout('kk', dim=3)

number_of_nodes = len(player_names)

Xn=[layt[k][0] for k in range(number_of_nodes)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(number_of_nodes)]# y-coordinates
Zn=[layt[k][2] for k in range(number_of_nodes)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

trace1=Scatter3d(x=Xe,
                 y=Ye,
                 z=Ze,
                 mode='lines',
                 line=Line(color='rgb(125,125,125)', width=1),
                 hoverinfo='none'
                 )
trace2=Scatter3d(x=Xn,
                 y=Yn,
                 z=Zn,
                 mode='markers',
                 name='actors',
                 marker=Marker(symbol='dot',
                               size=6,
                               color=group,
                               colorscale='Viridis',
                               line=Line(color='rgb(50,50,50)', width=0.5)
                               ),
                text=labels,
                hoverinfo='text'
                )
axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = Layout(
         title="Link network(3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
    margin=Margin(
        t=100
   ),
   hovermode='closest',
        )
data=Data([trace1, trace2])
fig=Figure(data=data, layout=layout)
#return a div of the graph to be shown in browser
plotly.offline.plot(fig, output_type='file')
