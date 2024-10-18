# Dataset Structure

After building the dataset, there are various data structures encapsulated within the dataset object. The following sections describe the structure of the dataset object and its components.

## Data Objects
Every entity in a dataset that data can be assigned to is called a Data Object. Each Dataset consists of one or more levels of Data Objects, structured hierarchically. 

!!!tip
    Data Objects are analagous to the concept of "statistical factors" in the design of experiments.

The Data Object names can be any string, and this flexibility allows this package to work with datasets containing any kind of data.

Here's a couple of examples of the [data_object_hierarchy](attributes.md#data_objects_hierarchy) attribute for a couple example Datasets with different kinds of Data Objects. Recall that the format of the `data_objects_hierarchy` attribute is an ordered list of key-value pairs. The keys are the name of a column in the [data_objects_table](attributes.md/#data_objects_table_path), and the value is the name of the Data Object level in that column.

### Data Objects Example 1
A marine biologist is taking measurements of various fish species in different locations. The Data Objects in this case could be structured as follows:
```toml
data_objects_hierarchy = [
    { "Location (lat., long.)" = "Location" },
    { "Fish type (Latin name)" = "Species" },    
]
```
!!!info
    Note that the column names can be any string. Optionally, they can contain additional helpful information like the units of the data to describe what the Data Object represents.
```text
| Location (lat., long.) | Species (Latin name) |
| ---------------------- | -------------------  |
|       Location1        |       Species1       |
|       Location1        |       Species2       |
|       Location2        |       Species1       |
|       Location2        |       Species2       |
```
!!!warning
    Note that in the data objects table, there are **NO** measurements. This table only contains the names of the Data Objects. The actual measurements are stored in the data files.

### Data Objects Example 2
A biomechanist is measuring how high people can jump under different conditions. The Data Objects in this case could be structured as follows:
```toml
data_objects_hierarchy = [    
    { "Subject ID" = "Subject" },
    { "Condition" = "Condition" },
    { "Trial Name" = "Trial" },
]
```

## Data Object Trees
The Data Objects in a dataset are structured hierarchically. This hierarchy is represented as a tree (NetworkX MultiDiGraph). The tree is built from the [data_objects_hierarchy](attributes.md#data_objects_hierarchy) and the [data_objects_table](attributes.md#data_objects_table_path) attributes. The tree is used to navigate the dataset and access the data files.

There are two types of Data Object trees:

### Minimal Data Object Tree
```python
dataset.dataset_tree
```
The minimal Data Object tree is the smallest tree that can be built from the data_objects_hierarchy by minimizing the number of nodes. It's built by connecting the Data Objects in the data_objects_hierarchy in the order they are listed. Using the first Data Object example above, the tree would contain a total of four nodes, two Locations and two Species. The tree would look like this:

![Minimal Data Object Tree](images/minimal_tree_example.png)

This tree is meant to be more visually understandable as the number of Data Objects grows, as there will not be any redundancy in the number of nodes. 

### Expanded Data Object Tree
```python
dataset.expanded_dataset_tree
```
The minimal tree also provides the template to create the expanded tree. The expanded tree contains unique nodes for each unique Data Object ancestry. This allows the Data Object nodes to be iterated over, to process every Data Object in a data processing pipeline.

For example, the expanded tree for the first Data Object example would look like this:

![Expanded Data Object Tree](images/expanded_tree_example.png)

This tree is used to iterate over every unique Data Object ancestry in the dataset.