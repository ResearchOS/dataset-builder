
from .constants import REQUIRED_ATTR_NAMES_LIST

class DictValidator:

    def validate(self, config: dict):
        for attr in REQUIRED_ATTR_NAMES_LIST:
            if attr not in config:
                raise ValueError(f'Missing required attribute: {attr}')
        for attr in config:
            attr_validator = ATTRIBUTE_VALIDATOR_FACTORY.attribute_validators.get(attr)
            if attr_validator is not None:
                attr_validator().validate(config[attr])

class AttributeValidator:
    
    def validate(self, value):
        raise NotImplementedError

    
class AttributeValidatorFactory:    

    def __init__(self):
        self.attribute_validators = {}
    
    def register(self, attr_name: str, cls) -> AttributeValidator:
        self.attribute_validators[attr_name] = cls
    pass

ATTRIBUTE_VALIDATOR_FACTORY = AttributeValidatorFactory()

# Decorator for registering attribute validators
def register_attribute_validator(attr_name: str):
    def decorator(cls):
        ATTRIBUTE_VALIDATOR_FACTORY.register(attr_name, cls)
        return cls
    return decorator

@register_attribute_validator('data_folder_path')
class DataFolderPathValidator(AttributeValidator):
    
    def validate(self, value: str):
        if not isinstance(value, str):
            raise ValueError('Invalid data folder path type. Must be string')

@register_attribute_validator('data_objects_hierarchy')
class DataObjectsHierarchyValidator(AttributeValidator):
    
    def validate(self, value: list):
        pass

@register_attribute_validator('data_objects_file_paths')
class DataObjectsFilePathsValidator(AttributeValidator):
    
    def validate(self, value):
        pass

@register_attribute_validator('data_objects_table_path')
class DataObjectsTablePathValidator(AttributeValidator):
    
    def validate(self, value: str):        
        if not isinstance(value, str):
            raise ValueError('Invalid data objects table path')
        value = value.lower()
        if not value.endswith(('.csv', '.xlsx')):
            raise ValueError('Data objects table path must end with .csv or .xlsx')        

@register_attribute_validator('num_header_rows')
class NumHeaderRowsValidator(AttributeValidator):
    
    def validate(self, value: int):
        if not isinstance(value, int):
            raise ValueError('Invalid num header rows type. Must be integer')
        if value < 0:
            raise ValueError('Num header rows must be non-negative')
        

@register_attribute_validator('other_columns')
class OtherColumnsValidator(AttributeValidator):

    def validate(self, value: list):
        pass