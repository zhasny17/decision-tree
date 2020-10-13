
from pprint import pprint
import json
from operator import gt
from math import log2
import sys
from functools import wraps


# class TailRecurseException(Exception):
#     def __init__(self, args, kwargs):
#         print('DONE@')
#         super().__init__()
#         self.args = args
#         self.kwargs = kwargs


# def tail_call_optimized(g):
#     @wraps(g)
#     def func(*args, **kwargs):
#         while True:
#             try:
#                 return g(*args, **kwargs)
#             except TailRecurseException as e:
#                 args = e.args
#                 kwargs = e.kwargs
#     return func


def divideset(data, column, value):
    split_function = list(filter(lambda row: row[column] == value, data))
    set1 = [row for row in data if row in split_function]
    set2 = [row for row in data if row not in split_function]
    return (set1, set2)


def uniquecounts(data):
    results = {}
    for row in data:
        r = row[-1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


def entropy(data):
    results = uniquecounts(data)
    ent = 0.0
    for r in results:
        p = float(results[r])/len(data)
        ent -= p*log2(p)
    return ent


class Decisionnode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.node = col
        self.value = value
        self.isLeaf = True if col == -1 else False
        self.results = results
        self.tb = tb
        self.fb = fb

    # @tail_call_optimized
    def exportToJson(self):
        print('building json tree!')
        response = {'isLeaf': self.isLeaf}
        if self.isLeaf:
            response['response'] = list(self.results.keys())[0]
        else:
            response['node'] = self.node
            response['value'] = self.value
            response['operation'] = 'eq'
            response['children'] = [
                self.fb.exportToJson(),
                self.tb.exportToJson()
            ]
        return response

# @tail_call_optimized
def buildtree(data, entropy=entropy):
    print('building tree!')
    if len(data) == 0:
        return decisionnode()

    current_score = entropy(data)

    best_gain = 0
    best_criteria = None
    best_sets = None

    column_count = len(data[0][:-1])
    for col in range(0, column_count):
        column_values = {}
        for row in data:
            column_values[row[col]] = 1
        gain = current_score
        column_info = []
        for value in column_values.keys():
            (set1, set2) = divideset(data, col, value)
            weight = float(len(set1))/len(data)
            gain -= weight*entropy(set1)
            column_info.append(
                {
                    'value': value,
                    'set1': set1,
                    'set2': set2
                }
            )
        for info in column_info:
            if gain >= best_gain and len(info['set1']) > 0 and len(info['set2']) > 0:
                best_gain = gain
                best_criteria = (col, info['value'])
                best_sets = (info['set1'], info['set2'])
                break
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return Decisionnode(
            col=best_criteria[0],
            value=best_criteria[1],
            tb=trueBranch,
            fb=falseBranch
        )
    else:
        return Decisionnode(results=uniquecounts(data))


def execute(dataset):
    tree = buildtree(dataset)
    json_dt = tree.exportToJson()
    return json_dt
