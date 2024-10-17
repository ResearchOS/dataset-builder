from config_reader import CONFIG_READER_FACTORY
from dataset import Dataset

def build_dataset(config_path: str):
    """Build the dataset from the config file."""
    config_reader = CONFIG_READER_FACTORY.get_config_reader(config_path)
    config = config_reader.read_config()
    return Dataset.build_from_dict(config)

if __name__=='__main__':
    config_path = 'dataset.toml'
    dataset = build_dataset(config_path)
    strings_dict = {
        "Subject": "Nairobi",
        "Trial": "Nairobi_006"
    }
    data_object = dataset.get_data_object(strings_dict)
    ancestry = dataset.get_ancestry(data_object)