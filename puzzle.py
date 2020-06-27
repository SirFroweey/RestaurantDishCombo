import itertools
import functools
import argparse
import csv
import os

from collections import namedtuple
from decimal import Decimal


Dish = namedtuple('Dish', ['name', 'price'])


def read_csv(file_name):
    """
    Read a CSV and parse the total and dishes from it.
    :filename (str) -> CSV to read from.
    """
    if not os.stat(file_name).st_size:
        print('Could not parse the CSV. File is empty.')
        return

    total = None
    dishes = []

    def _read_price(row):
        price = None
        try:
            # We utilize Decimal(s) to ensure proper floating point precision
            price = Decimal(row['price'].replace('$', ''))
        except AttributeError:
            print('Could not parse the CSV. Invalid format.')
            return

        return price

    # Read the CSV lines as a dictionary (key, value) pair and create new Dish objects.
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['name', 'price'])

        for row_index, row in enumerate(reader):
            price = _read_price(row)

            if not price:
                return

            if row_index == 0:
                total = price
            else:
                dishes.append(Dish(row['name'], price))

    return {
        'total': total, 
        'dishes': dishes
    }


def find_dish_combination(file_name):
    """
    Find a combination of dishes that amount to the given desired total.
    :filename (str) -> CSV to read from.
    Returns a list of Dish objects or None.
    """
    contents = read_csv(file_name)

    if not contents:
        return
    
    total = contents['total']
    dishes = contents['dishes']
    dish_list_indices = list(range(len(dishes)))

    # Generate all possible combination of dishes and attempt to find a sum equal to
    # the desired total.
    for index in range(len(dishes)):
        for combo in itertools.combinations(dish_list_indices, index):
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
