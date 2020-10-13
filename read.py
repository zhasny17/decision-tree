import json
from algorithms import sklearnAlg, id3Alg


def validate_decision_tree(decision_tree, truth_table, truth_table_response):
    for index, row in enumerate(truth_table):
        node = None
        done = False
        dt = decision_tree
        while not done:
            node = dt['node']
            if dt['operation'] == 'eolt':
                child_index = int((row[node] <= dt['value']))
                dt = dt['children'][child_index]
            elif dt['operation'] == 'eq':
                child_index = int((row[node] == dt['value']))
                dt = dt['children'][child_index]
            else:
                print('invalid operator')
                done = Truekf
            if dt['isLeaf']:
                if dt['response'] == truth_table_response[index]:
                    success = True
                    done = True
                else:
                    sucess = False
                    done = True
        print('{} = {}? {}'.format(row, truth_table_response[index], 'OK!' if success else 'WRONG!'))
