import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sn
import numpy as np

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




    
def string_2_date(string_date):

    ''' Convert the date as string into a datetime object
    Date format are always tricky : might raise error'''

    date = datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S%z')
    
    return(date)
    



def template():

    ''' Go through csv file loaded as dataframe global variable
        Display ...'''

    start_time = time.time()

    print('template. Execution time :',time.time()-start_time, 's.')


def check_near_contiguity():

    ''' Go through csv file loaded as dataframe global variable
        Display time coherent contiguity between to check if "event" means departure/arrival time'''

    start_time = time.time()

    # get all distinct shipment
    distinct_id_shipment = df.shipment_id.unique()

    list_average = []
    list_shipment_id = []
    for shipment_id in distinct_id_shipment:
        df_grpdby = df[df['shipment_id'] == shipment_id]

        list_time_dep = df_grpdby['timestamp_start.x'].to_list()
        list_time_end = df_grpdby['timestamp_end.x'].to_list()

        list_combination_startend = list(zip(list_time_dep,list_time_end))

        # create datetime objects
        list_combination_startend = [[string_2_date(date_str[0]), string_2_date(date_str[1])] for date_str in list_combination_startend]
##        print(shipment_id)
        
        # sort chronologically
        list_combination_startend.sort()
    

        # time difference between next section supposed departure time and section arrival time
        list_delta_date_across = [list_combination_startend[a+1][0]-list_combination_startend[a][1] for a in range(len(list_combination_startend)-1)]

        # convert in second (float)
        list_secdelta_date_across = [list_delta_date_across[a].total_seconds() / (3600 * 24) for a in range(len(list_delta_date_across))]

        # average delta
        try:
            list_average.append(sum(list_secdelta_date_across) / len(list_secdelta_date_across))
        except:
            list_average.append(0) # sometimes, there is no delta
            pass
            
        list_shipment_id.append(shipment_id)

        
    print('check_near_contiguity. Execution time :',time.time()-start_time, 's.')


    fig,ax = plt.subplots(1)
    
    ax.plot(list_shipment_id, list_average,'k+')
    ax.set_ylabel('supposed section departure/arrival delta (days)')
    ax.set_xlabel('id')

    # Turn off x tick labels
    ax.set_xticklabels([])
    

    plt.show()
    plt.close()


    

def time_boxplot_section():
    
    ''' Go through csv file loaded as dataframe global variable
        Display box plot to give a sense of time distribution for each section'''

    start_time = time.time()

    # get all distinct combination section departure/arrival name
    unique_combination_dep_end_sect = df.groupby(['departure_name','arrival_name']).size().reset_index().rename(columns={0:'count'})
    
    list_ucomb_dep = unique_combination_dep_end_sect['departure_name'].to_list()
    list_ucomb_end = unique_combination_dep_end_sect['arrival_name'].to_list()

    list_list_time_sect = []
    list_time_distin_sect = []
    names_sect = []

    
    # for each distinct combination. get all time recorded 
    for site in zip(list_ucomb_dep, list_ucomb_end):

        list_time_distin_sect = []
        
        filterdf_inte = df[(df['departure_name'] == site[0]) & (df['arrival_name'] == site[1])]
        
        list_inte_st = filterdf_inte['timestamp_start.x'].to_list()
        list_inte_en = filterdf_inte['timestamp_end.x'].to_list()

        #for each occurence get time difference end/start
        for occurence_ind in range(len(list_inte_st)):
            
            time_dif = string_2_date(list_inte_en[occurence_ind]) - string_2_date(list_inte_st[occurence_ind])
            
            time_dif_days = time_dif.total_seconds() / (60*60*24) # convert in days. built in function truncate
            
            list_time_distin_sect.append(time_dif_days)


        list_list_time_sect.append(list_time_distin_sect)
        
        #labels
        names_sect.append(site[0]+ "/" + site[1])      

        

    print('time_distribution_section. Execution time :',time.time()-start_time, 's.')


    uncol = unique_combination_dep_end_sect['count'].to_list()
    fig1 = plt.figure('1')
    plt.hist(uncol, bins=20)
    plt.gca().set(title='Frequency Histogram', xlabel= 'number of occurence' , ylabel='Frequency')
    
    
##
    fig2 = plt.figure('2')
    ax = fig2.add_subplot(111)
    bp = ax.boxplot(list_list_time_sect[14:25])
    ax.set_xticklabels(names_sect, rotation=70)
    plt.title('Boxplot time comparison')
    plt.ylabel('time taken (days)')
    plt.show()
    plt.close()



def check_time_lost():

    ''' Go through csv file loaded as dataframe global variable
        Display time "lost" in the same place compared to global time for each route'''

    start_time = time.time()

    # get all distinct shipment
    distinct_id_shipment = df.shipment_id.unique()

    list_sum_delta = []
    list_global_time = []
    list_shipment_id = []
    list_global_time_lost = []
    for shipment_id in distinct_id_shipment:
        df_grpdby = df[df['shipment_id'] == shipment_id]

        list_time_dep = df_grpdby['timestamp_start.x'].to_list()
        list_time_end = df_grpdby['timestamp_end.x'].to_list()

        list_combination_startend = list(zip(list_time_dep,list_time_end))

        # create datetime objects
        list_combination_startend = [[string_2_date(date_str[0]), string_2_date(date_str[1])] for date_str in list_combination_startend]
##        print(shipment_id)
        
        # sort chronologically
        list_combination_startend.sort()
        
        # global time
        global_time = list_combination_startend[-1][1] - list_combination_startend[0][0]
        global_time = global_time.total_seconds() / (3600 * 24) # conversion in days
        list_global_time.append(global_time)      
            
        list_shipment_id.append(shipment_id)

        # get distinct departure site for this route
        distinct_sectionfor_route = df_grpdby.departure_name.unique()

        # Python is really beautiful for allowing this
        list_filterdfgroupby_same = [df_grpdby[(df_grpdby['departure_name'] == site) & (df_grpdby['arrival_name'] == site)] for site in list(distinct_sectionfor_route)]

        global_time_lost = 0
        
        for same_deparr_section in list_filterdfgroupby_same:
            # list times of all which start at k and finish at k
            same_deparr_section_dept = list(same_deparr_section['timestamp_start.x'])
            same_deparr_section_endt = list(same_deparr_section['timestamp_end.x'])

            
            same_deparr_section_couplt =list(zip(same_deparr_section_dept, same_deparr_section_endt))
            
            # time taken for each section that goes from site to site
            list_time_samesection = [string_2_date(same_section_time[1]) - string_2_date(same_section_time[0]) for same_section_time in same_deparr_section_couplt]
            list_time_samesection = [ delta_times.total_seconds() for delta_times in list_time_samesection]


            global_time_lost += sum(list_time_samesection)

        list_global_time_lost.append(global_time_lost / (3600 * 24))
                       
        
    print('check_time_lost. Execution time :',time.time()-start_time, 's.')


##    fig,ax = plt.subplots(1)
##    
##    ax.plot(list_shipment_id, list_average,'k+')
##    ax.set_ylabel('supposed section departure/arrival delta (days)')
##    ax.set_xlabel('id')

    # Turn off x tick labels
    ax = plt.subplot(111)
    # display just a part for the sake of readability
    b1 = ax.bar(list_shipment_id[-15::], list_global_time[-15::], width=-0.4, color='b', align='edge')
    b2 = ax.bar(list_shipment_id[-15::], list_global_time_lost[-15::], width=0.4, color='r', align='edge')
    plt.ylabel('time (days)')
    plt.xlabel('route')
    plt.legend((b1[0], b2[0]), ('global time', 'time"lost"'))
    ax.set_xticklabels([])
    plt.show()
    plt.close()


def obligarory_passage():

    ''' Go through csv file loaded as dataframe global variable
        Display confusion matrix between mean departure / destination
        Display number of route per owner
        could have other version ; could do it for each section'''

    start_time = time.time()
    # get distinct id
    distinct_id_shipment = df.shipment_id.unique()
    list_departure = []
    list_destination = []

    # get each different route
    for shipment_id in distinct_id_shipment:
        df_grpdby_id = df[df['shipment_id'] == shipment_id]
        df_grpdby_id_hd = df_grpdby_id.head(1)
        list_departure += list(df_grpdby_id_hd['main_departure_name'])
        list_destination += list(df_grpdby_id_hd['destination_name'])

##    print(len(list_departure))
##    print(len(list_destination))
    confu_matrix = confusion_matrix(list_departure, list_destination)
##    print(confu_matrix)

    df_cm = pd.DataFrame(confu_matrix)

    # get number of route for the owner
    distinct_owner = df.owner.unique()
    list_number_router_owner = []
    for owner in distinct_owner:
        df_grpdby = df[df['owner'] == owner]
        list_number_router_owner.append(len(df_grpdby.shipment_id.unique()))

    print('template. Execution time :',time.time()-start_time, 's.')


    # Cannot understand why it does not display properly for now. with clean label and alignment
    sn.set(font_scale = 1.4)
    ax = sn.heatmap(df_cm, fmt = "g", cmap = "bone_r")
    plt.show()
    plt.close()

    ax = plt.subplot(111)
    b2 = ax.bar(distinct_owner, list_number_router_owner, width=0.4, color='r', align='center')
    ax.set_xticklabels(distinct_owner, rotation=90)
    plt.ylabel("number of route")
    plt.show()
    plt.close()
    







################# Useless / not finished ############


def make_categorical():

    ''' Go through csv file loaded as dataframe global variable
        Consider some variables as categories. Yet to check but could save execution time. Avoid string comparison (= operator)
        not really finished. Maybe there is a more beautiful way to do it'''

    # careful different columns can belong to same category
    start_time = time.time()
    
    categor_dict = dict()
    col_category= ['main_departure_name','destination_name', 'shipment_id',
       'departure_name', 'arrival_name', 'departure_poi_type', 'arrival_poi_type', 'owner']

    for col_cat in col_category:
            categor_dict[col_cat] = set(df[col_cat].unique())
            df[col_cat] = pd.Categorical(df[col_cat], categories = np.array(list(categor_dict[col_cat])))

##        categor_dict[col_cat] = set(df[col_cat].unique())
        
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    print('make_categorical. Execution time :',time.time()-start_time, 's.')

def check_time_lost_customer():

    ''' Go through csv file loaded as dataframe global variable
        Display time "lost" for client route (several here client with there potential multiple route)
        kind of specialization of check_time_lost
        

        not finished. Only owner chanel instead for now'''

##    distinct_owner = df.owner.unique()
##    for owner in distinct_owner:
##        df_grpdby = df[df['owner'] == owner]
##        print(owner)
##        print(len(df_grpdby.shipment_id.unique()))

    start_time = time.time()

    # get all distinct shipment
    distinct_owner = df.owner.unique()

    list_owner_p_route = []
    list_list_global_time = []
    list_list_global_time_lost = []
    for owner in distinct_owner:
        distinct_id_shipment = df_grpdby_owner.shipment_id.unique()
        list_sum_delta = []
        list_global_time = []
        list_shipment_id = []
        list_global_time_lost = []
        for shipment_id in distinct_id_shipment:
            df_grpdby = df[df['shipment_id'] == shipment_id]

            list_time_dep = df_grpdby['timestamp_start.x'].to_list()
            list_time_end = df_grpdby['timestamp_end.x'].to_list()

            list_combination_startend = list(zip(list_time_dep,list_time_end))

            # create datetime objects
            list_combination_startend = [[string_2_date(date_str[0]), string_2_date(date_str[1])] for date_str in list_combination_startend]
    ##        print(shipment_id)
            
            # sort chronologically
            list_combination_startend.sort()
            
            # global time
            global_time = list_combination_startend[-1][1] - list_combination_startend[0][0]
            global_time = global_time.total_seconds() / (3600 * 24) # conversion in days
            list_global_time.append(global_time)      
                
            list_shipment_id.append(shipment_id)

            # get distinct departure site for this route
            distinct_sectionfor_route = df_grpdby.departure_name.unique()

            # Python is really beautiful for allowing this
            list_filterdfgroupby_same = [df_grpdby[(df_grpdby['departure_name'] == site) & (df_grpdby['arrival_name'] == site)] for site in list(distinct_sectionfor_route)]

            global_time_lost = 0
            
            for same_deparr_section in list_filterdfgroupby_same:
                # list times of all which start at k and finish at k
                same_deparr_section_dept = list(same_deparr_section['timestamp_start.x'])
                same_deparr_section_endt = list(same_deparr_section['timestamp_end.x'])

                
                same_deparr_section_couplt =list(zip(same_deparr_section_dept, same_deparr_section_endt))
                
                # time taken for each section that goes from site to site
                list_time_samesection = [string_2_date(same_section_time[1]) - string_2_date(same_section_time[0]) for same_section_time in same_deparr_section_couplt]
                list_time_samesection = [ delta_times.total_seconds() for delta_times in list_time_samesection]


                global_time_lost += sum(list_time_samesection)

            list_global_time_lost.append(global_time_lost / (3600 * 24))
                       
        list_list_global_time_lost.append(list_global_time_lost)
##        list_owner_p_route.append(owner+df[]


        
    print('check_time_lost. Execution time :',time.time()-start_time, 's.')


##    fig,ax = plt.subplots(1)
##    
##    ax.plot(list_shipment_id, list_average,'k+')
##    ax.set_ylabel('supposed section departure/arrival delta (days)')
##    ax.set_xlabel('id')

    # Turn off x tick labels
    ax = plt.subplot(111)
    # display just a part for the sake of readability
    b1 = ax.bar(list_shipment_id[-15::], list_global_time[-15::], width=-0.4, color='b', align='edge')
    b2 = ax.bar(list_shipment_id[-15::], list_global_time_lost[-15::], width=0.4, color='r', align='edge')
    plt.ylabel('time (days)')
    plt.xlabel('route')
    plt.legend((b1[0], b2[0]), ('global time', 'time"lost"'))
    ax.set_xticklabels([])
    plt.show()
    plt.close()




# Powered by RqD
