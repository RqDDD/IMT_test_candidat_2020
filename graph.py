import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# obviously not written in python considering performance. may not run on your pc. Lot of dependancies. plateform dependant
from igraph import *



df = pd.read_csv("Dataset Next4 - Feuille 1.csv")
##df.isnull().values.any()


def format_date():

    ''' Go through csv file loaded as dataframe global variable
        Operate a convenient change in date format for the timestamp
        Here the timezone of the stamps are not standard for python datetime library
        '''

    start_time = time.time()

    df['timestamp_start.x'] = df['timestamp_start.x'].apply(lambda x: x + "00")
    df['timestamp_end.x'] = df['timestamp_end.x'].apply(lambda x: x + "00")

    print('format_date. Execution time :',time.time()-start_time, 's.')

format_date()



def simple_graph():

    ''' Go through csv file loaded as dataframe global variable
        Display an oversimplified graph to describe departure / destination network and higlight communities
        we could do that for sections too'''

    start_time = time.time()
    # get distinct id
    distinct_id_shipment = df.shipment_id.unique()
    list_departure = []
    list_destination = []

    # get each different route (same id, depends what we mean by route)
    for shipment_id in distinct_id_shipment:
        df_grpdby_id = df[df['shipment_id'] == shipment_id]
        df_grpdby_id_hd = df_grpdby_id.head(1)
        list_departure += list(df_grpdby_id_hd['main_departure_name'])
        list_destination += list(df_grpdby_id_hd['destination_name'])

    # for gephi
    df_bis = pd.DataFrame(list(zip(list_departure, list_destination)))
    df_bis.to_csv("gephi_test.csv", sep = ",")
    
    lbs= list(set(list_departure+list_destination))
    print(lbs)
    confu_matrix = confusion_matrix(list_departure, list_destination, labels=lbs)
    print(confu_matrix)
    graph_depdest = Graph.Adjacency(confu_matrix.tolist(),mode=ADJ_UNDIRECTED)
    # associate summit with name
    graph_depdest.vs["name"] = lbs
    graph_depdest.vs['label'] = [name[0:3] for name in lbs] # make it shorter for readability

    print('simple_graph. Execution time :',time.time()-start_time, 's.')
    
    # plotting
    community_dete_graph = graph_depdest.community_edge_betweenness(directed=False)
    plot(community_dete_graph)
##    community_dete_graph.show()
    plot(graph_depdest,vertex_label_size=15,vertex_size=35,vertex_color='#06b823')
##    plot_graph.show()
    
##    df_cm = pd.DataFrame(confu_matrix)
##    print(df_cm)


    
