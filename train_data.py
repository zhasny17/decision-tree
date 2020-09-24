import os
from matplotlib import image
from pprint import pprint
from algorithms import id3Alg, sklearnAlg
from time import time
import numpy
import csv
from datetime import datetime
from read import validate_decision_tree


def generate_dataset_from_csv():
    dataset = []
    with open('Space_Corrected.csv', 'r') as f:
        data = csv.reader(f)
        for row in data:
            # removendo as duas primeiras colunas de dados desnecessarios
            dataset.append(row[2:])
    # removendo a linha de titulos
    del(dataset[0])
    # formatando datas e mantendo apenas o ano, diminuindo as ramificacoes da nossa arvore
    for row in dataset:
        year = 0
        if row[2].endswith('UTC'):
            text = row[2].split(' UTC')[0]
            try:
                date = datetime.strptime(text, '%a %b %d, %Y %H:%M')
                year = date.year
            except Exception:
                print('!!!!ERROR!!!!! ', text)
                year = 0
        elif row[2] is None:
            year = 0
        else:
            try:
                text = row[2].split(', ')[1]
                year = text
            except Exception as err:
                print(row[2])
                year = 0
                print('!!!!!!CONVERSION ERROR!!!!!! ', str(err))
        row[2] = year
    return dataset


if __name__ == "__main__":
    initial_time = time()
    dataset = generate_dataset_from_csv()
    end_time = time()
    print('execution time to generate dataset is: ', end_time-initial_time)
    print('dataset shape: ', len(dataset[0]), 'x', len(dataset))
    initial_time = time()
    json_tree = id3Alg.execute(dataset)
    end_time = time()
    print('execution time to generate decision tree is: ', end_time-initial_time)
    validate_data = [
        [
            'ISA',
            'Imam Khomeini Spaceport, Semnan Space Center, Iran',
            '2019',
            'Safir-1B+ | Nahid-1',
            'StatusActive',
            ''
        ]
    ]
    response = [
        'Prelaunch Failure'
    ]
    validate_decision_tree(json_tree, validate_data, response)
