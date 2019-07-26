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

THREE_BRIDGES_UNCLEANED = [['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233', 
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
     '90.1', '']]

THREE_BRIDGES = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567, '1965', '2014', '2009', 4, [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]

################################################
def format_data(data: List[List[str]]) -> None:  
    """Modify data so that it follows the format outlined in the 
    'Data formatting' section of the assignment handout.
    
    >>> d = THREE_BRIDGES_UNCLEANED
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    """
    id_n = 1
    outputList = []
    
    tempList=[]
    spanList=[]
    bciList=[]
    dataList=[]
    
    for element in data:
        spanStr=""
        spanList=[]
        dataList=[]
        
        spanStr = element[SPAN_LENGTH_INDEX]
        tempList = spanStr.split('=')
        
        for span in tempList:
            if (not 'Total' in span) and (not '(1)' in span):
                spanList.append(float(span.split(';')[0]))
 
                
        tempList = element[BCIS_INDEX + 1: len(element)-1]
        # # if you want remove empty BCI, use below code
        bciList=[]
        for bci in tempList: 
            if bci: ##check empty string
                bciList.append(float(bci))        
        # # ortherwise - bciList = tempList
        
        
        ##dataList.append(int(element[ID_INDEX].split('-')[0]))
        dataList.append(id_n)
        id_n+=1
        dataList.append(element[NAME_INDEX])
        dataList.append(element[HIGHWAY_INDEX])
        dataList.append(float(element[LAT_INDEX]))
        dataList.append(float(element[LON_INDEX]))
        dataList.append(element[YEAR_INDEX])
        dataList.append(element[LAST_MAJOR_INDEX])
        dataList.append(element[LAST_MINOR_INDEX])
        dataList.append(int(element[NUM_SPANS_INDEX]))
        
        dataList.append(spanList)
        
        if float(element[LENGTH_INDEX]) == int(float(element[LENGTH_INDEX])):
            dataList.append(int(element[LENGTH_INDEX]))
        else:
            dataList.append(float(element[LENGTH_INDEX]))
        
        dataList.append(element[LAST_INSPECTED_INDEX])
        
        dataList.append(bciList)
        ## one record done
        
        outputList.append(dataList)
        
    print(outputList)
        
    data[:] = list(outputList)
                
    ##return list(data)

    
    # TODO
    # Note: do not work on this function until you have implemented at
    # least some of the other functions below.
  
def get_bridge(bridge_data: List[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridge_data. If
    there is no bridge with the given id, return an empty list.  
    
    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567, '1965', '2014', '2009', 4, [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    
    >>> result = get_bridge(THREE_BRIDGES, 2)
    >>> result == [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567, '1965', '2014', '2009', 4, [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    False
    """
    
    #Set variable data to empty list
    #If statement False, the empty list is returned by default
    data = []
    
    for bridge_subdata in bridge_data:
        if bridge_subdata[ID_INDEX] == bridge_id:
            data = bridge_subdata
    
    return data 

def get_average_bci(bridge_data: List[list], bridge_id: int) -> float:
    """Return the average BCI for the bridge with bridge_id from bridge_data.
    If there is no bridge with the id bridge_id, return 0.0. If there are no
    BCIs for the bridge with id bridge_id, return 0.0.
    
    >>> get_average_bci(THREE_BRIDGES, 1)
    70.88571428571429
    >>> get_average_bci(THREE_BRIDGES, 2)
    70.14285714285714
    >>> get_average_bci(THREE_BRIDGES, 3)
    74.4
    >>> get_average_bci(THREE_BRIDGES, 4)
    0.0
    #Arbitrary 13 element list with one list containing an empty list at a[2][BCIS_INDEX]
    >>>a = [[1,1,1,1,1,1,1,1,1,1,1,1,[1,1,1,1,1,1]], 
    [3,1,1,1,1,1,1,1,1,1,1,1,[3,3,3,3,3,3,3,3]], [5,1,1,1,1,2,1,1,1,1,1,1,[]]]
    >>> get_average_bci(a, 5)
    0.0
    """
    #Set bci to 0.0 by defalut in case nonexsistant id or empty BCI
    bci = 0.0
    
    for subdata in bridge_data:
        if subdata[ID_INDEX] == bridge_id:
            if len(subdata[BCIS_INDEX]) > 0:
                #the sum of int in list is divided by its length
                bci = sum(subdata[BCIS_INDEX])/len(subdata[BCIS_INDEX])
    
    #returned the bci value
    return bci

def get_total_length_on_highway(bridge_data: List[list], highway: str) -> float:
    """Return the total length of bridges in bridge_data on highway.
    Use zero for the length of bridges that do not have a length provided.
    If there are no bridges on highway, return 0.0.
    
    >>> get_total_length_on_highway(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_highway(THREE_BRIDGES, '401')
    0.0
    """
    #length is set by default to zero for nonexsistant bridges
    length = 0.0
    
    for bridge_subdata in bridge_data:
        if bridge_subdata[HIGHWAY_INDEX] == highway:
            #Add length to sum of length
            length = bridge_subdata[LENGTH_INDEX] + length
    return length

def get_distance_between(bridge1: list, bridge2: list) -> float:
    """Return the distance in kilometres, rounded to the nearest metre
    (i.e., 3 decimal places), between the two bridges bridge1 and bridge2.
        
    >>> get_distance_between(get_bridge(THREE_BRIDGES, 1), \
                                 get_bridge(THREE_BRIDGES, 2))
    1.968
    """
  

    #Under assumption that bridge1, bridge2 in data    
    if bridge1 != [] and bridge2 != []:
        return round(calculate_distance(bridge1[LAT_INDEX], \
                                        bridge1[LON_INDEX], bridge2[LAT_INDEX], bridge2[LON_INDEX]), 3)
    #WHAT IF ONE OF THE BRIDGES DNE?
    #else: return None? not sure.
    
def find_closest_bridge(bridge_data: List[list], bridge_id: int) -> int:
    """Return the id of the bridge in bridge_data that has the shortest
    distance to the bridge with id bridge_id.
    
    Precondition: a bridge with bridge_id is in bridge_data, and there are
    at least two bridges in bridge_data
    
    >>> find_closest_bridge(THREE_BRIDGES, 2)
    1
    >>> find_closest_bridge(THREE_BRIDGES, 1)
    2
    """ 
    t = 0 #Set up marker used for indexing
    distance = 0 #dummy variable to store distance
    distance_bridge = [] #Use parallel list to bridge_data
    ref_list = [] #distance index list
    while t in range(len(bridge_data)):
        bridge_temp_data = get_bridge(bridge_data, t + 1) #Temp bridge data storage
        distance = get_distance_between(get_bridge(bridge_data, bridge_id), \
                                        bridge_temp_data)
        distance_bridge.append(distance)
        t = t + 1
            
    #stored distances as tuple for future indexing
    ref_list = tuple(distance_bridge)
    #distance between bridge and self is zero (remove it)
    distance_bridge.remove(0.0)
    #selected and stored min bridge distance (excluding self)
    min_dist = min(distance_bridge)
    #found index of selected bridge in bridge_data
    #and returned list id
    return bridge_data[ref_list.index(min_dist)][ID_INDEX]

def find_bridges_in_radius(bridge_data: List[list], lat: float,
                           long: float, distance: float) -> List[int]:
    """Return the IDs of the bridges that are within radius distance
    from (lat, long).
    
    >>> find_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    """
    #list to store id of bridges within range
    list_ID = []
    #set up marker for loop
    t = 0
    
    while t in range(len(bridge_data)):
        #index and store subdata
        subdata = get_bridge(bridge_data, t + 1)
        #store lat and long of bridge
        bridge_lat = subdata[LAT_INDEX]
        bridge_long = subdata[LON_INDEX]
        #find distance between ref point and bridge 
        dist_from_centre = calculate_distance(lat, long,
                       bridge_lat, bridge_long)
        if dist_from_centre <= distance:
            list_ID.append(subdata[ID_INDEX])
            t = t + 1
        else:
            t = t + 1
    return list_ID

def get_bridges_with_bci_below(bridge_data: List[list], bridge_ids: List[int],
                               bci_limit: float) -> List[int]:
    """Return the IDs of the bridges with ids in bridge_ids whose most recent
    BCIs are less than or equal to bci_limit.

 
    
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1, 2], 72)
    [2]
    """
    
    IDList=[]
    
    for br in bridge_data:
        if br[ID_INDEX] in bridge_ids:
            if br[BCIS_INDEX][0] <= bci_limit:
                IDList.append(br[ID_INDEX])
                
    return IDList
    
    # TODO - not sure, still working on it

def get_bridges_containing(bridge_data: List[list], search: str) -> List[int]:
    """
    Return a list of IDs of bridges whose names contain search (case
    insensitive).
    
    >>> get_bridges_containing(THREE_BRIDGES, 'underpass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'Highway')
    [1]
    """
    #Created empty list for id storage
    id_list = []
    
    for subdata in bridge_data:
        #standardized case of search and bridge name
        if search.lower() in subdata[NAME_INDEX].lower():
            #added id of inquired bridge
            id_list.append(subdata[ID_INDEX])
            
    return id_list

def assign_inspectors(bridge_data: List[list], inspectors: List[List[float]],
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


def inspect_bridges(bridge_data: List[list], bridge_ids: List[int], date: str, 
                    bci: int) -> None:
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
    #Stored bridge data in a variable
    data = get_bridge(bridge_data, bridge_id)
    #Checked significance of rehab and made replacement
    if is_major is True:
        data[LAST_MAJOR_INDEX] = new_date
    elif is_major is False:
        data[LAST_MINOR_INDEX] = new_date



if __name__ == '__main__':
    # #pass 
    
    #print(format_data(THREE_BRIDGES_UNCLEANED))
    ##print(get_bridges_with_bci_below(THREE_BRIDGES, [1, 2,3], 70))
    
    d = THREE_BRIDGES_UNCLEANED
    format_data(d)
    print(d)
    print(d == THREE_BRIDGES )  
    
    # # To test your code with larger lists, you can uncomment the code below to
    # # read data from the provided CSV file.
    #bridges = read_data(open('bridge_data.csv'))
    #format_data(bridges)

    # # For example,
    #print(get_bridge(bridges, 3))
    #expected = [3, 'NORTH PARK STEET UNDERPASS', '403', 43.165918, -80.263791,
    #             '1962', '2013', '2009', 4, [12.2, 18.0, 18.0, 12.2], 60.8,
    #             '04/13/2012', [71.4, 69.9, 67.7, 68.9, 69.1, 69.9, 72.8]]
    #print('Testing get_bridge: ', \
    #      get_bridge(bridges, 3) == expected)
