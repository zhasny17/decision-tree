from sklearn import tree
import numpy as np
from sklearn.tree import _tree

def export_to_json(decision_tree, out_file=None, feature_names=None, target_values=None):
    unique_target_values = list(set(target_values))

    def arr_to_py(arr):
        arr = arr.ravel()
        wrapper = float
        if np.issubdtype(arr.dtype, np.int):
            wrapper = int
        return list(map(wrapper, arr.tolist()))

    def node_to_str(tree, node_id, unique_target_values):
        if tree.children_left[node_id] != _tree.TREE_LEAF:
            feature = tree.feature[node_id]
            label = '"node": {}, "operation": "eolt", "value": {}'.format(feature, tree.threshold[node_id])
            node_type = '"isLeaf": false'
            node_repr = ", ".join((label, node_type))
        else:
            values_x = arr_to_py(tree.value[node_id])
            target_index = values_x.index(max(list(values_x)))
            node_repr = '"response": {}'.format(
                unique_target_values[target_index]
            )
            node_type = '"isLeaf": true'
            node_repr = ", ".join((node_repr, node_type))
        return node_repr

    def recurse(tree, node_id, parent=None, unique_target_values=None):
        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id {}".format(_tree.TREE_LEAF))

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        out_file.write('{' + '{}'.format(node_to_str(tree, node_id, unique_target_values=unique_target_values)))

        if left_child != _tree.TREE_LEAF:
            out_file.write(', "children": [')
            recurse(tree, right_child, node_id, unique_target_values=unique_target_values)
            out_file.write(', ')
            recurse(tree, left_child, node_id, unique_target_values=unique_target_values)
            out_file.write(']')

        out_file.write('}')

    if isinstance(decision_tree, _tree.Tree):
        recurse(decision_tree, 0, unique_target_values=unique_target_values)
    else:
        recurse(decision_tree.tree_, 0, unique_target_values=unique_target_values)

    return out_file


def execute(dataset):
    data = []
    target = []
    for row in dataset:
        data.append(row[:-1])
        target.append(row[-1])

    clf = tree.DecisionTreeClassifier()
    decision_tree = clf.fit(data, target)

    with open('decision_tree.json', 'w') as f:
        export_to_json(decision_tree, f, target_values=target)