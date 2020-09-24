import json
from algorithms import sklearnAlg, id3Alg


def validade_decision_tree(decision_tree, truth_table, truth_table_response):
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
                done = True
            if dt['isLeaf']:
                if dt['response'] == truth_table_response[index]:
                    success = True
                    done = True
                else:
                    sucess = False
                    done = True
        print('{} = {}? {}'.format(row, truth_table_response[index], 'OK!' if success else 'WRONG!'))


if __name__ == "__main__":
    data_set = [
        [1, 1, 1, 0, 4],
        [0, 1, 0, 0, 3],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 3],
        [0, 0, 1, 0, 2],
        [1, 0, 0, 1, 2],
        [0, 1, 0, 1, 4],
        [0, 0, 1, 0, 2],
        [0, 0, 0, 1, 2]
    ]

    truth_table = []
    responses = []
    for row in data_set:
        truth_table.append(row[:-1])
        responses.append(row[-1])

    # Sklearning decision tree validation (gini)
    sklearnAlg.execute(data_set)
    with open('decision_tree.json', 'r') as f:
        decision_tree = json.load(f)
    validade_decision_tree(
        decision_tree,
        truth_table,
        responses
    )

    print('\n')

    # # Entropy algorithm
    # id3Alg.execute(data_set)
    # with open('decision_tree.json', 'r') as f:
    #     decision_tree = json.load(f)
    # validade_decision_tree(
    #     decision_tree,
    #     truth_table,
    #     responses
    # )
