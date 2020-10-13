from sklearn import tree
import numpy as np
from sklearn.tree import _tree
import json

def export_to_json(decision_tree, out_data={}, feature_names=None, target_values=None):
    unique_target_values = list(set(target_values))

    def arr_to_py(arr):
        arr = arr.ravel()
        wrapper = float
        if np.issubdtype(arr.dtype, np.int):
            wrapper = int
        return list(map(wrapper, arr.tolist()))

    def node_to_dict(tree, node_id, unique_target_values):
        if tree.children_left[node_id] != _tree.TREE_LEAF:
            feature = tree.feature[node_id]
            print(tree)
            node_repr =  {
                "node": int(feature),
                "operation": "eolt",
                "value": (tree.threshold[node_id]),
                "isLeaf": False
            }
        else:
            values_x = arr_to_py(tree.value[node_id])
            target_index = values_x.index(max(list(values_x)))
            node_repr = {
                "response": unique_target_values[target_index],
                "isLeaf": True
            }
        return node_repr

    def recurse(tree, node_id, parent=None, unique_target_values=None):
        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id {}".format(_tree.TREE_LEAF))

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        out_data = node_to_dict(
            tree=tree,
            node_id=node_id,
            unique_target_values=unique_target_values
        )

        if left_child != _tree.TREE_LEAF:
            out_data["children"] = []
            out_data["children"].append(
                recurse(
                    tree=tree,
                    node_id=right_child,
                    parent=node_id, 
                    unique_target_values=unique_target_values
                )
            )
            out_data["children"].append(
                recurse(
                    tree=tree,
                    node_id=left_child,
                    parent=node_id,
                    unique_target_values=unique_target_values
                )
            )
        return out_data

    if isinstance(decision_tree, _tree.Tree):
        out_data = recurse(
            tree=decision_tree,
            node_id=0,
            unique_target_values=unique_target_values
        )
    else:
        out_data = recurse(
            tree=decision_tree.tree_,
            node_id=0,
            unique_target_values=unique_target_values
        )

    return out_data


def execute(dataset):
    data = []
    target = []
    for row in dataset:
        data.append(row[:-1])
        target.append(row[-1])

    clf = tree.DecisionTreeClassifier()
    decision_tree = clf.fit(data, target)

    with open("decision_tree.json", "w") as f:
        data = export_to_json(decision_tree=decision_tree, target_values=target)
        f.write(json.dumps(data))