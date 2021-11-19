'''
Problem:
    We want to build a system to pick the best (or worst) movies for the person provided.
    The algorithm makes its decision based on Euclidian scoring and users opinions.

    To run the code you have to specific an user, e.g:
    python3 main.py --user "Adam Tomporowski"


Author:
    Adam Tomporowski, s16740
    Piotr Baczkowski, s16621
'''

# To run this script you just have to import below modules
import argparse, json
import numpy as np
from operator import itemgetter
# This script uses Euclidean distance algorithm to calculate the best bets
# You can learn more here https://en.wikipedia.org/wiki/Euclidean_distance
from compute_scores import euclidean_score


def build_arg_parser():
    '''
    The argparse module makes it easy to write user-friendly command-line interfaces

    :return: a command with parameter
    '''
    parser = argparse.ArgumentParser(description='Find users who are similar to the input user')
    parser.add_argument('--user', dest='user', required=True,
                        help='Input user')
    return parser


# Finds users in the dataset that are similar to the input user
def find_similar_users(dataset, user, num_users):
    '''
    Finds users with similar scores

    :param dataset: tells the function which json file to read
    :param user: Name of the user to find best/worst bets
    :param num_users: Specifics the number of users to get recommendations from. Notice they are picked from the best
    matching to worst
    :return: Return users with matching score
    '''
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user
    # and all the users in the dataset
    scores = np.array([[x, euclidean_score(dataset, user,
                                           x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted = np.argsort(scores[:, 1])[::-1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted[:num_users]

    return scores[top_users]


if __name__ == '__main__':
    # Parsed args
    args = build_arg_parser().parse_args()
    # Assigns arg to user variable
    user = args.user
    # Name of the dataset file
    ratings_file = 'ratings.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    # print('\nUsers similar to ' + user + ':\n')
    similar_users = find_similar_users(data, user, 6)
    # print(similar_users)
    # print('User\t\t\tSimilarity score')
    # print('-' * 41)
    # for item in similar_users:
    #   print(item[0], '\t\t', round(float(item[1]), 2))

# This list stores names of users with most similar taste, without scoring
guys = []
# Dict to save recommendations
best_bets = {}
# This for separates names and scores
for item in similar_users:
    guys.append(item[0])

# print("List of users with similar taste: ")
# print(guys)

# Assigns all movies watched by guys[] with scores
for item in guys:
    best_bets.update(data[item])

# Dict of films already watched by the user
already_watched = {}

# Assigns titles to the above dict
for key in data:
    if key == user:
        already_watched.update(data[user])

# Assign all the films from best matching users
movies_to_watch = []
movies_to_watch_merged = {}
for item in data:
    for guy in guys:
        if item == guy:
            movies_to_watch.append(data[item])

# Removes duplicates
for i in movies_to_watch:
    movies_to_watch_merged = {key: i.get(key, 0) + movies_to_watch_merged.get(key, 0)
                              for key in set(i) | set(movies_to_watch_merged)}

# Sorts by a key value
movies_to_watch_merged = (sorted(movies_to_watch_merged.items(), key=itemgetter(1), reverse=True))

# Removes already watched films from the final list
for i in movies_to_watch_merged:
    for y in already_watched:
        if i[0] == y:
            movies_to_watch_merged.remove(i)

print("Top 5 movies recommended for you based on others opinion: ")
print(movies_to_watch_merged[:5])
print("Worst 5 movies for you:")
print(movies_to_watch_merged[-5:])