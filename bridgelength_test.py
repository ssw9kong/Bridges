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

def get_total_length_on_highway(bridge_data, highway: str) -> float:
    """Return the total length of bridges in bridge_data on highway.
    Use zero for the length of bridges that do not have a length provided.
    If there are no bridges on highway, return 0.0.
    
    >>> get_total_length_on_highway(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_highway(THREE_BRIDGES, '401')
    0.0
    """
    #TODO
    
    for data_set in bridge_data:
        if data_set[2] == highway:
            highway_lens = [bridge_data[data_set][10] for data_set in range(len(bridge_data))]
            #highway_lens = []
            #highway_lens = highway_lens.append(bridge_data[data_set][10])
            return highway_lens
        else:
            return 0.0
    return 0.0

print (get_total_length_on_highway(THREE_BRIDGES, '403'))