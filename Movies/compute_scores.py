import argparse
import json
import numpy as np


def euclidean_score(dataset, user1, user2):
    '''
    Compute the Euclidean distance score between user1 and user2

    :param dataset: data to calculate on
    :param user1: user to calculate scores for
    :param user2: other users from the dataset
    :return: Euclidean scores
    '''
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        # print(dataset[user1])
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))