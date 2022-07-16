'''Module 4: Individual Programming Assignment 1

Parsing Data

This assignment covers your ability to manipulate data in Python.
'''

def relationship_status(from_member, to_member, social_graph):
    '''Relationship Status.
    20 points.

    Let us pretend that you are building a new app.
    Your app supports social media functionality, which means that users can have
    relationships with other users.

    There are two guidelines for describing relationships on this social media app:
    1. Any user can follow any other user.
    2. If two users follow each other, they are considered friends.

    This function describes the relationship that two users have with each other.

    Please see "assignment-4-sample-data.py" for sample data. The social graph
    will adhere to the same pattern.

    Parameters
    ----------
    from_member: str
        the subject member
    to_member: str
        the object member
    social_graph: dict
        the relationship data    

    Returns
    -------
    str
        "follower" if fromMember follows toMember,
        "followed by" if fromMember is followed by toMember,
        "friends" if fromMember and toMember follow each other,
        "no relationship" if neither fromMember nor toMember follow each other.
    '''
    
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    
    # Get the list of the following of the members
    from_member_following = social_graph[from_member]["following"] # Gives a list of From Member's following
    to_member_following = social_graph[to_member]["following"] # Gives a list of To Member's following
    
    # Check if Friends: if fromMember and toMember follow each other
    if (from_member in to_member_following) and (to_member in from_member_following): 
        return "friends"
    # Check if Follower: if fromMember follows toMember
    elif to_member in from_member_following:
        return "follower"
    # Check if Followed By: if fromMember is followed by toMember
    elif from_member in to_member_following:
        return "followed by"
    # Check if No Relationship: if neither fromMember nor toMember follow each other.
    else:
        return "no relationship"


def tic_tac_toe(board):
    '''Tic Tac Toe. 
    25 points.

    Tic Tac Toe is a common paper-and-pencil game. 
    Players must attempt to successfully draw a straight line of their symbol across a grid.
    The player that does this first is considered the winner.

    This function evaluates a tic tac toe board and returns the winner.

    Please see "assignment-4-sample-data.py" for sample data. The board will adhere
    to the same pattern. The board may by 3x3, 4x4, 5x5, or 6x6. The board will never
    have more than one winner. The board will only ever have 2 unique symbols at the same time.

    Parameters
    ----------
    board: list
        the representation of the tic-tac-toe board as a square list of lists

    Returns
    -------
    str
        the symbol of the winner or "NO WINNER" if there is no winner
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    
    results = []
    
    # Horizontal Patterns
    horizontals_list = board
    for horizontal in horizontals_list:
        if len(set(horizontal)) == 1:
            results.append(horizontal[0])
    
    # Vertical Patterns
    verticals_list = list(zip(*board))
    for vertical in verticals_list: 
        if len(set(vertical)) == 1:
            results.append(vertical[0])
    
    # Diagonal Up-Down Pattern
    diagonal_updown = [board[i][i] for i in range(len(board))]
    if len(set(diagonal_updown)) == 1:
        results.append(diagonal_updown[0])
    
    # Diagonal Down-Up Pattern
    diagonal_downup = [board[len(board)-1-i][i] for i in range(len(board))]
    if len(set(diagonal_downup)) == 1:
        results.append(diagonal_downup[0])
    
    # Check for Winner
    check_winner = set(results)
    if len(check_winner) == 1:
        return (list(check_winner))[0]
    else:
        return "NO WINNER"

def eta(first_stop, second_stop, route_map):
    '''ETA. 
    25 points.

    A shuttle van service is tasked to travel along a predefined circlar route.
    This route is divided into several legs between stops.
    The route is one-way only, and it is fully connected to itself.

    This function returns how long it will take the shuttle to arrive at a stop
    after leaving another stop.

    Please see "mod-4-ipa-1-sample-data.py" for sample data. The route map will
    adhere to the same pattern. The route map may contain more legs and more stops,
    but it will always be one-way and fully enclosed.

    Parameters
    ----------
    first_stop: str
        the stop that the shuttle will leave
    second_stop: str
        the stop that the shuttle will arrive at
    route_map: dict
        the data describing the routes

    Returns
    -------
    int
        the time it will take the shuttle to travel from first_stop to second_stop
    '''
    
    # List of all stops (both first stops and second stops)
    all_stops = list(route_map.keys())
    
    # List of dictionaries containing info about travel time from one stop to another
    travel_times_info = list(route_map.values())
   
    # List of possible first stops in order
    first_stops_list  = [all_stops[i][0] for i in range(len(all_stops))]

    # List of possible second stops in order
    second_stops_list = [all_stops[i][1] for i in range(len(all_stops))]

    # List of travel time values (in minutes) from one stop to another in order
    travel_times_list = [travel_times_info[x]["travel_time_mins"] for x in range(len(travel_times_info))]    

    # Indeces of the first stop and the second stop in their respective lists
    first_stop_index = first_stops_list.index(first_stop)
    second_stop_index = second_stops_list.index(second_stop)

    # Get the sum of the total travel time
    start = first_stop_index
    total_time = travel_times_list[start] # Initial value of total travel time, assuming that once a person rides the van, they'll alight at the next stop AT LEAST
    while start != second_stop_index:
        total_time += travel_times_list[(start + 1) % len(travel_times_list)] # Modulo was used so it can loop around like a circular route
        start = (start + 1) % len(travel_times_list)
     
    return total_time