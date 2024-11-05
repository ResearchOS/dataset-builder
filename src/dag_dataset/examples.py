import os

from .dataset import Dataset

def load_test_table():
    path = os.path.join(os.path.dirname(__file__), "test_table.csv")
    hierarchy = ["Subject", "Trial"]
    file_paths = "Subject/Trial"

    return Dataset(
        data_folder_path=os.getcwd(),
        data_objects_hierarchy=hierarchy,
        data_objects_file_paths=file_paths,
        data_objects_table_path=path,
        num_header_rows=1
    )
