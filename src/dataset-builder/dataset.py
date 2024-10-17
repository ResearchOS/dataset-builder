import os
import csv
from collections import deque

import networkx as nx

from validator import DictValidator
from data_objects import create_data_object_classes
from data_objects import DataObject

class Dataset:

    def __init__(self,
                 data_folder_path: str,
                 data_objects_hierarchy: list,
                 data_objects_file_paths: str,
                 data_objects_table_path: str,
                 num_header_rows: int,
                 other_columns: list,
                 **kwargs):
        input_dict = {
            'data_folder_path': data_folder_path,
            'data_objects_hierarchy': data_objects_hierarchy,
            'data_objects_file_paths': data_objects_file_paths,
            'data_objects_table_path': data_objects_table_path,
            'num_header_rows': num_header_rows,
            'other_columns': other_columns
        }
        input_dict.update(kwargs)
        dict_validator = DictValidator()
        dict_validator.validate(input_dict)
        for attr_name in input_dict:
            setattr(self, attr_name, input_dict[attr_name])    

    @classmethod
    def build_from_dict(cls, config: dict):
        """Build the dataset from the config."""
        dataset = cls(**config)
        if not os.path.exists(dataset.data_objects_table_path):
            raise ValueError('Data folder path does not exist')
        dataset.create_data_objects_tree()

    def create_data_objects_tree(self):
        """Read the data objects table and create a tree of the data objects.
        NOTE: The tree is a NetworkX MultiDiGraph, and each data object instance is a singleton."""
        file_path = self.data_objects_table_path
        # Convert list of dicts to dict
        self.data_objects_hierarchy = {list(d.keys())[0]: list(d.values())[0] for d in self.data_objects_hierarchy}
        data_object_class_names = [v for v in self.data_objects_hierarchy.values()]
        self.data_object_classes = create_data_object_classes(data_object_class_names)
        dataset_tree = nx.MultiDiGraph()
        DataObject.is_singleton = True
        # Read the table
        with open(file_path, 'r') as file:
            # Skip the header rows
            reader = csv.DictReader(file)
            header_row = reader.fieldnames
            if header_row[0].startswith('\ufeff'):
                header_row[0] = header_row[0][1:] 
            
            # Iterate over each row in the CSV
            for count, row in enumerate(reader):
                if count < self.num_header_rows - 1:
                    continue # Skip remaining header rows

                row_data_objects = []
                for column_name, class_name in self.data_objects_hierarchy.items():
                    # Retrieve the class from the data_object_classes dictionary
                    data_class = self.data_object_classes.get(class_name)
                    # Instantiate the class with data from the row and store the instance
                    instance_name = row[column_name]
                    data_object_instance = data_class(instance_name)
                    row_data_objects.append(data_object_instance)
                    dataset_tree.add_node(data_object_instance)

                if len(row_data_objects) > 1:
                    for count, data_object in enumerate(row_data_objects[0:len(row_data_objects)-1]):
                        dataset_tree.add_edge(data_object, row_data_objects[count+1])

        self.dataset_tree = dataset_tree
        graph_dict = self.convert_digraph_to_dict(self.dataset_tree)
        self.expanded_dataset_tree = self.convert_dict_to_digraph(graph_dict, self.data_object_classes)
        self.check_expanded_dataset_tree()
        return

    def convert_digraph_to_dict(self, graph):
        def recurse(node):
            successors = list(graph.successors(node))
            return {successor.instance_name: recurse(successor) for successor in successors}
        
        return {node.instance_name: recurse(node) for node in graph if graph.in_degree(node) == 0}

    def convert_dict_to_digraph(self, graph_dict: dict, data_object_classes: dict):
        """Convert the nested dictionary to a NetworkX MultiDiGraph using breadth-first search (BFS)."""
        dataset_tree = nx.MultiDiGraph()
        DataObject.is_singleton = False

        # Initialize the queue with the root nodes
        queue = deque()
        cls = data_object_classes[list(data_object_classes.keys())[0]]
        
        for node_name, node_dict in graph_dict.items():
            node = cls(node_name)
            dataset_tree.add_node(node)
            queue.append((node, node_dict, 1))  # Add root node to queue along with its dictionary and depth level

        # Perform BFS
        while queue:
            source_node, node_dict, recurse_count = queue.popleft()
            if not node_dict:
                continue

            # Get the class for the next level
            cls = data_object_classes[list(data_object_classes.keys())[recurse_count]]
            
            for child_name, child_dict in node_dict.items():
                child_node = cls(child_name)
                dataset_tree.add_node(child_node)
                dataset_tree.add_edge(source_node, child_node)
                queue.append((child_node, child_dict, recurse_count + 1))

        return dataset_tree
    
    def check_expanded_dataset_tree(self):
        """Confirm that the expanded dataset tree is valid."""
        # Check that all nodes have <= 1 parent
        for node in self.expanded_dataset_tree:
            if self.expanded_dataset_tree.in_degree(node) > 1:
                raise ValueError('Data object instance has more than one parent')
        # Check that nodes' predecessors are the proper type
        data_object_classes_keys = list(self.data_object_classes.keys())
        for node in self.expanded_dataset_tree:
            node_index = data_object_classes_keys.index(node.__class__.__name__)
            predecessors = list(self.expanded_dataset_tree.predecessors(node))
            if not predecessors:
                continue
            parent = predecessors[0]
            if not parent.__class__.__name__ == data_object_classes_keys[node_index - 1]:
                raise ValueError('Data object instance has an incorrect parent')