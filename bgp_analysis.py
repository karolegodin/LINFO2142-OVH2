import glob # Used to reach multiple files in a folder
import matplotlib.pyplot as plt


collectors=["rrc00","rrc01","rrc02","rrc03","rrc04","rrc05","rrc06","rrc07","rrc08","rrc09","rrc10","rrc11","rrc12","rrc13","rrc14","rrc15","rrc16","rrc18","rrc19","rrc20","rrc21","rrc22","rrc23","rrc24","rrc25","rrc26"]


global_router_index = {}
i=0
for router in range( len(collectors) ):
    global_router_index[collectors[router]]=i
    i+=1
print("Global router index : ", global_router_index)

#  Sends a tab containing all the parsed data of a line
def traiter(line):
    subtab = line.split("|")
    # print(subtab, "\n")
    return(subtab)


# Returns an array of arrays. Each sub-array contains the data of a line,
# whole array is a parsed file.
def analyse_1_file_simple(file_path):
    one_router_arr=[]
    for i in range(len(collectors)):
        one_router_arr.append(0)

    data_array=[]
    f = open(file_path, "r")
    for line in f.readlines():
        data_array.append( traiter(line) )
    print(data_array)
    return data_array

def get_collectors_names(file_path):
    one_router_arr=[]
    for i in range(len(collectors)):
        one_router_arr.append(0)

    data_array=[]
    f = open(file_path, "r")
    for line in f.readlines():
        data_array.append( traiter(line) )
    print(data_array)
    return data_array

# Looks for the number of times a router appears in a file
def analyse_1_file_routerFrequency(file_path):
    one_router_arr=[]
    for i in range(len(collectors)):
        one_router_arr.append(0)

    data_array=[]
    f = open(file_path, "r")
    for line in f.readlines():
        data_array.append( traiter(line) )
    #print(data_array)

    for elt in range( len(data_array) ):
        index_to_incr = global_router_index[ data_array[elt][4] ]
        one_router_arr[index_to_incr]+=1

    #print("Router array", one_router_arr)
    return one_router_arr


# Parses data for multiple moments (multiple files)
def analyse_multiple_routerFrequency(folder_path):
    files_data=[]
    files_array = glob.glob(folder_path + "\\*.txt")
    for moment in range( len(files_array) ):
        tmp_data_arr=[]
        #print("\nAnalyzing ", files_array[moment])
        #tmp_data_dic = analyse_1_file_routerFrequency( files_array[moment] )
        #print("tmp data : ", tmp_data_dic)
        #files_data.append( tmp_data_dic )
        files_data.append( analyse_1_file_routerFrequency(files_array[moment]) )

    #print("\nData gathered : ")
    #display_data_by_router(files_data)
    return files_data

# Looks for the number of times a router appears in a file
def analyse_1_file_viewFrequency(file_path, view_name):
    counter = 0

    data_array=[]
    f = open(file_path, "r")
    for line in f.readlines():
        data_array.append( traiter(line) )
    #print(data_array)

    for elt in range( len(data_array) ):
        print(data_array[elt][4], " (", elt, "/", len(data_array), ")")
        if(data_array[elt][4]== view_name):
            counter += 1
    print("Total of the file : ", counter)

    return counter

# Parses data for multiple moments (multiple files)
def analyse_multiple_viewFrequency(folder_path, view_name):
    files_data=[]
    files_array = glob.glob(folder_path + "\\*.txt")
    for moment in range( len(files_array) ):
        tmp_data_arr=[]
        files_data.append( analyse_1_file_viewFrequency(files_array[moment], view_name) )

    return files_data

def display_data_by_router(moments_array):
    for router in range( len(collectors) ):
        print("\nRouter : ", collectors[router])
        for moment in range( len(moments_array) ):
            print(moments_array[moment][router])

#IN : all the data of a moment
def linechart_drawer(in_moments_data):
    print("Rendering graph...")
    for router in range( len(collectors) ):
        tmp_data=[]
        for moment in range( len(in_moments_data) ):
            tmp_data.append( in_moments_data[moment][router] )
        #print( tmp_data )
        plt.plot( tmp_data )

    plt.xlabel('Time', fontweight ='bold', fontsize = 10)
    plt.ylabel("Routers", fontweight ='bold', fontsize = 10)
    plt.show()

#IN : all the data of a moment
def single_collector_getter(in_moments_data, cltr_name):
    for router in range( len(collectors) ):
        tmp_data=[]
        for moment in range( len(in_moments_data) ):
            tmp_data.append( in_moments_data[moment][router] )
            print("Data from extraction, at router", router," : ", in_moments_data[moment][router])
        print("MATCH - Router in list : ", router, ", Router expected : ", global_router_index[cltr_name], " (", cltr_name, ")")
        if global_router_index[cltr_name] == router:
            return tmp_data


#IN : all the data of a moment
def extract_single_collector(in_moments_data, cltr_name):
    print("----------------------------------------------\nExtracting data, for ", cltr_name)

    for router in range( len(collectors) ):
        tmp_data=[]
        print("Current router : ", router)
        if global_router_index[cltr_name] == router:
            for moment in range( len(in_moments_data) ):
                #tmp_data.append( in_moments_data[moment][router] )
                print("MATCH - Router : ", router, ", number : ", global_router_index[cltr_name])
            return tmp_data
    return -1


# IN : an array of paths to files to get
def plot_1_collector_different_times(paths_to_folders, collector):
    # Get data for each time
    tab = []
    for path in range( len(paths_to_folders) ):
        tmp = analyse_multiple_routerFrequency( paths_to_folders[path])
        tmp.append(single_collector_getter(tmp, collector))
        print("Values for ", path," : ", tmp)
        tab.append(tmp)

    #Plot
    for moment in range( len(tab) ):
        plt.plot( tab[moment], label=moment )
    plt.legend()
    plt.xlabel('Time of the day', fontweight ='bold', fontsize = 10)
    plt.ylabel("Collector use", fontweight ='bold', fontsize = 10)
    plt.show()

### Script examples
paths=[]
paths.append("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"BGP_specific_collector\\\rrc_data_control_12_10")
paths.append("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"BGP_specific_collector\\rrc_data_control_13_10")
paths.append("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"BGP_specific_collector\\rrc_data_control_14_10")

# Gathers, diplays and graphs from a set of files
"""
tab = analyse_multiple_routerFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"BGP_specific_collector\\rrc_data_control_1310")
print( tab )
linechart_drawer(tab)
"""

# Looks at the data of a single file
"""
analyse_1_file_simple("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\rcc_sample\\650-700.txt")
"""

# Print the graph of all collectors on a day, then get a specific collector
"""
tab = analyse_multiple_routerFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\rrc_data_control_13-10")
linechart_drawer(tab)
print("Values for \'rrc00\' : ", single_collector_getter(tab, "rrc00"))
"""

# We take 3 moments, get the data, from each moment extract what "rrc00" only does, then plot it.
"""
tab = analyse_multiple_routerFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"BGP_specific_collector\\rrc_data_control_12_10")
subtab = single_collector_getter(tab, "rrc00")

tab1 = analyse_multiple_routerFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\rrc_data_control_13_10")
subtab1 = single_collector_getter(tab1, "rrc00")

tab2 = analyse_multiple_routerFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\rrc_data_control_14_10")
subtab2 = single_collector_getter(tab2, "rrc00")

print("Values for \'rrc00\' the 12: ", subtab)
print("Values for \'rrc00\' the 13: ", subtab1)
print("Values for \'rrc00\' the 14: ", subtab2)

tmp = [subtab, subtab1, subtab2]
plt.plot(subtab, label="12/10")
plt.plot(subtab1, label="14/10")
plt.plot(subtab2, label="13/10")
plt.legend()
plt.xlabel('Time of the day', fontweight ='bold', fontsize = 10)
plt.ylabel("Messages sent", fontweight ='bold', fontsize = 10)
plt.show()
"""

# Search for specific views and count them in a folder
"""
tab = analyse_multiple_viewFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"views\\route-views_data_13_10", "route-views.eqix")
print(tab)
"""
"""
tab = analyse_multiple_viewFrequency("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\"+"views\\route-views_data_control_12_10", "route-views.eqix")
print(tab)
"""

subtab = analyse_multiple_viewFrequency("C:\\Users\\Asus\\Documents\\VM docs\\network_project\\route-views_data_control_12_10", "route-views.eqix")
subtab.reverse()
subtab1 = analyse_multiple_viewFrequency("C:\\Users\\Asus\\Documents\\VM docs\\network_project\\route-views_data_13_10", "route-views.eqix")
subtab1.reverse()
subtab2 = analyse_multiple_viewFrequency("C:\\Users\\Asus\\Documents\\VM docs\\network_project\\route-views_data_control_14_10", "route-views.eqix")
subtab2.reverse()

print("Values for \'rrc00\' the 12: ", subtab)
print("Values for \'rrc00\' the 13: ", subtab1)
print("Values for \'rrc00\' the 14: ", subtab2)

tmp = [subtab, subtab1, subtab2]
plt.plot(subtab, label="12/10")
plt.plot(subtab1, label="13/10")
plt.plot(subtab2, label="14/10")
plt.legend()
plt.xlabel('Time (UTC+2)', fontweight ='bold', fontsize = 10)
plt.ylabel("Number of BGP updates sent from OVH AS to route-views.eqix collector (California)", fontweight ='bold', fontsize = 10)
plt.show()