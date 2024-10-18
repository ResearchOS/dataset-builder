# Minimal Example Project Structure

## Example directory structure
A small dataset consisting of .txt files, where each file contains data for one trial of one subject, could be structured as follows:
```text
/Users/my_username/my_dataset/
├── Subject1/
│   ├── Trial1.txt
│   ├── Trial2.txt
├── Subject2/
│   ├── Trial1.txt
│   ├── Trial2.txt
```

## Example CSV file
This is the contents of the [data_objects_table](attributes.md/#data_objects_table_path) file corresponding to the above directory structure:
```text
# /Users/my_username/my_dataset/data_objects_table.csv
| Subject Name | Trial Name |
| ------------ | ---------  |
|   Subject1   |   Trial1   |
|   Subject1   |   Trial2   |
|   Subject2   |   Trial1   |
|   Subject2   |   Trial2   |
```

## Example configuration file
This is the configuration file that would be used to build this dataset.
```toml
# /Users/username/dataset.toml
data_folder_path = "/Users/my_username/my_dataset/"
data_objects_hierarchy = [
    { "Subject Name" = "Subject"},
    { "Trial Name" = "Trial"},
]
data_objects_file_paths = "Subject/Trial"
data_objects_table_path = "data_objects_table.csv"
num_header_rows = 1
```