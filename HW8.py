# Your name: Selena Wang
# Your student id: 27901898
# Your email: selenaw@umich.edu
# List who you have worked with on this homework: N/A

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    {'M-36 Coffee Roasters Cafe': {'category': 'Cafe', 'building': 1101, 'rating': 3.8}, . . . }
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db)
    cur = conn.cursor()

    d = {}

    cur.execute('SELECT name, rating FROM restaurants')
    for c in cur:
        d[c[0]] = {}
        d[c[0]]['rating'] = c[1]

    cur.execute('SELECT categories.category, restaurants.name FROM categories JOIN restaurants ON restaurants.category_id = categories.id')
    for c in cur:
        d[c[1]]['category'] = c[0]

    cur.execute('SELECT restaurants.name, buildings.building FROM buildings JOIN restaurants ON restaurants.building_id = buildings.id')
    for c in cur:
        d[c[0]]['building'] = c[1]

    return d




def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db)
    cur = conn.cursor()

    d = {}

    cur.execute('SELECT category FROM categories')
    for c in cur:
        d[c[0]] = 0

    cur.execute('SELECT categories.category FROM categories JOIN restaurants ON categories.id = restaurants.category_id')
    for c in cur:
        d[c[0]] += 1

    l = list(sorted(d.items(), key = lambda t: t[1]))
    x = []
    y = []
    
    for item in l:
        x.append(item[0])
        y.append(int(item[1]))

    fig, ax = plt.subplots(figsize =(20, 8)) # the disproportionate ratio is the only way I can make the types and the ylabel show ;-;

    ax.barh(x, y)
    ax.set_title('# of South Ave Restaurant Types')
    plt.xlabel("# of Type")
    plt.ylabel("Restaurant Categories")
    tickpos = [0,1,2,3,4]
    plt.xticks(tickpos,tickpos)
    plt.savefig("bargraph.png")
    plt.show()

    return d

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db)
    cur = conn.cursor()

    l = []
    d = {}
    cmd = 'SELECT restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = '

    cur.execute(cmd + str(building_num))

    for c in cur:
        d[c[0]] = float(c[1])
    
    sort = list(sorted(d.items(), key = lambda t: t[1], reverse= True))
    for s in sort:
        l.append(s[0])

    return l
    

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db)
    cur = conn.cursor()
    
    cate_d = {}
    build_d = {}

    cur.execute('SELECT category FROM categories')
    for c in cur:
        cate_d[c[0]] = 0

    for ca in cate_d.items():
        cate = ca[0]
        cur.execute(f"SELECT AVG(restaurants.rating) FROM categories JOIN restaurants ON restaurants.category_id = categories.id WHERE categories.category = '{cate}'")
        for c in cur:
            cate_d[cate] =float("{:.1f}".format(c[0]))
    cate_l = list(sorted(cate_d.items(), key = lambda t: t[1]))

    cur.execute('SELECT building FROM buildings')
    for c in cur:
        build_d[c[0]] = 0

    for b in build_d.items():
        build = b[0]
        cur.execute(f"SELECT AVG(restaurants.rating) FROM buildings JOIN restaurants ON restaurants.building_id = buildings.id WHERE buildings.building = '{build}'")
        for c in cur:
            build_d[build] =float("{:.1f}".format(c[0]))
    build_l = list(sorted(build_d.items(), key = lambda t: t[1]))

    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for l in cate_l:
        y1.append(l[1])
        x1.append(l[0])
    for b in build_l:
        y2.append(b[1])
        x2.append(str(b[0]))

    fig = plt.figure(figsize=(20,10))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.barh(x1, y1)
    ax2.barh(x2, y2)
    ax1.set_xlim([0,5])
    ax2.set_xlim([0,5])
    ax1.set_title('Average Restaurant Ratings by Category')
    ax1.set_xlabel('Average Rating')
    ax2.set_xlabel('Average Rating')
    ax1.set_ylabel('Categories')
    ax2.set_ylabel('Buildings')
    ax2.set_title('Average Restaurant Ratings by Building')
    plt.savefig("xcredit.png")
    plt.show()

    return [cate_l[len(cate_l) - 1], build_l[len(build_l) - 1]]


#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
