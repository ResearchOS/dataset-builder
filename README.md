# dataset-builder
Build a Dataset, reading from a provided TOML file. Supported datasets are hierarchically structured data of any kind, with files split across folders. Each data file should represent one Data Object. Currently, multiple data objects per data file is not supported (see the [Roadmap](#roadmap))

This Dataset package supports any type of hierarchically structured data by specifying its metadata. It is the second tool developed for use with the ResearchOS platform (check out the first tool to generate DAG's of a data processing pipeline, [dagpiler](https://github.com/ResearchOS/dagpiler)).

## Useage
### TOML file
```toml
data_folder_path = "path/to/dataset/folder"
data_objects_hierarchy = [
    { "Data_Object_Column_Name1" = "DataObjectName1" },
    { "Data_Object_Column_Name2" = "DataObjectName2" },
]
data_objects_file_paths = "DataObjectName1/DataObjectName2"
data_objects_table_path = "path/to/dataset/table.csv"
num_header_rows = 1
other_columns = [
    { "Other_Column_Name" = "otherVariableName" }
]
```

### Python
The above TOML equates to:
```python
from dataset_builder import Dataset

data_folder_path = "path/to/dataset/folder"
data_objects_hierarchy = [
    { "Data_Object_Column_Name1": "DataObjectName1" },
    { "Data_Object_Column_Name2": "DataObjectName2" }
]
data_objects_file_paths = "DataObjectName1/DataObjectName2"
data_objects_table_path = "path/to/dataset/table.csv"
num_header_rows = 1
other_columns = [
    { "Other_Column_Name": "otherVariableName" }
]
dataset = Dataset(
    data_folder_path = data_folder_path,
    data_objects_hierarchy = data_objects_hierarchy,
    data_objects_file_paths = data_objects_file_paths,
    data_objects_table_path = data_objects_table_path,
    num_header_rows = num_header_rows,
    other_columns = other_columns
)
```

## Roadmap
- Support datasets that have multiple data objects per file (i.e. one or more CSV files)