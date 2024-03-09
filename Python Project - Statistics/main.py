import csv
import math
import random
import sys
import os


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arviz as az


def generate_random_data():
    ages = range(18, 70)
    genders = ['M', 'F']
    nationalities = ['Romana', 'Engleza', 'Germana', 'Franceza', 'Italiana', 'Spaniola', 'Americana', 'Chineza']

    return {
        'varsta': random.choice(ages),
        'sex': random.choice(genders),
        'IQ': random.randint(80, 150),
        'nationalitate': random.choice(nationalities)
    }


file_path = ""

try:
    assert len(sys.argv) == 2, "You should introduce one argument: a path to a csv file"
    file_path = sys.argv[1]
except Exception as e:
    print(e)
    exit(1)

try:
    assert os.path.exists(file_path) and os.path.isfile(file_path), "There is no file with path: " + file_path
except Exception as e:
    print(e)
    exit(1)


class Solver:

    def __init__(self):
        self.file_path = file_path
        self.varsta_col = 'varsta'
        self.iq_col = 'IQ'

    def populate_csv(self):
        with open(self.file_path, mode='w') as f:
            writer = csv.DictWriter(f, ['varsta', 'sex', 'IQ', 'nationalitate'])
            writer.writeheader()
            for _ in range(1000):
                random_dict = generate_random_data()
                writer.writerow(random_dict)

    def get_column_values(self, col):
        data = pd.read_csv(self.file_path)
        data = data[col].values
        return data

    def calculate_mean(self, data_set):
        suma = 0
        for value in data_set:
            suma += value
        return suma / len(data_set)

    def calculate_max(self, data_set):
        max_value = data_set[0]
        for value in data_set:
            if max_value < value:
                max_value = value
        return max_value

    def calculate_min(self, data_set):
        min_value = data_set[0]
        for value in data_set:
            if min_value > value:
                min_value = value
        return min_value

    def calculate_median(self, data_set):
        sorted_values = sorted(data_set)
        if len(sorted_values) % 2 == 1:
            median_value = sorted_values[(len(sorted_values) - 1) // 2] / 1
        else:
            median_value = (sorted_values[len(sorted_values) // 2] + sorted_values[len(sorted_values) // 2 - 1]) / 2
        return median_value

    def calculate_standard_deviation(self, data_set):
        suma = 0
        mean = self.calculate_mean(data_set)
        for value in data_set:
            suma += (value - mean) ** 2
        standard_dev = math.sqrt(suma / len(data_set))
        return standard_dev

    def calculate_quartiles(self, data_set):
        second_quartile = self.calculate_median(data_set)
        if len(data_set) % 2 == 1:
            first_quartile = self.calculate_median(data_set[:((len(data_set) - 1) // 2)])
            third_quartile = self.calculate_median(data_set[((len(data_set) - 1) // 2):])
        else:
            first_quartile = self.calculate_median(data_set[:(len(data_set) // 2)])
            third_quartile = self.calculate_median(data_set[((len(data_set) // 2) - 1):])
        quartiles = [first_quartile, second_quartile, third_quartile]
        return quartiles

    def calculate_covariance(self, data_set_1, data_set_2):
        suma = 0
        mean_1 = self.calculate_mean(data_set_1)
        mean_2 = self.calculate_mean(data_set_2)
        for i in range(len(data_set_1)):
            suma += (data_set_1[i] - mean_1) * (data_set_2[i] - mean_2)
        return suma / len(data_set_1)

    def calculate_correlation_coeff(self, data_set_1, data_set_2):
        suma_1 = 0
        suma_2 = 0
        suma_3 = 0
        mean_1 = self.calculate_mean(data_set_1)
        mean_2 = self.calculate_mean(data_set_2)
        for i in range(len(data_set_1)):
            suma_1 += (data_set_1[i] - mean_1) * (data_set_2[i] - mean_2)
            suma_2 += (data_set_1[i] - mean_1) ** 2
            suma_3 += (data_set_2[i] - mean_2) ** 2

        return suma_1 / (math.sqrt(suma_2) * math.sqrt(suma_3))

    def plot_relationship(self):
        data_set_1 = self.get_column_values(self.varsta_col)
        data_set_2 = self.get_column_values(self.iq_col)
        plt.figure(figsize=(8, 6))

        covariance = self.calculate_covariance(data_set_1, data_set_2)
        correlation = self.calculate_correlation_coeff(data_set_1, data_set_2)

        plt.scatter(len(data_set_1) + 2, covariance, color='red', label= f'Covariance Varsta-IQ = {covariance:.5f}')
        plt.scatter(len(data_set_2) + 2, correlation, color='blue', label=f'Correlation Varsta-IQ = {correlation:.5f}')

        plt.plot(data_set_1, label='Varsta')
        plt.plot(data_set_2, label='IQ')

        plt.title('Evoluția Varstei și IQ')
        plt.xlabel('Linie din CSV')
        plt.ylabel('Valoare')
        plt.legend()
        plt.grid(True)
        plt.show()

    def make_calculus(self):
        print("Column: " + self.varsta_col)
        varsta_data_set = self.get_column_values(self.varsta_col)
        iq_data_set = self.get_column_values(self.iq_col)
        print("Mean: " + str(self.calculate_mean(varsta_data_set)))
        print("Median: " + str(self.calculate_median(varsta_data_set)))
        print("Max: " + str(self.calculate_max(varsta_data_set)))
        print("Min: " + str(self.calculate_min(varsta_data_set)))
        print("Standard Deviation: " + str(self.calculate_standard_deviation(varsta_data_set)))
        print("Quartiles: " + str(self.calculate_quartiles(varsta_data_set)))
        print("Relationship between varsta-iq")
        print("Covariance varsta-iq: " + str(self.calculate_covariance(varsta_data_set, iq_data_set)))
        print("Correlation coefficient varsta-iq: " + str(self.calculate_correlation_coeff(varsta_data_set, iq_data_set)))


def main():
    solver = Solver()
    solver.populate_csv()
    solver.make_calculus()
    solver.plot_relationship()


if __name__ == "__main__":
    main()
