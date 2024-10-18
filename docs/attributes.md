# Attributes

To define a dataset, there are several attributes that need to be set in the dataset's configuration file. All attributes are required unless specified otherwise.

## data_folder_path
The absolute path to the folder containing the files in the dataset. This is the `data_folder` folder in the [Folder Structure](example.md) page.
```toml
data_folder_path = "/path/to/data_folder"
```

## data_objects_hierarchy
The hierarchy of the data objects in the dataset. The column names in the data objects are used to define the hierarchy. The hierarchy is a list of dictionaries where the key is the column name and the value is the data object class. The first item is the top level data object, and each successive item is lower in the data object hierarchy.
```toml
data_objects_hierarchy = [
    {column_name1 = "data_object_class1"},
    {column_name2 = "data_object_class2"},
]
```
For the [example dataset](example.md/#example), which consists of Subject data objects that each contain multiple Trial data objects, the hierarchy would be:
```toml
data_objects_hierarchy = [
    { "Subject Name" = "Subject"},
    { "Trial Name" = "Trial"},
]
```
!!!tip
    By convention, the data object class names are capitalized.

## data_objects_file_paths
This defines the relative path to each data objects' data file(s). The path is relative to the `data_folder` folder. 
```toml
data_objects_file_paths = "Subject/Trial"
```
!!!warning
    The data object names in the file path must match the data object names in the [data_objects_hierarchy](#data_objects_hierarchy) exactly.

## data_objects_table_path
The path to the table (csv file) that defines the data objects ([example](example.md/#example-csv-file)). The path can be relative to the `data_folder` folder or an absolute path.

If the file is located at $data_folder/data_objects_table.csv, the path would be:
```toml
data_objects_table_path = "data_objects_table.csv"
```

If the file is located outside of the `$data_folder` folder, the path would be:
```toml
data_objects_table_path = "/path/to/data_objects_table.csv"
```

## num_header_rows
The number of rows in the data objects table that are header rows. These rows are skipped when reading the table. The first row of the table is assumed to always be the header row. If that is your only header row, then you will have:
```toml
num_header_rows = 1
```
If there are additional header rows below the first row, for example the first header row plus two additional rows, then you will need to set this value to the number of header rows.
```text
# /Users/my_username/my_dataset/data_objects_table.csv
| Subject Name | Trial Name |
| header txt1  | header txt1|
| header txt2  | header txt2|
| ------------ | ---------  |
|   Subject1   |   Trial1   |
|   Subject1   |   Trial2   |
|   Subject2   |   Trial1   |
|   Subject2   |   Trial2   |
```
```toml
num_header_rows = 3
```

## (Optional) other_columns
For now, this attribute is not used and can be omitted. Any additional columns in the data objects table that are not part of the data objects hierarchy are ignored.
!!!todo
In the future, this attribute will be used to specify how other columns within the data objects table should be handled. If other columns contain metadata like notes, or actual data, this attribute will include them in the dataset as well.