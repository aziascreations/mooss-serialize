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
    def _is_type_valid(cls, expected_type, actual_type, process_listed_types: bool = False) -> bool:
        """
        Checks if a given type is the same or contained within a given set or expected types.
        
        :param expected_type: [As expected by a class def, may be complex]
        :param actual_type: [Should be basic -> std json types]
        :param process_listed_types: ???
        :return: True if the type is valid, False otherwise.
        :raises TypeError: ???
        """
        
        print("> is_type_valid: '{}', '{}'".format(expected_type, actual_type))
        
        # Fixing some potential issues
        if expected_type is None:
            print(">> Fixing 'expected_type' from 'None' to 'NoneType' !")
            expected_type = type(None)
        
        if actual_type is None:
            print(">> Fixing 'actual_type' from 'None' to 'NoneType' !")
            actual_type = type(None)
        
        # Testing some basic stuff
        if expected_type == type(None):
            print(">> Found 'NoneType' !")
            print(">> {} == {} -> {}".format(expected_type, actual_type, expected_type == actual_type))
            return expected_type == actual_type
        
        if expected_type is Any:
            return True
        
        if expected_type in [str, int, bool, float]:
            print(">> Detected a primitive type, not performing any filtering !")
            return expected_type is actual_type
        elif get_origin(expected_type) is Union:
            print(">> Detected a 'Union' or 'Optional' type")
            for individual_expected_type in get_args(expected_type):
                print(">> Testing '{}'...".format(individual_expected_type))
                if cls._is_type_valid(expected_type=individual_expected_type, actual_type=actual_type,
                                      process_listed_types=process_listed_types):
                    print(">> Found a valid match for the union/optional !")
                    return True
        elif isinstance(expected_type, type):
            # print(">> Detected a 'type' type '{}'".format(expected_type))
            # print(">> origin:'{}' & args:'{}'".format(get_origin(expected_type), get_args(expected_type)))
            # Catches classes, list, list[a, b], ...
            
            # TODO: Check if the following can be supported:
            #  Set, collection, namedTuple, NewType, Mapping, Sequence, Sequence, TypeVar, Iterable
            
            # Testing for composed types
            if get_origin(expected_type) in [list, dict, tuple, set]:
                print(">> Encountered a composed type -> {}".format(get_args(expected_type)))
                expected_type = get_origin(expected_type)
            
            # Checking for composed types and classes
            if expected_type in [list, dict, tuple, set]:
                # Simple list/dict/tuple
                print(">> Simple list/dict/tuple")
                return expected_type is actual_type
            
            # Checking for ISerializable interfaces
            # This check is disgusting, but it fixes the following error with list, dict, ???:
            # |_> TypeError: issubclass() arg 1 must be a class
            if expected_type.__class__ is not type:
                print(">> Should be a class a class -> '{}' !".format(expected_type.__class__))
                print(">> Does implement ISerializable ? -> {}".format(issubclass(expected_type, ISerializable)))
                print(">> Is actual_type a dict ? -> {}".format(actual_type is dict))
                return issubclass(expected_type, ISerializable) and actual_type is dict  # TODO: Check for null !
            else:
                print(">> Not a class or None !")
                raise TypeError("The expected type '{}' is a type that is not supported, nor is it a class !".format(
                    expected_type
                ))
        
        elif isinstance(expected_type, list):
            # Only gets triggered when passing list of individual types, not complex lists such as 'list[a, b]' !
            if process_listed_types:
                for individual_expected_type in expected_type:
                    if cls._is_type_valid(expected_type=individual_expected_type, actual_type=actual_type,
                                          process_listed_types=process_listed_types):
                        return True
            else:
                raise TypeError("The expected type '{}' is a list of individual types !")
        else:
            print(">> WTF !!!")
            raise TypeError("The expected type '{}' is not supported by 'ISerializable' !".format(expected_type))
        
        """
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
        """
        
        # Default return case when encountering supported types.
        return False
    
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
            if not cls._is_type_valid(value_class, type(value_data)):
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
