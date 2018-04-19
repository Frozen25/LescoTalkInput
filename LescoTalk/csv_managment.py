import csv
import operator
import math

def string_to_int_array(string_vector):
    int_array = []

    for i in string_vector:
        int_array.append(int(i))

    return int_array

def string_to_float_array(string_vector):
    float_array = []

    for i in string_vector:
        float_array.append(float(i))

    return float_array

def in_product(x, y):
    a = list(map(operator.mul, x, y))
    y = 0
    for i in range(len(a)):
        y += a[i]
    return y

def magnitude(x):
    a = math.sqrt(in_product(x, x))
    return a

def angle(x, y):
    a = in_product(x, y) / (magnitude(x) * (magnitude(y)))
    if 0.992 < a < 1.3:
        return 0
    return math.acos(in_product(x, y) / (magnitude(x) * (magnitude(y))))

def is_equal_vector(vector1, vector2):
    return angle(vector1, vector2) == 0

def comparate_with_database(x_vector, y_vector):
    final_word = ""
    with open('database.csv') as database_file:
        csv_reader = csv.DictReader(database_file)

        for line in csv_reader:
            word_x_vector = string_to_float_array(line['x_position'].split("!"))
            word_y_vector = string_to_float_array(line['y_position'].split("!"))

            if (is_equal_vector(word_x_vector, x_vector) and is_equal_vector(word_y_vector, y_vector)):
                final_word = line['word']
                break
    return final_word

def get_database_vector():
    final_list = []

    with open('database.csv') as database_file:
        csv_reader = csv.DictReader(database_file)

        for line in csv_reader:
            temp_list = []
            word_x_vector = line['x_position'].split("!")
            word_y_vector = line['y_position'].split("!")

            temp_list.append(line['word'])
            temp_list.append(string_to_float_array(word_x_vector))
            temp_list.append(string_to_float_array(word_y_vector))

            final_list.append(temp_list)

    return final_list


#print(comparate_with_database([4.2, 6, 8], [3, 2, 4]))
#print(get_database_vector())










