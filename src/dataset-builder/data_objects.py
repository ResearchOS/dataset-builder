
DATA_OBJECTS = {}

class DataObject:
    """Abstract base class for all dynamically created data classes with singleton behavior."""

    is_singleton = True    
    
    def __new__(cls, instance_name: str):
        # Retrieve the dictionary for the class name or initialize one
        class_data_objects = DATA_OBJECTS.setdefault(cls.__name__, {})

        # Check if an instance with the given name already exists
        if instance_name in class_data_objects and DataObject.is_singleton:
            # Return the existing instance if it exists
            return class_data_objects[instance_name]
        
        # Otherwise, create a new instance and store it
        instance = super(DataObject, cls).__new__(cls)
        if DataObject.is_singleton:
            class_data_objects[instance_name] = instance
        return instance

    def __init__(self, instance_name: str):
        # Initialization code that runs only once per unique instance_name
        self.instance_name = instance_name
        self.is_singleton = DataObject.is_singleton

    def __repr__(self):
        return f'{self.__class__.__name__}({self.instance_name})'


def create_data_object_classes(class_names: list[str]):
    """
    Dynamically create and return subclasses of DataObject for each class name in the list.
    
    Args:
        class_names (list[str]): A list of class names to be created.
    
    Returns:
        dict[str, type]: A dictionary where keys are class names and values are class objects.
    """
    parent_class = DataObject
    subclasses_dict = {}
    
    for class_name in class_names:
        # Dynamically define a new class with the given name, inheriting from DataObject
        new_class = type(
            class_name,  # Name of the class
            (parent_class,),  # Tuple of parent classes
            {}
        )

        parent_class = new_class
        
        # Add the newly created class to the dictionary
        subclasses_dict[class_name] = new_class
    
    return subclasses_dict
