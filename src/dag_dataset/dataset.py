import os
import csv
from collections import deque

from base_dag import DAG

from .validator import DictValidator
from .data_objects import create_data_object_classes
from .data_objects import DataObject
from .config_reader import CONFIG_READER_FACTORY

class Dataset:

    def __init__(self,
                 data_folder_path: str,
                 data_objects_hierarchy: list,
                 data_objects_file_paths: str,
                 data_objects_table_path: str,
                 num_header_rows: int,
                 other_columns: list = [],
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
    def build(cls, config_path: str) -> 'Dataset':
        """Build the dataset from the config."""
        config_reader = CONFIG_READER_FACTORY.get_config_reader(config_path)
        config = config_reader.read_config()        
        dataset = cls(**config)
        if not os.path.exists(dataset.data_objects_table_path):
            raise ValueError('Data folder path does not exist')
        dataset._create_data_objects_trees()
        return dataset
    
    def resolve_file_path(self, data_object: DataObject = None, ancestry_dict: dict = None) -> str:
        """Return the resolved file path for the given data object instance.
        NOTE: If a dict is provided (with keys as class names and values as data object names), the data object instance is retrieved first."""        
        if not data_object and ancestry_dict is not None:
            data_object = self.get_data_object(ancestry_dict)
        class_names = list(self.data_objects_hierarchy.values())
        file_path = os.path.normpath(self.data_objects_file_paths)
        if os.path.isabs(file_path):
            file_path = file_path[1:] # Handle / at beginning
        if file_path.endswith('/'):
            file_path = file_path[:-1] # Handle / at end
        ancestry = self.get_ancestry(data_object)
        for class_name in class_names:
            ancestor_data_object = [a for a in ancestry if a.__class__.__name__ == class_name]
            if file_path.startswith(class_name):
                file_path = file_path.replace(class_name + '/', ancestor_data_object.instance_name + '/')
            if file_path.endswith(class_name):
                file_path = file_path.replace('/' + class_name, '/' + ancestor_data_object.instance_name)
            else:
                file_path = file_path.replace('/' + class_name + '/', '/' + ancestor_data_object.instance_name + '/')        
        # Return the absolute path
        return os.path.join(self.data_folder_path, file_path) 

    def _create_data_objects_trees(self) -> None:
        """Read the data objects table and create a tree of the data objects.
        NOTE: The tree is a NetworkX MultiDiGraph, and each node is a data object instance."""
        file_path = self.data_objects_table_path
        # Convert list of dicts to dict
        self.data_objects_hierarchy = {list(d.keys())[0]: list(d.values())[0] for d in self.data_objects_hierarchy}
        data_object_class_names = [v for v in self.data_objects_hierarchy.values()]
        self.data_object_classes = create_data_object_classes(data_object_class_names)
        dataset_tree = DAG()
        DataObject.is_singleton = True
        # Read the table
        all_data_object_names = []
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

                all_data_object_names.append([data_object.instance_name for data_object in row_data_objects])

                if len(row_data_objects) > 1:
                    for count, data_object in enumerate(row_data_objects[0:len(row_data_objects)-1]):
                        dataset_tree.add_edge(data_object, row_data_objects[count+1])

        self.all_data_object_names = all_data_object_names # The CSV file as a list of lists.
        self.dataset_tree = dataset_tree
        self._expand_dataset_tree(self.dataset_tree)
        self._check_expanded_dataset_tree()
        return
    
    def _expand_dataset_tree(self, dataset_tree: DAG = None) -> DAG:
        """Expand the dataset tree to include all data object instances."""
        if not dataset_tree:
            dataset_tree = self.dataset_tree
        graph_dict = self.convert_digraph_to_dict()
        self.expanded_dataset_tree = self.convert_dict_to_digraph(graph_dict, self.data_object_classes)
        return self.expanded_dataset_tree

    def convert_digraph_to_dict(self, graph: DAG = None) -> dict:
        """Convert the NetworkX MultiDiGraph to a nested dictionary."""
        if not graph:
            graph = self.dataset_tree
        def recurse(node):
            successors = list(graph.successors(node))
            return {successor.instance_name: recurse(successor) for successor in successors}
        
        return {node.instance_name: recurse(node) for node in graph if graph.in_degree(node) == 0}

    def convert_dict_to_digraph(self, graph_dict: dict = None, data_object_classes: dict = None) -> DAG:
        """Convert the nested dictionary to a NetworkX MultiDiGraph using breadth-first search (BFS)."""
        if not graph_dict:
            graph_dict = self.convert_digraph_to_dict()
        if not data_object_classes:
            data_object_classes = self.data_object_classes

        dataset_tree = DAG()
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
                # Check that this edge exists in the CSV file, and is not an artifact of the over-connected dataset tree
                is_real_edge = False
                ancestors = self.get_ancestry(child_node, expanded_dataset_tree=dataset_tree)
                for row in self.all_data_object_names:
                    if all([ancestor.instance_name in row for ancestor in ancestors]):
                        is_real_edge = True
                        break
                if not is_real_edge:
                    dataset_tree.remove_edge(source_node, child_node)
                    dataset_tree.remove_node(child_node)
                else:
                    queue.append((child_node, child_dict, recurse_count + 1))

        return dataset_tree
    
    def _check_expanded_dataset_tree(self) -> None:
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
            
    def get_ancestry(self, data_object: DataObject, expanded_dataset_tree: DAG = None) -> list:
        """Return the ancestry of the given data object instance. Include the instance itself."""        
        if not expanded_dataset_tree:
            expanded_dataset_tree = self.expanded_dataset_tree
        if len([n for n in expanded_dataset_tree if n == data_object]) == 0:
            raise ValueError('Data object instance not found in the expanded dataset tree')
        ancestor_nodes = list(expanded_dataset_tree.ancestors(data_object))        
        ancestor_nodes.append(data_object)
        # Ensure they're in the same order as the data object classes are specified.
        ancestor_nodes = sorted(ancestor_nodes, key=lambda x: list(self.data_object_classes.keys()).index(x.__class__.__name__))
        return ancestor_nodes
        
    def get_data_object(self, dict_of_strings: dict) -> DataObject:
        """Return the data object instance corresponding to the given dictionary of class names (keys) and data object names (values)."""
        # Check the input dictionary
        ordered_classes = list(self.data_object_classes.keys())        
        for key, value in dict_of_strings.items():
            if key not in ordered_classes:
                raise ValueError('Invalid class name key in dictionary')
        
        # Order the dictionary by class hierarchy, and get the lowest type (the type of the data object we are looking for)
        ordered_dict_of_strings = {key: dict_of_strings[key] for key in ordered_classes if key in dict_of_strings}
        lowest_type = [k for k in ordered_dict_of_strings.keys()][-1]        

        # Find the data object instances with the given name and type
        data_objects_of_type_and_name = [n for n in self.expanded_dataset_tree if n.__class__.__name__ == lowest_type and n.instance_name == dict_of_strings[lowest_type]]
        if not data_objects_of_type_and_name:
            raise ValueError('Data object instance not found')

        # Check the ancestry of each data object instance to see if it matches the input dictionary
        data_object = None
        for current_data_object in data_objects_of_type_and_name:
            ancestry = self.get_ancestry(current_data_object)
            is_match = True
            for key, value in ordered_dict_of_strings.items():
                if not any([ancestor.instance_name == value for ancestor in ancestry if ancestor.__class__.__name__ == key]):
                    is_match = False
                    break

            if is_match:
                data_object = current_data_object                
                break

        if not data_object:
            raise ValueError('Data object instance not found')
        
        return data_object