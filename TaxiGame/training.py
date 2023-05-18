from taxi_build import Node, Taxi, Passenger
from GANN import ANN, crossover
from datetime import datetime
from random import randint, choice
from numpy import argmax, savetxt
import pandas as pd
import logging
from dateutil.parser import parse
from sklearn.preprocessing import normalize
from csv import reader, writer
from numpy import save

with open('test/nodes.csv', 'r') as f:
    # Skip the header row
    reader = reader(f)
    next(reader)  # skip the header row
    graph = []

    for row in reader:
        node_id, longitude, latitude, connected_nodes, travel_times = row
        connected_nodes_list = eval(connected_nodes)
        travel_times_list = eval(travel_times)
        #print(f'Connected Nodes: {connected_nodes_list}')
        #print(f'Travel Times: {travel_times_list}')
        node = Node(node_id, float(longitude), float(latitude), connected_nodes_list, travel_times_list)
        graph.append(node)
    
    for node in graph:
        for connected_node in node.connected_nodes_list:
            for node2 in graph:
                if connected_node == node2.node_id:
                    node.connected_nodes.append(node2)
                
            

    """
    next(f)

    for line in f:
        row = line.split('[')
        # extract connected nodes and travel times
        connected_nodes = row[1][1:-1].split(', ')
        travel_times = row[3][1:-1].split(', ')
        print(connected_nodes, travel_times)
        # convert travel times to floats
        travel_times = [float(t) for t in travel_times]
        """


with open('test/clean_data_with_nodes.csv', 'r') as f:
    # Skip the header row
    next(f)  
    passengers = []

    for row in f:
        trip_duration = row[7]
        pickup_node_id = row[8]
        dropdown_node_id = row[9]
        #print(row)
        values = row.split(',')
        # Extract the pickup and dropoff datetime values
        pickup_datetime = values[1]
        dropoff_datetime = values[2]
        pickup_time = parse(pickup_datetime)
        dropoff_time = parse(dropoff_datetime)
        #print(pickup_time,dropoff_time)
        ptime = int(pickup_time.timestamp() / 60)
        dtime = int(dropoff_time.timestamp() / 60)
        #print(ptime,dtime)
        passengers.append(Passenger(pickup_node_id, dropdown_node_id, ptime, dtime, trip_duration))
    
# store all active ANNs
taxis = []
pool = []

# Initial Population
population = 5

for i in range(population):
    taxis.append(Taxi())
    taxis[i].id = i
for taxi in taxis:
    taxi.current_node = graph[randint(0, 211)]

# Store Max Fitness Weights
optimal_weights = []
#rows is  avariable for to save the information for graphing
rows = []

# Evolution Loop
epochs = 100
for i in range(epochs):

    time = 0
    while  time < 13 * 60:           #return it to when i am done testing time <= 13 * 60

        #add the passengers to the nodes
        while passengers[0].pickup_time < time:
            for node in graph:
                if node.id == passengers[0].pickup_node:
                    node.passengers.append(passengers[0])
            passengers.pop(0)

        #every taxi will make a choice on what node to go to next and move all the taxis to the node they chose
        for taxi in taxis:
            if taxi.is_full == False:
                
                # the taxi will only chose from 5 nodes some have 6 but they are a small in number
                for node in graph:
                    if node.node_id == taxi.current_node:
                        taxi.current_node = node

                input_data = []
                #the taxi know were the other taxies are. remember to increase the number of inputes when i use
                for j in taxis:
                    input_data.append(j.current_node.longitude)
                    input_data.append(j.current_node.latitude) 
                
                nodes_list = taxi.current_node.connected_nodes

                if len(nodes_list) <= 5:
                    for j in range(len(nodes_list)):
                        input_data.append(nodes_list[j].longitude)
                        input_data.append(nodes_list[j].latitude)
                    for j in range(5 - len(nodes_list)):
                        input_data.append(0)
                        input_data.append(0)
                else:
                    for j in range(5):
                        input_data.append(nodes_list[j].longitude)
                        input_data.append(nodes_list[j].latitude)

                #make a predition on were to go
                input_data.append(time)
                normalized_arr = normalize([input_data])
                print(normalized_arr)
                perdicted_node = argmax(taxi.ANN.predict(normalized_arr))
                

                #update the total travel time and current node
                if perdicted_node <= len(nodes_list) and perdicted_node != 0:
                    taxi.total_travel_time += taxi.current_node.travel_times[perdicted_node - 1]
                    #print(nodes_list[perdicted_node - 1])
                    taxi.current_node = nodes_list[perdicted_node - 1] 
                    taxi.passed_nodes.append(nodes_list[perdicted_node - 1].node_id)
                else:
                    #print(nodes_list[0])
                    taxi.total_travel_time += taxi.current_node.travel_times[0]
                    taxi.current_node = nodes_list[0]
                    taxi.passed_nodes.append(nodes_list[0].node_id)

                #if the node has a passenger the taxi will pickthem up and teleport to the destination
                for node in graph:
                    if node.node_id == taxi.current_node:
                        taxi.pickup_passenger(node)     

                #wait the duration of the ride before being active again
            else:
                if taxi.passenger.dropoff_time < time :
                    taxi.is_full = False

        #add 5 minuts to the time
        print(time)
        time += 5

    for taxi in taxis:
        # Propagate to calculate fitness score
        taxi.fitness = taxi.passenger_tavel_time
        # Add to pool after calculating fitness
        pool.append(taxi)

    # Clear for propagation of next children
    taxis.clear()

    # Sort anns by fitness
    pool = sorted(pool, key=lambda x: x.fitness)
    pool.reverse()

    # Track Max Fitness
    max_fitness = 0
    best = pool[0]
    #save the information to be graphed later of the best taxi
    savetxt("passed_nodes_of_best_taxi_epoch"+str(i)+".csv", 
           best.passed_nodes,
           delimiter =", ", 
           fmt ='% s')

    rows.append([str(i), str(best.total_travel_time), str(best.passenger_tavel_time), str(best.number_of_rides)])
    
    #save the model maybe i will use it in the future
    best.ANN.save_weights('best_taxi_brain'+str(i)+'.h5')

    # Find Max Fitness and Log Associated Weights
    for i in range(len(pool)):
        if pool[i].fitness > max_fitness:
            max_fitness = pool[i].fitness
            best = pool[i]
            logging.debug("Max Fitness: " + str(max_fitness) + "\r\n")

    # Iterate through layers, get weights, and append to optimal
    optimal_weights = []
    for layer in best.ANN.layers:
        optimal_weights.append(layer.get_weights()[0])
    logging.debug('optimal_weights: ' + str(optimal_weights)+"\r\n")

    # Crossover: top 2 randomly select 2 partners and keep the best
    taxis.append(pool[0])
    for i in range(2):
        for j in range(2):
            # Create a child and add to taxis
            childANN = crossover(pool[i], choice(pool))
            child = Taxi()
            child.ANN = childANN
            # Add to taxis to calculate fitness score next iteration
            taxis.append(child)

    for taxi in taxis:
        taxi.current_node = graph[randint(0, 211)]

with open('information to be graphed', 'w') as f:
    # using csv.writer method from CSV package
    write = writer(f)
    fields = ['epoch', 'total_travel_time', 'passenger_tavel_time', 'number_of_rides']
    write.writerow(fields)
    write.writerows(rows)
    f.close()
# Create a Genetic Neural Network with optimal initial weights
#ann = ANN(optimal_weights)