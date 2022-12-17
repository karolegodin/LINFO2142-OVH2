import yaml # For yaml interpretation
import math #
import glob # Used to reach multiple files in a folder

# Graph libraries
import numpy as np
import matplotlib.pyplot as plt

# This array is usde for displaying hours instead of the file number.
# Cannot be used everytime as this is quickly unreadable
time = ["8.00", "8.05", "8.10", "8.15", "8.20", "8.25", "8.30", "8.35", "8.40", "8.45", "8.50", "8.55", "9.00", "9.05", "9.10", "9.15", "9.20", "9.25", "9.30", "9.35", "9.40", "9.45", "9.50", "9.55", "10.00", "10.05", "10.10", "10.15", "10.20", "10.25", "10.30", "10.35", "10.40", "10.45", "10.50", "10.55", "11.00", "11.05", "11.10", "11.15", "11.20", "11.25", "11.30", "11.35", "11.40", "11.45", "11.50", "11.55", "12.00"]


# Used to cut digits
def truncate(number, digits):
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1])
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

# Displays the array-data gathered for a single file
def print_operator_array(op_tab):
    for op in range(len(op_tab)):
        # Print operator name
        print("\n["+op_tab[op][0]+"]")
        for i in op_tab[op][1]:
            print("  - "+i, " : ", op_tab[op][1][i])

    # Statistics
    print("\nStatistics")
    #Average load for operators
    avg_load = 0
    avg_links = 0
    for op in range(len(op_tab)):
        avg_load += op_tab[op][1]["total_load"]
        avg_links += op_tab[op][1]["nb_of_links"]
    avg_load =  truncate(avg_load/len(op_tab), 2)
    avg_links = truncate(avg_links/len(op_tab), 2)
    print("Average load for an operator : ", avg_load)
    print("Average peers for an operator : ", avg_links)



# IN : array from extract_data of a moment
def barchart_drawer(in_data):
    # Colors
    color_array=["mediumblue","mediumorchid","violet","crimson","lightpink","royalblue","lightsteelblue","limegreen","cadetblue","yellow"]
    # set width of bar
    barWidth = 0.15
    fig = plt.subplots(figsize =(10, 6))

    position_array= []
    data_array=[]
    set_name=[]
    operator_name_set=[]

    # Set names
    for set in in_data[0][1]:
        set_name.append( str(set) )
    print("Set names : ", set_name,"\n")
    print("Init data_array : ", data_array,"\n")


    # Fill data array
    for set in in_data[0][1]:
        tmp_subdata =[]
        for op in range( len(in_data) ):
            tmp_subdata.append(in_data[op][1][set])
        print(set, " : ", tmp_subdata)
        data_array.append(tmp_subdata)
    print("Data array : ", data_array,"\n")

    # Operator name
    for op in range( len(in_data) ):
        op_name= in_data[op][0]
        operator_name_set.append(op_name)
    print("Operator names : ",operator_name_set,"\n")


    # Set position of bar on X axis
    br_tmp = np.arange( len(data_array[0]) )
    position_array.append(br_tmp)
    print("br_tmp init : ",br_tmp)

    for dataSet in range( len(data_array)-1 ):
        br_tmp = [x + barWidth for x in position_array[dataSet]]
        position_array.append(br_tmp)
        print("br_tmp : ",br_tmp)
    print("Position array : ",position_array,"\n")

    # Make the plot
    for i in range( len(data_array) ):
        plt.bar(position_array[i],
                data_array[i],
                color=color_array[i%10],
                width=barWidth,
                edgecolor='grey',
                label=set_name[i])


    # X/Y names
    plt.xlabel('Operator', fontweight ='bold', fontsize = 10)
    plt.ylabel('UA', fontweight ='bold', fontsize = 10)
    plt.xticks([r + barWidth for r in range(len(data_array[0]))],
            operator_name_set)

    plt.legend()
    plt.show()


#IN : all the data of a set of moments, string of category to analyse
# Draws the chart of the evolution of all operators regarding a specific category, on different times
def linechart_drawer(in_moments_data, category, legend):
    print("Rendering graph...")
    graphCount = 1
    for op in range( len(in_moments_data[0]) ):
        tmp_op_time_evolution=[]
        for moment in range( len(in_moments_data) ):
            tmp_op_time_evolution.append(in_moments_data[moment][op][1][category])
        #print(moment, " : ", op, " : ", tmp_op_time_evolution)
        plt.plot(tmp_op_time_evolution, label=in_moments_data[moment][op][0])

    plt.xlabel('Time (1 UA = 5 minutes)', fontweight ='bold', fontsize = 10)
    plt.ylabel(category, fontweight ='bold', fontsize = 10)
    if legend:
        plt.legend()
    plt.show()

#  For all operators from a single file we get [name, data table]
def extract_data(file_path):
    # Open file
    with open(file_path,'r') as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)

    # Variables
    operator_Array = [] #
    operator_dict = {}
    index = 0

    for operator in data:
        operator_dict[operator]=index
        index+=1

        op_load = 0
        link_count=0

        for label in data[operator]["links"]:
            op_load += label["load"]
            link_count += 1

        #print("Total load for ", operator," : ", op_load)
        #print("-------------------------")
        avg_load = truncate( (op_load/link_count) ,2)
        tmp_dict={"total_load": op_load, "nb_of_links": link_count, "avg_load_per_link": avg_load}
        operator_Array.append([operator,tmp_dict])

    #print("AMAZON : ", operator_dict["AMAZON"])
    #print( operator_Array[ operator_dict["AMAZON"] ][1]["total_load"])
    #print("\n| DATA FOR :", file_path ," ------\n")
    #print_operator_array(operator_Array)
    return operator_Array

# For one operator we get [name, data table]from a single file
def extract_data_1_OP(file_path, op):
    # Open file
    with open(file_path,'r') as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)

    # Variables
    operator_Array = [] #
    operator_dict = {}
    index = 0

    operator = op
    operator_dict[operator]=index
    index+=1

    op_load = 0
    link_count=0

    for label in data[operator]["links"]:
        op_load += label["load"]
        link_count += 1

    #print("Total load for ", operator," : ", op_load)
    #print("-------------------------")
    avg_load = truncate( (op_load/link_count) ,2)
    tmp_dict={"total_load": op_load, "nb_of_links": link_count, "avg_load_per_link": avg_load}
    operator_Array.append([operator,tmp_dict])

    #print("AMAZON : ", operator_dict["AMAZON"])
    #print( operator_Array[ operator_dict["AMAZON"] ][1]["total_load"])
    #print("\n| DATA FOR :", file_path ," ------\n")
    #print_operator_array(operator_Array)
    return operator_Array


# IN : path of folder containing yaml files to parse
# OUT : a list of "data arrays"
#
def extract_several(folder_path, decalage, step):
    #fin=decalage+50
    print("Extracting data...")
    fileCounter = 1
    fin = decalage+step
    files_data_array=[]
    # Find all folder paths and put them in an array
    files_array = glob.glob(folder_path + "\\*.yaml")
    for i in range( len(files_array[decalage:fin]) ):
        #for i in range( len(files_array[decalage:]) ):
        moment_data = extract_data( files_array[i+decalage])
        files_data_array.append( moment_data )
        #barchart_drawer(moment_data)
        #print(i, " : ", moment_data, "\n\n")
        print(fileCounter)
        fileCounter+=1
    #print(files_data_array)
    return files_data_array

# Plots the total of available links in a network of a set of moments
def chart_total_link_on_network(in_moments_array):
    res = []
    for moment in range(len(in_moments_array)):
        subres = 0
        for op in range( len(in_moments_array[moment]) ):
            subres+=in_moments_array[moment][op][1]["nb_of_links"]
        print("Subres : ", subres)
        res.append(subres)
        print("Sommes des liens",res)

    plt.plot(res, label="Total number of links in network")
    plt.xlabel('Time (1 UA = 5 minutes)', fontweight ='bold', fontsize = 10)
    plt.ylabel("Number of available links in Europe", fontweight ='bold', fontsize = 10)
    plt.legend()
    plt.show()
    return res

# Extracts data only for 1 operator, so that it is possible to draw a single line in the plotting.
def extract_several_single_op(folder_path, decalage, step, op):
    #fin=decalage+50
    print("Extracting data...")
    fileCounter = 1
    fin = decalage+step
    files_data_array=[]
    # Find all folder paths and put them in an array
    files_array = glob.glob(folder_path + "\\*.yaml")
    for i in range( len(files_array[decalage:fin]) ):
        #for i in range( len(files_array[decalage:]) ):
        moment_data = extract_data_1_OP( files_array[i+decalage], op)
        files_data_array.append( moment_data )
        #barchart_drawer(moment_data)
        #print(i, " : ", moment_data, "\n\n")
        print(fileCounter)
        fileCounter+=1
    #print(files_data_array)
    return files_data_array

# Compares 2 sets of moments 1 by 1. You need to chose sets so they start at the same time and have the same lengh.
def accident_day_comparison_drawer(in_moments_d1, in_moments_d2):
    print("Rendering graph...")
    time = ["8.35", "8.40", "8.45", "8.50", "8.55", "9.00", "9.05", "9.10", "9.15", "9.20", "9.25", "9.30", "9.35", "9.40", "9.45", "9.50", "9.55", "10.00", "10.05", "10.10", "10.15", "10.20", "10.25", "10.30", "10.35", "10.40", "10.45", "10.50", "10.55", "11.00", "11.05", "11.10", "11.15", "11.20", "11.25", "11.30", "11.35", "11.40", "11.45", "11.50", "11.55", "12.00"]
    day_1=[]
    for mom in range( len(in_moments_d1) ):
        day_1.append( in_moments_d1[mom][0][1]["total_load"] )
    plt.plot(time[0: len(in_moments_d1) ], day_1, label="fra-fr5-sbb2-nc5, 12 Oct.")

    day_2=[]
    for mom in range( len(in_moments_d2) ):
        day_2.append( in_moments_d2[mom][0][1]["total_load"] )
    plt.plot(time[0: len(in_moments_d2) ], day_2, label="fra-fr5-sbb2-nc5, 13 Oct.")

    plt.xlabel('Time (am)', fontweight ='bold', fontsize = 10)
    plt.ylabel("Total load (UA)", fontweight ='bold', fontsize = 10)
    plt.legend()
    plt.show()

# Draws the difference (as a rate) between two sets of data
def difference_drawer(category):
    array_d1 = extract_several("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\europe_problemes_3j", 288+80, 50)
    array_d2 = extract_several("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\europe_problemes_3j", 284+80+288, 50)

    diff = []

    for moment in range( len(array_d1) ):
        tmp_load_d1=0
        tmp_load_d2=0
        for op in range ( len(array_d1[moment]) ):
            tmp_load_d1 += array_d1[moment][op][1][category]
            tmp_load_d2 += array_d2[moment][op][1][category]
        print(category, " day 1 : ", tmp_load_d1)
        print(category, " day 2 : ", tmp_load_d2)
        diff.append( truncate( tmp_load_d2/tmp_load_d1,3) )
    print("Differences : ", diff)
    return diff

"""
Result :
[0.984, 0.987, 0.986, 0.983, 0.993, 0.997, 0.985, 0.985, 0.987, 0.984, 1.001, 1.003, 0.436, 0.021, 0.404, 0.665, 0.762, 0.81, 0.826, 0.84, 0.854, 0.873, 0.889, 0.9, 0.905, 0.914, 0.919, 0.922, 0.931, 0.943, 0.935, 0.945, 0.949, 0.949, 0.97, 0.976, 0.966, 0.967, 0.967, 0.975, 0.98, 0.977, 0.97, 0.967, 0.971, 0.967, 0.978, 0.99, 0.977, 0.975]
"""


### Scripts examples

# Parse 1 YAML file
"""
array = glob.glob("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\data_sample\\*.yaml")
"""

# Extract data from several files in the same folder
"""
file_path = "C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\weathermap_courte.yaml"
tab = extract_several("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\data_sample")
"""

# Extract data from multiple files and graph them
"""
tab = extract_several("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\apac", 288, 144)
linechart_drawer(tab, "total_load", False)
"""

# Draw difference between 2 sets of files (change parameters inside the function)
"""
difference_drawer("total_load")
"""

#
"""
tab = extract_several_single_op("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\world", 288, 144, "fra-fr5-sbb2-nc5")
linechart_drawer(tab, "total_load", True)
"""

# Compare max load's operator on accident day and the day before
"""
tab13 = extract_several_single_op("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\europe_problemes_3j", 288+288+80, 25, "fra-fr5-sbb2-nc5")
tab12 = extract_several_single_op("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\europe_problemes_3j", 288+80, 25, "fra-fr5-sbb2-nc5")
accident_day_comparison_drawer(tab12, tab13)
#linechart_drawer(tab12, "total_load", True)
"""

# Plots the graph of total available links in the network
"""
tab = extract_several("C:\\Users\\Utilisateur\\Desktop\\Cours Belgique\\Network\\Projet 2\\europe_problemes_3j", 288, 288+144)
chart_total_link_on_network(tab)
"""