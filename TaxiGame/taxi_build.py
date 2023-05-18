from GANN import ANN



class Node:
    def __init__(self, node_id,longitude,latitude,connected_nodes_list,travel_times):
        self.node_id = node_id
        self.longitude = longitude
        self.latitude = latitude
        self.connected_nodes_list = connected_nodes_list
        self.connected_nodes = []
        self.travel_times = travel_times
        self.passengers = []

class Passenger:
    def __init__(self, pickup_node, dropdown_node, pickup_time, dropoff_time, trip_duration):
        self.pickup_node = pickup_node
        self.dropdown_node = dropdown_node
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time
        self.trip_duration = trip_duration

class Taxi:
    def __init__(self):
        self.id = 0
        self.current_node = Node(0,0,0,[],[])
        self.is_full = False
        self.number_of_rides = 0
        self.passenger_tavel_time = 0
        self.passed_nodes = []
        self.total_travel_time = 0 
        self.ANN = ANN()   
        

    def pickup_passenger(self, node):
        if len(node.passengers) > 0:
            self.is_full = True
            self.number_of_rides += 1
            self.passenger = node.passenger[0]
            self.passenger_tavel_time += node.passengers[0].trip_duration
            node.passenger.pop(0)
            node = self.passenger.dropdown_node

