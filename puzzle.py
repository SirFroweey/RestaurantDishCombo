import itertools
import functools
import argparse
import csv

from collections import namedtuple
from decimal import Decimal


Dish = namedtuple('Dish', ['name', 'price'])


def read_csv(file_name):
    """
    Read a CSV and parse the total and dishes from it.
    :filename (str) -> CSV to read from.
    """
    total = None
    dishes = []

    # Read the CSV lines as a dictionary (key, value) pair and create new Dish objects.
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['name', 'price'])
        for row_index, row in enumerate(reader):
            if row_index == 0:
                total = Decimal(row['price'].replace('$', ''))
            else:
                # We utilize Decimal(s) to ensure proper floating point precision
                dishes.append(Dish(row['name'], Decimal(row['price'].replace('$', ''))))

    return (total, dishes)


def find_dish_combination(file_name):
    """
    Find a combination of dishes that amount to the given desired total.
    :filename (str) -> CSV to read from.
    Returns a list of Dish objects or None.
    """
    total, dishes = read_csv(file_name)
    indices = list(range(len(dishes)))

    # Generate all possible combination of dishes and attempt to find a sum equal to
    # the desired total.
    for index in range(len(dishes)):
        for combo in itertools.combinations(indices, index):
            projected_total = sum([dishes[index].price for index in combo])
            if projected_total == total:
                return [dishes[index] for index in combo]
    
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', dest='file_name', type=str, default='example.csv',
                        help='name of csv to read from (default: example.csv)')
    args = parser.parse_args()

    if args.file_name:
        dishes = find_dish_combination(file_name=args.file_name)
        print(dishes or 'No combination of dishes that is equal to the target price found')
    else:
        print('No file specified')
