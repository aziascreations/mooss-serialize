# Imports
from abc import ABC
import json
from typing import Union, get_origin, get_args, Any


# Classes
class ISerializable(ABC):
    @classmethod
    def get_serializable_fields(cls) -> dict[str, Any]:
        """
        Get a dict of all the serializable variables and their types.
        
        :return: A dictionary containing all the serializable variables with the variable as the key, and
        its type as the value.
        """
        
        return {
            key: value
            for annotations
            in list(filter(None, [
                x.__annotations__
                for x in cls.__mro__
                if issubclass(x, ISerializable) and hasattr(x, "__annotations__")
            ]))
            for key, value
            in annotations.items()
        }
    
    @classmethod
    def is_field_serializable(cls, field_name) -> bool:
        """
        Check if a given field is serializable.
        
        :param field_name: Field's name to check.
        :return: True if it is serializable, False otherwise.
        """
        return field_name in cls.get_serializable_fields()
    
    @classmethod
    def decompose_complex_types(cls, complex_type) -> list:
        pass
    
    @classmethod
    def is_type_valid(cls, expected_type, actual_type) -> bool:
        """
        Checks if a given type is the same or contained within a given set or expected types.
        
        :param expected_type:
        :param actual_type:
        :return: True if the type is valid, False otherwise.
        """
        print("> is_type_valid: '{}', '{}'".format(expected_type, actual_type))
        
        # Checking if we have a class that implements the 'ISerializable' interface and a dict.
        # TODO: Move down, to single stuff handling after list processing
        print(">> Tmp: Checking for complex types...")
        if isinstance(expected_type, type):
            print(">> Tmp: Found one, now checking if it implements 'ISerializable'...")
            if issubclass(expected_type, ISerializable) and actual_type is dict:
                print(">> Tmp: Returning early due to valid check !")
                return True
        
        # Checking if we have a Union, and converting it to a list if needed.
        if get_origin(expected_type) is Union:
            print(">> The 'expected_type' parameter is a Union, converting to a list...")
            expected_type = list(get_args(expected_type))
        
        # Checking if we have a list instead of a Union.
        if isinstance(expected_type, list):
            print(">> The 'expected_type' parameter is a list !")
            for expected_individual_type in expected_type:
                print(">> Testing '{}' against '{}' !".format(actual_type, expected_individual_type))
                if cls.is_type_valid(expected_individual_type, actual_type):
                    return True
            return False
        
        detected_valid_types = []
        
        if expected_type in [str, int, bool, float]:
            print(">> Detected a primitive type, adding it as-is to the 'detected_valid_types' list !")
            detected_valid_types.append(expected_type)
        
        # TODO: Special check for 'Any' !
        
        print(">> Comparing actual_type '{}' against detected_valid_types '{}' gotten from expected_type '{}' !".format(
            actual_type, detected_valid_types, expected_type
        ))
        return actual_type in detected_valid_types
    
    @classmethod
    def _deserialize_value(cls, value_class: type, value_data, allow_unknown: bool = False, validate_type: bool = True,
                           parsing_depth: int = -1):
        """
        ???
        
        :param value_class:
        :param value_data:
        :param allow_unknown: Unused unless a subclass of 'ISerializable' is encountered, it is passed to 'from_dict'.
        :param validate_type:
        :param parsing_depth: [recursive depth]
        :return: The deserialized value as a 'ISerializable' object, or its default value given in 'value_data'.
        """
        
        print("> _deserialize_value: '{}', '{}', {}, {}, {}".format(value_class, value_data, allow_unknown,
                                                                    validate_type, parsing_depth))
        
        # Validating the type.
        if validate_type:
            if not cls.is_type_valid(value_class, type(value_data)):
                raise TypeError(">> The '{}' type is supported by '{}'".format(type(value_data), value_class))
        
        # print("{} -> {}".format(value_class, value_data))
        
        # Skipping Union (Will be changed !!!)
        if get_origin(value_class) is Union:
            possible_types = get_args(value_class)
            # Checking if there are too many types
            if type(None) in possible_types:
                # We can assume that we will have some data since we are checking the field itself, and we need a value
                #  for that.
                possible_types = [x for x in possible_types if x is not type(None)]
            
            if len(possible_types) > 1:
                print("Too many types for '{}', using the first non-NoneType one !".format(get_args(value_class)))
            
            print(">> Now treating '{}' as '{}' !".format(value_class, possible_types[0]))
            print("   |_> {}".format(value_data))
            value_class = possible_types[0]
        
        if get_origin(value_class) is list:
            # print()
            return [cls._deserialize_value(
                value_class=get_args(value_class)[0],
                value_data=x,
                allow_unknown=allow_unknown
            ) for x in value_data]
        
        if get_origin(value_class) is not None:
            print(">> Encountered unhandled origin type: {}".format(value_class))
        
        if issubclass(value_class, ISerializable):
            print(">> Deserializing into '{}' from '{}' !".format(value_class, value_data))
            value_class: ISerializable
            return value_class.from_dict(data_dict=value_data, allow_unknown=allow_unknown)
        
        return value_data
    
    # TODO: Add 'check_required' with the Optional !
    
    @classmethod
    def from_dict(cls, data_dict: dict, allow_unknown: bool = False):
        print("> from_dict: '{}', '{}'".format(data_dict, allow_unknown))
        
        # FIXME: Handle missing and default values !!!
        
        # TODO: Implement check for nullable fields !
        
        # Checking for unknown fields.
        if not allow_unknown:
            for field_name in data_dict.keys():
                if not cls.is_field_serializable(field_name):
                    raise ValueError("The field '{}' is not present in the '{}' class !".format(
                        field_name, cls.__name__))
        
        # Filtering the dict to work on later on.
        filtered_dict = {key: value for key, value in data_dict.items() if cls.is_field_serializable(key)}
        
        # Preparing the other serializable classes.
        for key, value in filtered_dict.items():
            filtered_dict[key] = cls._deserialize_value(
                value_class=cls.__annotations__.get(key),
                value_data=value,
                allow_unknown=allow_unknown
            )
        
        # TODO: Check 'None' 'category(ies)' fields !
        
        # Preparing the returned class.
        return cls(**filtered_dict)
    
    @classmethod
    def from_json(cls, data_json: str, allow_unknown: bool = False):
        return ISerializable.from_dict(json.loads(data_json), allow_unknown)
    
    @classmethod
    def to_dict(cls):
        pass
    
    @classmethod
    def to_json(cls):
        return json.dumps(ISerializable.to_dict())
