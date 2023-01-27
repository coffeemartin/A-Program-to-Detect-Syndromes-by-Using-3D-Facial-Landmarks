# Fanchao Meng - 23370209
# CITS1401 - Project 2

def adultid_checker (filename,adultids):
    """
         A function to check user's adult ID inputs:

         If both adult IDs are invalid. The function will return None,
         and generate a report. Explaining what was the issue with the adult Ids.
       
         The issues can be :
       
          (1): invalid X,Y,Z coordinates, prompt user to check specific adult ID's X,Y,Z Coordinates.
          (2): missing/extra/mis-spelling landmarks. prompt user to check specific adult ID's 15 landmarks.
          (3): Adult ID doesn't exist in the data at all.
        
    """
    corrupted_coordinates_list = corrupt_xyz_coordinates (filename)
    missing_landmark_list = missing_landmark(filename)
    full_adultid_list = find_adult_id_list(filename)
    final_dict = final_clean_dict(filename)
    valid_adultid_list = list(final_dict.keys())
    if adultids[0] not in valid_adultid_list and adultids[1] not in valid_adultid_list:
        for i in adultids:
            print("Report - {}".format(adultids.index(i)+1))
            if i in corrupted_coordinates_list:
                print ("The AdultID: {} has invalid values in the x/y/z column(s).".format(i))
            elif i in missing_landmark_list:
                print ("The AdultID: {} has missing/wrong/extra facial landmarks.".format(i))  
            elif i not in full_adultid_list:
                print ("The AdultID: {} does not exsited in the data, please check your input.".format(i))
        return None
    else:
        return True
        
        



def filereader (filename):
    
    """
        A function to read in the data.
        
        If the file doesn't exist, gracefully terminate and notify user.
        
        If the file exist: 
        (1): check if it is a blank csv
        (2): converts everything to uppercase to be case insensitive
        (3): strips every cell's leading and trailing white spaces if there is any.
        
        function returns a header list, then main data list.
    """
    try:
        with open(filename,"r",encoding='utf-8-sig') as myfile:
            data_list = []
            header_list = []
            header = myfile.readline().rstrip("\n").split(",")
            if len(header) == 0:
                print("There is no data in the file : {}".format(filename))
                return None
            else:
                for x in header:
                    header_list.append(x.upper().strip())
                content = myfile.readlines()
                for line in content:
                    mylist = line.rstrip("\n").upper().split(",")
                    for i in range(len(mylist)):
                        mylist[i] = mylist[i].strip()
                    data_list.append(mylist)
                return(header_list,data_list)
    except FileNotFoundError:
        print("cannot open the file   {0:s}   ,please check your filename or directory".format(filename))
        return None
    
def corrupt_xyz_coordinates (filename):
    """
       A function to check X,Y,Z coordinates depends on header order, and
       return a list of adult_ids when its corresponding X,Y,Z coordinates
       is invalid, either:
       
       1: Empty or multiple white spaces
       2: Not numbers (letters, random characters)
       3: Out of bound [-200,200] range
       
       All the data corresponding these ID numbers will be excluded from any further calculations.   
    """
    
    original_list = filereader (filename)[1]
    my_header = filereader(filename)[0]
    corrupted_coordinates_list = []
    id_index = my_header.index("ADULTID")
    x_index = my_header.index("X")
    y_index = my_header.index("Y")
    z_index = my_header.index("Z")
    for item in original_list:
        for i in [x_index, y_index, z_index]:
            if item[i] == "" :
                if item[id_index] not in corrupted_coordinates_list:
                    corrupted_coordinates_list.append(item[id_index])
            elif item[i].lstrip('-').replace('.','',1).isdigit() == False:
                if item[id_index] not in corrupted_coordinates_list:
                    corrupted_coordinates_list.append(item[id_index])
            elif float(item[i]) > 200 or float(item[i]) < -200:
                if item[id_index] not in corrupted_coordinates_list:
                    corrupted_coordinates_list.append(item[id_index])      
    return corrupted_coordinates_list
        
    

def find_adult_id_list(filename):
    """
       A function to produce an entire adult_id_list from "adultid" column,
       minus all the adult_id which has invalid X,Y,Z coordinates.
    
    """

    mylist = filereader(filename)[1]
    header = filereader(filename)[0]
    id_index = header.index("ADULTID")
    to_be_deleted_id = corrupt_xyz_coordinates (filename)
    final_id_list = []
    for i in mylist:
        if i[id_index] not in final_id_list:
            final_id_list.append(i[id_index])
    for i in to_be_deleted_id:
        final_id_list.remove(i)
        
    return final_id_list



def original_data_dict (filename):
    """
        A function to produce an initial nested dictionary, having adult_id as main keys, then in every
        adult_id dictionary, having all 15 facial landmanks as keys with corresponding x,y,z
        coordinates values
    """
    original_dict = {}
    nested_dict = {}
    header = filereader(filename)[0]
    original_data = filereader(filename)[1]
    adult_id_list = find_adult_id_list(filename)
    id_index = header.index("ADULTID")
    landmark_index = header.index("LANDMARK")
    x_index = header.index("X")
    y_index = header.index("Y")
    z_index = header.index("Z")
    for i in adult_id_list:
        for row in original_data:
            if row[id_index]==i:
                nested_dict[row[landmark_index]] = [float(row[x_index]),float(row[y_index]),float(row[z_index])]
        original_dict[i]=nested_dict
        nested_dict={}
    return original_dict

def missing_landmark(filename):
    """
       A function to check every adult ID, is having 15 valid facial landmarks recorded.
       If there is a landmark entry missing, or a invalid landmark name,
       this function will return a list of these invalid adult_id,
       to be excluded in further calculations.
    """
    original = original_data_dict(filename)
    missing_landmark_list = []
    for adultid in original:
        correct_landmark_list = ['EX_L', 'EN_L', 'N', 'EN_R', 'EX_R', 'PRN', 'AL_L', 'AL_R', 'SBAL_L', 'SBAL_R', 'CH_L', 'CH_R', 'SN', 'FT_L', 'FT_R']
        keylist =  original[adultid].keys()           
        a = set(keylist)
        b = set(correct_landmark_list)
        if a != b :
            missing_landmark_list.append(adultid)        
    return(missing_landmark_list)
            
def final_clean_dict(filename):
    """
       A function to produce a final dictionary ready to be used and calculated,
       it will excludes the missing_landmark_list from above function.
    """
    original = original_data_dict (filename)
    to_be_delete = missing_landmark (filename)
    for i in to_be_delete:
        del original[i]
    return original

    
def calculate_facial_distance (filename):
    
    """
       A function to return a new dictionary of facial landmark distances, based on the
       given formular. Have Adult Id as keys, and its value is another nested key, with
       ficial distance abvn as keys.

    """
    my_dict = final_clean_dict (filename)
    facial_distance_dict = {}
    nested_dict = {}
    for i in my_dict:
        nested_dict["FW"]=((my_dict[i]["FT_L"][0]-my_dict[i]["FT_R"][0])**2 + (my_dict[i]["FT_L"][1]-my_dict[i]["FT_R"][1])**2 + (my_dict[i]["FT_L"][2]-my_dict[i]["FT_R"][2])**2)**(1/2)
        nested_dict["OCW"]=((my_dict[i]["EX_L"][0]-my_dict[i]["EX_R"][0])**2 + (my_dict[i]["EX_L"][1]-my_dict[i]["EX_R"][1])**2 + (my_dict[i]["EX_L"][2]-my_dict[i]["EX_R"][2])**2)**(1/2)
        nested_dict["LEFL"]=((my_dict[i]["EX_L"][0]-my_dict[i]["EN_L"][0])**2 + (my_dict[i]["EX_L"][1]-my_dict[i]["EN_L"][1])**2 + (my_dict[i]["EX_L"][2]-my_dict[i]["EN_L"][2])**2)**(1/2)
        nested_dict["REFL"]=((my_dict[i]["EN_R"][0]-my_dict[i]["EX_R"][0])**2 + (my_dict[i]["EN_R"][1]-my_dict[i]["EX_R"][1])**2 + (my_dict[i]["EN_R"][2]-my_dict[i]["EX_R"][2])**2)**(1/2)
        nested_dict["ICW"]=((my_dict[i]["EN_L"][0]-my_dict[i]["EN_R"][0])**2 + (my_dict[i]["EN_L"][1]-my_dict[i]["EN_R"][1])**2 + (my_dict[i]["EN_L"][2]-my_dict[i]["EN_R"][2])**2)**(1/2)
        nested_dict["NW"]=((my_dict[i]["AL_L"][0]-my_dict[i]["AL_R"][0])**2 + (my_dict[i]["AL_L"][1]-my_dict[i]["AL_R"][1])**2 + (my_dict[i]["AL_L"][2]-my_dict[i]["AL_R"][2])**2)**(1/2)
        nested_dict["ABW"]=((my_dict[i]["SBAL_L"][0]-my_dict[i]["SBAL_R"][0])**2 + (my_dict[i]["SBAL_L"][1]-my_dict[i]["SBAL_R"][1])**2 + (my_dict[i]["SBAL_L"][2]-my_dict[i]["SBAL_R"][2])**2)**(1/2)
        nested_dict["MW"]=((my_dict[i]["CH_L"][0]-my_dict[i]["CH_R"][0])**2 + (my_dict[i]["CH_L"][1]-my_dict[i]["CH_R"][1])**2 + (my_dict[i]["CH_L"][2]-my_dict[i]["CH_R"][2])**2)**(1/2)
        nested_dict["NBL"]=((my_dict[i]["N"][0]-my_dict[i]["PRN"][0])**2 + (my_dict[i]["N"][1]-my_dict[i]["PRN"][1])**2 + (my_dict[i]["N"][2]-my_dict[i]["PRN"][2])**2)**(1/2)
        nested_dict["NH"]=((my_dict[i]["N"][0]-my_dict[i]["SN"][0])**2 + (my_dict[i]["N"][1]-my_dict[i]["SN"][1])**2 + (my_dict[i]["N"][2]-my_dict[i]["SN"][2])**2)**(1/2)
        facial_distance_dict[i] = nested_dict
        nested_dict={}
    return facial_distance_dict

def cosine_sim (two_dict):
    """
       A function to calculate cosine_similarities between two dictionaries.
       based on the given formular.
       
       It will except the situation when all coordinates are zeros to prevent crash.
       
    """
    
    a_list = two_dict[0]
    b_list = two_dict[1]
    a = 0.0
    b = 0.0
    c = 0.0
    for i in a_list.keys():
        a += a_list.get(i)**2
        b += b_list.get(i)**2
        c += a_list.get(i) * b_list.get(i)
        
    try:
        return c / ( a**(1/2) * b**(1/2) )
    except ZeroDivisionError:
        return None



def all_cosine_sim (filename,adultid):
    """
       A function to calculate all the cosine_similarities between
       two adultids given by the users & all the other adult ids,
       
       The function will :
       
       1 : Excluding the input ids for calculations. 
       1 : Returning None for the invalid/none-exsited id given by user.
       2 : Excluding any IDs which return a None cosine similaities result (ZeroDivisionError).
       3 : Sorting all the calculated cosine similarities in order (decreasing then alpha).
       4 : Returning None if there is not enough top 5 valid cosine similarities 

    """
    
    dictionary = calculate_facial_distance (filename)
    my_key = list(dictionary.keys()).copy()
    op3_result = []
    
    for i in adultid:
        if i in my_key:
            my_key.remove(i)
    
    for x in adultid:
        if dictionary.get(x,None) == None:
            op3_result.append (None)
        else:
            result_dict = {}
            for i in my_key:
                result_dict[i]=cosine_sim([dictionary.get(x),dictionary.get(i)])
                if result_dict[i] == None:
                    result_dict.pop(i)
            sorted_list = sorted(result_dict.items(),key=lambda x: x[0])
            sorted_list = sorted(sorted_list,key=lambda x: x[1],reverse=True)
            sorted_dict = dict([(k,round(v,4))for k,v in sorted_list])
            if len(sorted_dict) > 5:
                op3_result.append (list(sorted_dict.items())[:5])
            else:
                op3_result.append (None)
    return op3_result


def average_facial_distance (filename,adultid):
    """
       A function to calculate average_facial_distance for OP4,
       from: two sets of five closest cosine similarity facial data (OP3).
       
       1 : If any result is None in OP3, OP4 will return None too.
       2 : Retrieving the 2 sets of 5 adult IDs from OP3 first
       3 : Iterate and calculate averages from 15 landmarks
       4 : Returning two sets of result ( rounding to 4 decimals )

    """
    
    top_five = all_cosine_sim (filename,adultid)
    mydict = calculate_facial_distance (filename)
    final_result = []
    for i in top_five:
        if i == None:
            final_result.append(None)
        else:
            temp_list = []
            temp_dict = {}
            for x in i:
                temp_list.append(x[0])
            for adult_id in temp_list:
                for keys in mydict[adult_id].keys():
                    temp_dict[keys]=temp_dict.get(keys,0) + mydict[adult_id][keys]
            for y in temp_dict:
                temp_dict[y] = round((temp_dict[y]*(1/5)),4)
            final_result.append(temp_dict)
    return final_result
            

            
def dict_rounding (my_dict):
    result_dict ={}
    for i in my_dict:
        result_dict[i]=round((my_dict.get(i)),4)
    return result_dict
        
    
def main (csvfile,adultIDs):
    """
       The main function will check:
       
       1 : If csvfile is existed or blank, return None.
       2 : If user has given less or more than two adultIDs, notify the user. 
       3 : If both given ID are invalid, return None, produce report why they are invalid.
       4 : If only one given ID is valid, produce partial result and return None (where cannot be calculated)
       5 : If both given IDs are valid, produce full result. (If data given contain enough info to do so)
       6 : If both given IDs are valid, but one / both of their X,Y,Z, are zeros. Produce None where needed
       
    """
    file_checked = filereader(csvfile)
    if file_checked == None:
        op1,op2,op3,op4 = None,None,None,None
    else:
        adultid_upper = [x.strip().upper() for x in adultIDs]
        if len(adultid_upper) != 2:
            print ("Please provide two adultid only, you've provided {} id(s)".format(len(adultid_upper)))
            op1,op2,op3,op4 = None,None,None,None
        else:
            id_check = adultid_checker (csvfile,adultid_upper)
            if id_check == None:
                op1,op2,op3,op4 = None,None,None,None
            else:
                my_dict =  calculate_facial_distance (csvfile)
                op1 = []
                op1_no_rounding = []
                counter = 0
                for i in adultid_upper:
                    result = my_dict.get(i,None)
                    if result != None:
                        op1.append(dict_rounding(result))
                        op1_no_rounding.append(result)
                    else:
                        op1.append(result)
                        counter += 1
                if counter == 1:
                    op2 = None 
                elif cosine_sim(op1_no_rounding) == None:
                    op2 = None
                else:  
                    op2 = round((cosine_sim(op1_no_rounding)),4)
                op3 = all_cosine_sim(csvfile,adultid_upper)
                op4 = average_facial_distance (csvfile,adultid_upper)
            
    return op1,op2,op3,op4
        