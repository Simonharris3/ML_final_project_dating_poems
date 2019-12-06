import math
import csv
import random

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

PERCENT_TRAIN = .8
HIDDEN_SIZE = 20

def main():
    file = "poem_attributes.csv"
    random_seed = 349

    instances, possible_labels = readFromCsv(file)
    instances_cleaned, labels = separate_labels(instances)

    print(instances_cleaned)
    # for instance in instances_cleaned:
       # for attribute in instance:
            # if type(attribute) != float and type(attribute) != int:
              #  print("Not a float: " + str(attribute))

    # preprocessing for neural nets (scale the data)
    scaler = StandardScaler()
    scaler.fit(instances_cleaned)
    nn_instances_cleaned = scaler.transform(instances_cleaned)

    # divide the data into training and test sets based on the given parameters
    nn_training, nn_test = split_set(random_seed, nn_instances_cleaned)

    training_labels, test_labels = split_set(random_seed, labels)

    network = train_neural_net(nn_training, training_labels)

    nn_predictions = network.predict(nn_test)

    confusion_matrix_nn = []

    index = 0
    for l1 in possible_labels:
        confusion_matrix_nn.append([])

        for l2 in possible_labels:
            confusion_matrix_nn[index].append(0)
        index += 1

    num_correct_nn = 0
    for i in range(len(nn_test)):
        nn_actual = test_labels[i]

        predicted_index_nn = possible_labels.index(nn_predictions[i])
        actual_index_nn = possible_labels.index(nn_actual)

        confusion_matrix_nn[actual_index_nn][predicted_index_nn] += 1

        if nn_actual == nn_predictions[i]:
            num_correct_nn += 1

    print("Neural net accuracy: " + str(num_correct_nn / len(nn_test)))
    #
    # writeToCsv(random_seed, confusion_matrix_nn, possible_labels, file, "nn")
    #
    # nn_recalls = calculateRecall(confusion_matrix_nn, possible_labels)
    #
    # writeRecall(file, nn_recalls, possible_labels, "nn")

# open csv file and retrieve the data
def readFromCsv(filename):
    possible_labels = []

    with open(filename) as file:
        instances = []
        reader = csv.reader(file, delimiter=",")
        c = 0
        for row in reader:  # read in the instance in each row
            if c != 0:  # skip the first line
                instance = []
                a = 0
                for attribute in row:
                    if a == 0:
                        instance.append(attribute)  # don't cast label as an int, but store it as instance[0]
                        if attribute not in possible_labels:
                            possible_labels.append(attribute)
                    else:
                        try:
                            instance.append(float(attribute))  # cast the continuous attributes as ints
                        except ValueError:
                            instance.append(attribute)
                    a += 1
                instances.append(instance)
            c += 1

    return instances, possible_labels

def separate_labels(instances_with_labels):
    instances = []
    labels = []
    for instance in instances_with_labels:
        instances.append(instance[1:])
        labels.append(instance[0])
    return instances, labels

def split_set(random_seed, instances):
    random.seed(random_seed)
    shuffled = list(instances)
    random.shuffle(shuffled)
    training_cutoff = int(len(shuffled) * PERCENT_TRAIN)

    # Make training and test sets
    training_set = shuffled[:training_cutoff]
    test_set = shuffled[training_cutoff:]

    return training_set, test_set

def train_neural_net(training_set, labels):
    mlp = MLPClassifier(hidden_layer_sizes=HIDDEN_SIZE, max_iter=20000)
    mlp.fit(training_set, labels)
    return mlp


main()
