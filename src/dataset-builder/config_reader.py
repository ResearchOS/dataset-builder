from abc import abstractmethod

class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file

    @abstractmethod
    def read_config(self):
        raise NotImplementedError("Subclasses must implement this method")
    
class ConfigReaderFactory:
    def __init__(self):
        self.config_readers = {}

    def get_config_reader(self, config_file) -> ConfigReader:
        ext = config_file.split('.')[-1]
        if ext not in self.config_readers:
            raise ValueError(f"Unsupported config file type: {ext}")
        return self.config_readers[ext](config_file)
    
CONFIG_READER_FACTORY = ConfigReaderFactory()
    
# Create decorator
def register_config_reader(ext):
    def decorator(cls):
        CONFIG_READER_FACTORY.config_readers[ext] = cls
        return cls
    return decorator

# Register the config reader
@register_config_reader('toml')
class TomlConfigReader(ConfigReader):
    def read_config(self):
        import toml
        with open(self.config_file) as f:
            return toml.load(f)
    
@register_config_reader('json')
class JsonConfigReader(ConfigReader):
    def read_config(self):
        import json
        with open(self.config_file) as f:
            return json.load(f)
        
@register_config_reader('yaml')
class YamlConfigReader(ConfigReader):
    def read_config(self):
        import yaml
        with open(self.config_file) as f:
            return yaml.safe_load(f)