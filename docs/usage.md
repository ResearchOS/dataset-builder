# Usage

This package is not really intended for use as a command line package, as it serves primarily to prepare a dataset for use by other packages. The below Python commands are the intended way to interact with this package.

## Build a Dataset
```python
from dataset_builder import Dataset

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)
```

## Data Object Ancestry
To print the ancestry of each data object in the dataset.
```python
from dataset_builder import Dataset

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)

for data_object in dataset.data_objects:
    print(dataset.get_ancestry(data_object))
```

## Get Data Object from Ancestry
To get a data object from its ancestry.
```python
from dataset_builder import Dataset

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)

ancestry_dict = {
    "Subject": "subject1",
    "Trial": "trial1",
}
data_object = dataset.get_data_object(ancestry_dict)
```

## Resolve Data Object File Path
To print the resolved (actual) file path of each data object in the dataset.
```python
from dataset_builder import Dataset

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)

for data_object in dataset.data_objects:
    print(dataset.resolve_file_path(data_object))
```

## DiGraph to Nested Dict
```python
from dataset_builder import Dataset, convert_digraph_to_dict

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)

dag_dict = dataset.convert_digraph_to_dict()
```

## Nested Dict to DiGraph
```python
from dataset_builder import Dataset, convert_dict_to_digraph

dataset_config_path = "path/to/dataset.toml"
dataset = Dataset.build(dataset_config_path)

dag_dict = dataset.convert_digraph_to_dict()
dag = dataset.convert_dict_to_digraph(dag_dict)
```