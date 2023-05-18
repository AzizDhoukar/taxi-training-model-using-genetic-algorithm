import random
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import Constant

class ANN(Sequential):
    
    def __init__(self, child_weights=None):
        super().__init__()

        number_of_inputs = 21
        if child_weights is None:
            layer1 = Dense(15, input_shape=(number_of_inputs,), activation='sigmoid')
            layer2 = Dense(15, activation='sigmoid')
            layer3 = Dense(5, activation='sigmoid')
            self.add(layer1)
            self.add(layer2)
            self.add(layer3)
        else:
            self.add(Dense(3, activation='sigmoid',
                kernel_initializer=Constant(value=child_weights), input_shape=(number_of_inputs,)))
            """self.add(
                Dense(
                    15,
                    input_shape=(number_of_inputs,),
                    activation='sigmoid',
                    weights=[child_weights[0], np.ones(number_of_inputs)])
                )"""
            self.add(
                Dense(
                    15,
                    activation='sigmoid',
                    weights=[child_weights[1], np.zeros(number_of_inputs)])
            )
            self.add(
                Dense(
                    5,
                    activation='sigmoid',
                    weights=[child_weights[2], np.zeros(5)])
            )

def crossover(nn1, nn2,):
    
    nn1_weights = []
    nn1_biases = []
    nn2_weights = []
    nn2_biases = []
    child_weights = []
    child_biases = []

    for layer in nn1.ANN.layers:
        nn1_weights.append(layer.get_weights()[0])
        nn1_biases.append(layer.get_weights()[1])
    for layer in nn2.ANN.layers:
        nn2_weights.append(layer.get_weights()[0])
        nn2_biases.append(layer.get_weights()[1])
        
    for i in range(len(nn1_weights)):
        # Get single point to split the matrix in parents based on # of cols
        split = random.randint(0, np.shape(nn1_weights[i])[1]-1)
        # Iterate through after a single point and set the remaing cols to nn_2
        for j in range(split, np.shape(nn1_weights[i])[1]-1):
            nn1_weights[i][:, j] = nn2_weights[i][:, j]

        child_weights.append(nn1_weights[i])
        child_biases.append(nn1_biases[i])

    mutation(child_weights)
    mutation(child_biases)

    #print(child_weights)
    child = ANN()

    # Set the weights of the new model's layers to the corresponding weights in the array
    child.layers[0].set_weights([child_weights[0], child_biases[0]])
    child.layers[1].set_weights([child_weights[1], child_biases[1]])
    child.layers[2].set_weights([child_weights[2], child_biases[2]])
    
    return child

def mutation(child_weights):
    selection = random.randint(0, len(child_weights)-1)
    mut = random.uniform(0, 1)
    if mut <= .025:
        child_weights[selection] *= random.randint(2, 5)
    elif mut <= .05:
        child_weights[selection] /= random.randint(2, 5)
    else:
        pass

