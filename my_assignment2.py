""" 
Assignment 2: Bridges

The data used for this assignment is a subset of the data found in:
https://www.ontario.ca/data/bridge-conditions
"""

import csv
import math
from typing import List, TextIO

ID_INDEX = 0
NAME_INDEX = 1
HIGHWAY_INDEX = 2
LAT_INDEX = 3
LON_INDEX = 4
YEAR_INDEX = 5
LAST_MAJOR_INDEX = 6
LAST_MINOR_INDEX = 7
NUM_SPANS_INDEX = 8
SPAN_LENGTH_INDEX = 9
LENGTH_INDEX = 10
LAST_INSPECTED_INDEX = 11
BCIS_INDEX = 12

HIGH_PRIORITY_BCI = 60   
MEDIUM_PRIORITY_BCI = 70
LOW_PRIORITY_BCI = 100

HIGH_PRIORITY_RADIUS = 500  
MEDIUM_PRIORITY_RADIUS = 250
LOW_PRIORITY_RADIUS = 100

EARTH_RADIUS = 6371

####### BEGIN HELPER FUNCTIONS ####################

def read_data(csv_file: TextIO) -> List[List[str]]:
    """Read and return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of csv_file.

    Docstring examples not given since results depend on csv_file.
    """ 

    data = []
    lines = csv.reader(csv_file)
    for line in lines:            
        data.append(line)
    data = data[2:]
    return data


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by   
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.
    
    >>> calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> calculate_distance(43.42, -79.24, 53.32, -113.30)
    2713.226
    """

    # This function uses the haversine function to find the
    # distance between two locations. You do NOT need to understand why it
    # works. You will just need to call on the function and work with what it
    # returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1), 
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1 
    lat_diff = lat2 - lat1 
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return round(c * EARTH_RADIUS, 3)


####### END HELPER FUNCTIONS ####################

### SAMPLE DATA TO USE IN DOCSTRING EXAMPLES ####

THREE_BRIDGES_UNCLEANED = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2009', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
    ]

THREE_BRIDGES = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,
                  -80.275567, '1965', '2014', '2009', 4,
                  [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, 
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,
                                 73.3]],
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958',
                  '2013', '', 1, [16.0], 18.4, '08/28/2013',
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]                 
                ]

#################################################
def format_data(data: List[List[str]]) -> None:  
    """Modify data so that it follows the format outlined in the 
    'Data formatting' section of the assignment handout.
    
    >>> d = THREE_BRIDGES_UNCLEANED
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    """

    # TODO
    # Note: do not work on this function until you have implemented at
    # least some of the other functions below.
    counter = 0
    formatted_bridges = []
    
    while counter < len(data):
        bridge_list = []
        
        span_list = []
        x = data[counter]
        spans = data[counter][SPAN_LENGTH_INDEX]
        span_list = spans.split('=')
        span_list = span_list[2:] #starting from index 2
        span_list = [string.split(';')[0] for string in span_list]
        span_list = [float(string) for string in span_list]
        
        bcis_list = data[counter][BCIS_INDEX +1:] #leave out first bci bc it's the most recent repeat
        bcis_list = [float(bci) for bci in bcis_list if bci != '']
        
        bridge_list.append(counter + 1) #bridge id
        bridge_list.append(data[counter][NAME_INDEX]) #bridge name
        bridge_list.append(data[counter][HIGHWAY_INDEX]) #highway
        bridge_list.append(float(data[counter][LAT_INDEX])) #latitude
        bridge_list.append(float(data[counter][LON_INDEX])) #longitude
        bridge_list.append(data[counter][YEAR_INDEX])
        bridge_list.append(data[counter][LAST_MAJOR_INDEX])
        bridge_list.append(data[counter][LAST_MINOR_INDEX])
        bridge_list.append(int(data[counter][NUM_SPANS_INDEX]))
        bridge_list.append(span_list)
        
        length_data = data[counter][LENGTH_INDEX]
        if not length_data:
            length_data = '0'
        bridge_list.append(float(length_data)) 
        
        bridge_list.append(data[counter][LAST_INSPECTED_INDEX])       
        bridge_list.append(bcis_list)
        
        formatted_bridges.append(bridge_list)
        
        counter += 1
    
    #overwrite original data with new data
    data.clear()
    data.extend(formatted_bridges)
        
        

 
def get_bridge1(bridge_data: List[list], bridge_id: int) -> list:
    
    for data_set in range(len(bridge_data)):
        if bridge_data[data_set][0] == bridge_id:
            return bridge_data[data_set]
    return [] 

def get_bridge(bridge_data: List[list], bridge_id: int) -> list:
    return_list =[]
    for data_set in bridge_data:
        if data_set[ID_INDEX] == bridge_id:
            return_list = data_set
    return return_list

    """Return the data for the bridge with id bridge_id from bridge_data. If
    there is no bridge with the given id, return an empty list.  
    
    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, \
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    """
       
    # TODO
#space
def get_average_bci(bridge_data: List[list], bridge_id: int) -> float:
    """Return the average BCI for the bridge with bridge_id from bridge_data.
    If there is no bridge with the id bridge_id, return 0.0. If there are no
    BCIs for the bridge with id bridge_id, return 0.0.
    
    >>> get_average_bci(THREE_BRIDGES, 1)   
    70.88571428571429
    """
    # TODO
    average_bci = 0.0
    for data_set in bridge_data:
        if bridge_id == data_set[ID_INDEX]:
            bci_sum = sum(data_set[BCIS_INDEX])
            bci_amount = len(data_set[BCIS_INDEX])
            if bci_amount != 0:
                average_bci = bci_sum/bci_amount
    return average_bci
#space
def get_total_length_on_highway(bridge_data: List[list], highway: str) -> float:
    """Return the total length of bridges in bridge_data on highway.
    Use zero for the length of bridges that do not have a length provided.
    If there are no bridges on highway, return 0.0.
    
    >>> get_total_length_on_highway(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_highway(THREE_BRIDGES, '401')
    0.0
    """
    #TODO
    return_value = 0.0
    for data_set in bridge_data:
        if data_set[HIGHWAY_INDEX] == highway:
            return_value += data_set[LENGTH_INDEX]
    return return_value

def get_distance_between(bridge1: list, bridge2: list) -> float:
    """Return the distance in kilometres, rounded to the nearest metre
    (i.e., 3 decimal places), between the two bridges bridge1 and bridge2.
        
    >>> get_distance_between(get_bridge(THREE_BRIDGES, 1), \
                                 get_bridge(THREE_BRIDGES, 2))
    1.968
    """
    # TODO
    # Hint: use the provided helper function calculate_distance.
    distance_between = -1.0
    if len(bridge1) != 0 and len(bridge2) != 0:
        
        #lat_bridge1 = bridge1[LAT_INDEX]
        #lon_bridge1 = bridge1[LON_INDEX]
        #lat_bridge2 = bridge2[LAT_INDEX]
        #lon_bridge2 = bridge2[LON_INDEX]   
        distance_between = calculate_distance(bridge1[LAT_INDEX], bridge1[LON_INDEX],
                           bridge2[LAT_INDEX], bridge2[LON_INDEX]) 
    return distance_between
    
    
def find_closest_bridge1(bridge_data: List[list], bridge_id: int) -> int:
    """Return the id of the bridge in bridge_data that has the shortest
    distance to the bridge with id bridge_id.
    
    Precondition: a bridge with bridge_id is in bridge_data, and there are
    at least two bridges in bridge_data
    
    >>> find_closest_bridge(THREE_BRIDGES, 2)
    1
    """
    # TODO
    #distances = []
    #for data_set in bridge_data:
        #distances.append(get_distance_between(data_set, get_bridge(bridge_data, bridge_id)))
    #distances.remove(0.0) #how to not include distance btw itself
    #min_dist_indx = distances.index(min(distances))
    #return bridge_data[min_dist_indx][ID_INDEX]
    
   #if get_bridge(bridge_data, bridge_id) in bridge_data and len(bridge_data) >= 2
    select_bridge = get_bridge(bridge_data, bridge_id)
    min_distance = get_distance_between(bridge_data[0], select_bridge)
    min_bridge = bridge_data[0]     
    
    for bridge in bridge_data:
        new_distance = get_distance_between(bridge, select_bridge)
        if new_distance != 0:
            if min_distance == 0 :
                min_distance = new_distance
                min_bridge = bridge
            elif new_distance < min_distance:
                min_distance = new_distance
                min_bridge = bridge  
            
    return min_bridge[ID_INDEX]
#######

def find_closest_bridge(bridge_data: List[list], bridge_id: int) -> int:
    my_bridge_data = []
    select_bridge = get_bridge(bridge_data, bridge_id)
    for bridge in bridge_data:
        bridge_dist = get_distance_between(bridge, select_bridge)
        if bridge_dist != 0:
            my_bridge_data.append([bridge_dist, bridge])
        
    min_mybridge = min(my_bridge_data)
    
    return min_mybridge[1][ID_INDEX]
##########

def find_closest_bridge2(bridge_data: List[list], bridge_id: int) -> int:
    my_bridge_data = []
    select_bridge = get_bridge(bridge_data, bridge_id)
    for bridge in bridge_data:
        bridge_dist = get_distance_between(bridge, select_bridge)
        if bridge_dist != 0:
            my_bridge_data.append([bridge, bridge_dist])
        
    min_mybridge = min(my_bridge_data, key = bridge_dist)
    
    return min_mybridge[1][ID_INDEX]

def find_closest_bridge3(bridge_data: List[list], bridge_id: int) -> int:
    specified_bridge = get_bridge(bridge_data, bridge_id)
    new_bridge_data = bridge_data
    new_bridge_data.remove(specified_bridge)
    min_dist = get_distance_between(new_bridge_data[0], specified_bridge)
    min_bridge = new_bridge_data[0][ID_INDEX]
    for bridge in new_bridge_data:
        new_dist = get_distance_between(bridge, specified_bridge)
        if new_dist < min_dist:
            min_dist = new_dist
            min_bridge = bridge[ID_INDEX]
    return min_bridge


def find_bridges_in_radius(bridge_data: List[list], lat: float, long: float,
                           distance: float) -> List[int]:
    """Return the IDs of the bridges that are within radius distance
    from (lat, long).
    
    >>> find_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    """
    # TODO
    bridge_within = []
    for bridge in bridge_data:
        if calculate_distance(bridge[LAT_INDEX], bridge[LON_INDEX],
                           lat, long) <= distance:
            bridge_within.append(bridge[ID_INDEX])
    return bridge_within
        


def get_bridges_with_bci_below(bridge_data: List[list], bridge_ids: List[int],
                               bci_limit: float) -> List[int]:
    """Return the IDs of the bridges with ids in bridge_ids whose most
    recent BCIs are less than or equal to bci_limit.
    
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1, 2], 72)
    [2]
    """
    # TODO
    lower_BCI = []
    for bridge in bridge_ids:
        current_bridge = get_bridge(bridge_data, bridge)
        if current_bridge[BCIS_INDEX][0] <= bci_limit:
            lower_BCI.append(current_bridge[ID_INDEX])
    return lower_BCI


def get_bridges_containing(bridge_data: List[list], search: str) -> List[int]:
    """
    Return a list of IDs of bridges whose names contain search (case
    insensitive).
    
    >>> get_bridges_containing(THREE_BRIDGES, 'underpass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'Highway')
    [1]
    """
    # TODO
    positive_search = []
    
    for bridge in bridge_data:
        #search_list = bridge[NAME_INDEX].upper().split()
        #if search.upper() in search_list:
            #positive_search.append(bridge[ID_INDEX])
        if " " + search.upper() + " " in " " + bridge[NAME_INDEX].upper() + " ":
            positive_search.append(bridge[ID_INDEX])
    return positive_search

            


def assign_inspectors1(bridge_data: List[list], inspectors: List[List[float]],
                      max_bridges: int) -> List[List[int]]:
    """Return a list of bridge IDs to be assigned to each inspector in
    inspectors. inspectors is a list containing (latitude, longitude) pairs
    representing each inspector's location.
    
    At most max_bridges bridges should be assigned to an inspector, and each
    bridge should only be assigned once (to the first inspector that can
    inspect that bridge).
    
    See the "Assigning Inspectors" section of the handout for more details.
    
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    [[1]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)
    [[1], [2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    [[1, 2], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]], 2)
    [[1, 2], [3]]
    >>> assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]], 2)
    [[], [1, 2]]
    """
    # TODO
    bridge_id_list = [item[0] for item in bridge_data]
    
    high_priority_bridges = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(HIGH_PRIORITY_BCI))
    medium_priority_bridges = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(MEDIUM_PRIORITY_BCI)) - high_priority_bridges
    low_priority_bridges = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(LOW_PRIORITY_BCI)) - medium_priority_bridges - low_priority_bridges
    
    total_assigned_bridges = []


    for inspector in inspectors:
        hp_in_radius = find_bridges_in_radius(bridge_data, inspector[0], inspector[1], float(HIGH_PRIORITY_RADIUS))
        mp_in_radius = find_bridges_in_radius(bridge_data, inspector[0], inspector[1], float(MEDIUM_PRIORITY_RADIUS))
        lp_in_radius = find_bridges_in_radius(bridge_data, inspector[0], inspector[1], float(LOW_PRIORITY_RADIUS))
        
        assigned_bridges = []
        
        for bridge in hp_in_radius:
            if bridge in high_priority_bridges and len(assigned_bridges) < max_bridges:
                assigned_bridges.append(bridge)
                high_priority_bridges.remove(bridge)
            elif bridge in medium_priority_bridges and len(assigned_bridges) < max_bridges:
                if bridge in mp_in_radius:
                    assigned_bridges.append(bridge)  
                    medium_priority_bridges.remove(bridge)
            elif bridge in low_priority_bridges and len(assigned_bridges) < max_bridges:
                if bridge in lp_in_radius:
                    assigned_bridges.append(bridge)  
                    low_priority_bridges.remove(bridge)
            #else:
                #pass
        total_assigned_bridges.append(assigned_bridges)                
    
    return total_assigned_bridges

def assign_inspectors(bridge_data: List[list], inspectors: List[List[float]],
                      max_bridges: int) -> List[List[int]]:
    
    bridge_id_list = [item[0] for item in bridge_data]
    
    total_assigned_bridges = []    
    
    for inspector in inspectors:
        HP_bridge_id_list = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(HIGH_PRIORITY_BCI))
        MP_bridge_id_list = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(MEDIUM_PRIORITY_BCI))
        MP_bridge_id_list= [bid for bid in MP_bridge_id_list
                            if bid not in HP_bridge_id_list]
        LP_bridge_id_list = get_bridges_with_bci_below(bridge_data, bridge_id_list, float(LOW_PRIORITY_BCI))
        LP_bridge_id_list = [bid for bid in LP_bridge_id_list
                             if (bid not in MP_bridge_id_list) 
                                and (bid not in HP_bridge_id_list)]
        
        HP_bridge_data_L = []
        MP_bridge_data_L = []
        LP_bridge_data_L = []    
        
        for bridge_id in HP_bridge_id_list:
            HP_bridge_data_L.append(get_bridge(bridge_data,bridge_id))
        for bridge_id in MP_bridge_id_list:
            MP_bridge_data_L.append(get_bridge(bridge_data,bridge_id))
        for bridge_id in LP_bridge_id_list:
            LP_bridge_data_L.append(get_bridge(bridge_data,bridge_id))        
        
        hp_inrad_id_L = find_bridges_in_radius(HP_bridge_data_L, inspector[0], inspector[1], float(HIGH_PRIORITY_RADIUS))
        mp_inrad_id_L = find_bridges_in_radius(MP_bridge_data_L, inspector[0], inspector[1], float(MEDIUM_PRIORITY_RADIUS))
        lp_inrad_id_L = find_bridges_in_radius(LP_bridge_data_L, inspector[0], inspector[1], float(LOW_PRIORITY_RADIUS))
        
        possible_assignment_list = hp_inrad_id_L + mp_inrad_id_L + lp_inrad_id_L
        if len(possible_assignment_list) < max_bridges:
            max_bridges_1 = len(possible_assignment_list)
            assigned_bridges = possible_assignment_list[0:max_bridges_1]
        
        assigned_bridges = possible_assignment_list[0:max_bridges]
        bridge_id_list = [bridge_id for bridge_id in bridge_id_list if bridge_id not in assigned_bridges]
      
        #for select_bridge_id in possible_assignment_list:
            #if len(assigned_bridges) < max_bridges:
                #assigned_bridges.append(select_bridge_id)
                #bridge_id_list.remove(select_bridge_id)
    
        total_assigned_bridges.append(assigned_bridges)       
        
    return total_assigned_bridges




def inspect_bridges(bridge_data: List[list], bridge_ids: List[int], date: str, 
                    bci: float) -> None:
    """Update the bridges in bridge_data with id in bridge_ids with the new
    date and BCI score for a new inspection.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> inspect_bridges(bridges, [1], '09/15/2018', 71.9)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2009', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '09/15/2018', \
                     [71.9, 72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """
    
    # TODO
    #select_bridge = get_bridge(bridge_data, bridge_id[0])
    #select_bridge[LAST_INSPECTED_INDEX] = date
    #select_bridge[BCIS_INDEX][0] = bci
    
    #my_bridge_data = []
    #updated_bridge_data = []
    #for bridge in bridge_data:
        #my_bridge_data.append([bridge, bridge[ID_INDEX]])
        
    #for select_bridge in my_bridge_data:
        #if bridge_ids[0] == select_bridge[1]:
            #select_bridge[0][LAST_INSPECTED_INDEX] = date
            #select_bridge[0][BCIS_INDEX].insert(0, bci)
    
    #for select_bridge in my_bridge_data:
        #updated_bridge_data.append(select_bridge[0])
    
    #return updated_bridge_data

    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_ids[0]:
            bridge[LAST_INSPECTED_INDEX] = date
            bridge[BCIS_INDEX].insert(0, bci)            

    #return bridge_data    


def add_rehab(bridge_data: List[list], bridge_id: int, new_date: str, 
              is_major: bool) -> None:
    """
    Update the bridge with the id bridge_id to have its last rehab set to
    new_date. If is_major is True, update the major rehab date. Otherwise,
    update the minor rehab date.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> add_rehab(bridges, 1, '2018', False)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2018', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """
    # TODO
    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_id:
            if is_major is True:
                bridge[LAST_MAJOR_INDEX] = new_date
            else:
                bridge[LAST_MINOR_INDEX] = new_date
    return bridge_data



if __name__ == '__main__':
    #pass 
    #a = get_bridge(THREE_BRIDGES, 3)
    #a = get_total_length_on_highway(THREE_BRIDGES, '403')
    #a = get_average_bci(THREE_BRIDGES, 4)
    #a = get_distance_between(get_bridge(THREE_BRIDGES,1), get_bridge(THREE_BRIDGES,3))
    #a = find_closest_bridge(THREE_BRIDGES, 1)
    #a = find_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    #a = get_bridges_with_bci_below(THREE_BRIDGES, [1, 2, 3], 84)
    #a = get_bridges_containing(THREE_BRIDGES, 'underpass') 
    
    #a = assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    #b = assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    #c = assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    #d = assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)    
    #e = assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    #f = assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]], 2)    
    #g = assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]], 2)
    #list = [a, b, c, d, e, f, g]
    #for letter in list:
        #print(letter)
    
    #inspect_bridges(THREE_BRIDGES, [1], '09/15/2018', 71.9)
    #a = add_rehab(THREE_BRIDGES, 2, '2019', True)
    #print(THREE_BRIDGES)
    
    bridge_data_csv_list = read_data(open('bridge_data.csv'))
    bridge_data_csv_list = bridge_data_csv_list
    format_data(bridge_data_csv_list)
    a = get_bridges_containing(bridge_data_csv_list, '')
    print(a)
    # # To test your code with larger lists, you can uncomment the code below to
    # # read data from the provided CSV file.
    # bridges = read_data(open('bridge_data.csv'))
    # format_data(bridges)

    # # For example,
    # print(get_bridge(bridges, 3))
    # expected = [3, 'NORTH PARK STEET UNDERPASS', '403', 43.165918, -80.263791,
    #             '1962', '2013', '2009', 4, [12.2, 18.0, 18.0, 12.2], 60.8,
    #             '04/13/2012', [71.4, 69.9, 67.7, 68.9, 69.1, 69.9, 72.8]]
    # print('Testing get_bridge: ', \
    #      get_bridge(bridges, 3) == expected)
