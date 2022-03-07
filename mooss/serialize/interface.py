# Imports
from abc import ABC
import copy
import json
import dataclasses
from dataclasses import dataclass, Field
from typing import Union, get_origin, get_args, Any, Optional

from .field_types import EFieldType

# Notes
"""
It should be possible to simplify a lot of stuff by using ISerializable.__dataclass_fields__.values() on dataclasses !
See: dataclasses.fields()
"""


# Classes
class ISerializable(ABC):
    __dataclass_fields__: dict[str, Field]
    
    @classmethod
    def _get_serializable_fields(cls) -> dict[str, Field]:
        """
        Get a dict of all the serializable variables and their types.
        
        :return: A dictionary containing all the serializable variables with the variable as the key, and
        a 'Field' object from the 'dataclasses' module representing them.
        """
        
        # TODO: Add a way to filter out fields when declaring the class !
        
        return cls.__dataclass_fields__
    
    @classmethod
    def _is_field_serializable(cls, field_name) -> bool:
        """
        Check if a given field is serializable.
        
        :param field_name: Field's name to check.
        :return: True if it is serializable, False otherwise.
        """
        
        return field_name in cls._get_serializable_fields()
    
    @classmethod
    def _get_field_definition(cls, field_name) -> Optional[Field]:
        """
        Gets a given field's 'Field' definition.
        
        :param field_name: Field's name to check.
        :return: The relevant 'Field' object if found, None otherwise.
        """
        
        return cls._get_serializable_fields().get(field_name)
    
    @classmethod
    def _analyse_type(cls, expected_type, actual_type, process_listed_types: bool = False) -> tuple[bool, EFieldType]:
        """
        Analyses a given type and checks the given types are compatible and which type of field it is.
        
        :param expected_type: [As expected by a class def, may be complex]
        :param actual_type: [Should be basic -> std json types]
        :param process_listed_types: ???
        :return: True if the type is valid, False otherwise.
        :raises TypeError: ???
        """
        
        # print("> is_type_valid: '{}', '{}'".format(expected_type, actual_type))
        
        # Fixing some potential issues
        if expected_type is None:
            # print(">> Fixing 'expected_type' from 'None' to 'NoneType' !")
            expected_type = type(None)
        
        if actual_type is None:
            # print(">> Fixing 'actual_type' from 'None' to 'NoneType' !")
            actual_type = type(None)
        
        # Testing some basic stuff
        if expected_type == type(None):
            # print(">> Found 'NoneType' !")
            # print(">> {} == {} -> {}".format(expected_type, actual_type, expected_type == actual_type))
            return expected_type == actual_type, EFieldType.FIELD_TYPE_PRIMITIVE
        
        if expected_type is Any:
            return True, EFieldType.FIELD_TYPE_UNKNOWN
        
        if expected_type in [str, int, bool, float]:
            # print(">> Detected a primitive type, not performing any filtering !")
            return expected_type is actual_type, EFieldType.FIELD_TYPE_PRIMITIVE
        elif get_origin(expected_type) is Union:
            # print(">> Detected a 'Union' or 'Optional' type")
            for individual_expected_type in get_args(expected_type):
                # print(">> Testing '{}'...".format(individual_expected_type))
                analysed_data_result = cls._analyse_type(expected_type=individual_expected_type,
                                                         actual_type=actual_type,
                                                         process_listed_types=process_listed_types)
                # print(">> Found a valid match for the union/optional !")
                if analysed_data_result[0]:
                    return analysed_data_result
        elif isinstance(expected_type, type):
            # print(">> Detected a 'type' type '{}'".format(expected_type))
            # print(">> origin:'{}' & args:'{}'".format(get_origin(expected_type), get_args(expected_type)))
            # Catches classes, list, list[a, b], ...
            
            # TODO: Check if the following can be supported:
            #  Set, collection, namedTuple, NewType, Mapping, Sequence, Sequence, TypeVar, Iterable
            
            # Testing for composed types
            if get_origin(expected_type) in [list, dict, tuple, set]:
                # print(">> Encountered a composed type -> {}".format(get_args(expected_type)))
                expected_type = get_origin(expected_type)
            
            # Checking for composed types and classes
            if expected_type in [list, dict, tuple, set]:
                # Simple list/dict/tuple
                # print(">> Simple list/dict/tuple")
                return expected_type is actual_type, EFieldType.FIELD_TYPE_ITERABLE
            
            # Checking for ISerializable interfaces
            # This check is disgusting, but it fixes the following error with list, dict, ???:
            # |_> TypeError: issubclass() arg 1 must be a class
            if expected_type.__class__ is not type:
                # print(">> Should be a class a class -> '{}' !".format(expected_type.__class__))
                # print(">> Does implement ISerializable ? -> {}".format(issubclass(expected_type, ISerializable)))
                # print(">> Is actual_type a dict ? -> {}".format(actual_type is dict))
                # TODO: Check for null !
                return issubclass(expected_type, ISerializable) and actual_type is dict,\
                       EFieldType.FIELD_TYPE_SERIALIZABLE
            else:
                # print(">> Not a class or None !")
                raise TypeError("The expected type '{}' is a type that is not supported, nor is it a class !".format(
                    expected_type
                ))
        
        elif isinstance(expected_type, list):
            # Only gets triggered when passing list of individual types, not complex lists such as 'list[a, b]' !
            if process_listed_types:
                for individual_expected_type in expected_type:
                    analysed_data_result = cls._analyse_type(expected_type=individual_expected_type,
                                                             actual_type=actual_type,
                                                             process_listed_types=process_listed_types)
                    if analysed_data_result[0]:
                        return analysed_data_result
            else:
                raise TypeError("The expected type '{}' is a list of individual types !")
        else:
            # print(">> WTF !!!")
            raise TypeError("The expected type '{}' is not supported by 'ISerializable' !".format(expected_type))
        
        # Default return case when encountering supported types.
        return False, EFieldType.FIELD_TYPE_UNKNOWN

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
        
        return cls._analyse_type(expected_type, actual_type, process_listed_types)[0]
    
    @classmethod
    def _deserialize_value(cls, value_class: type, value_data: Any, allow_unknown: bool = False,
                           validate_type: bool = True, parsing_depth: int = -1):
        """
        Deserializes a given value into the given type while checking for strict typing and recursive depth if needed.
        
        :param value_class: Expected type of the parsed data as defined in the class' annotations.
        :param value_data: The data that will be deserialized into a variable of the given 'value_class'.
        :param allow_unknown: Unused unless a subclass of 'ISerializable' is encountered, it is passed to and from
         'cls.from_dict()'.
        :param validate_type: A switch to toggle the strict typechecks that may raise 'TypeError' exceptions.
        :param parsing_depth: The amount of recursive call that can be done to parse nested deserializable structures.
        :return: The deserialized value as a 'ISerializable' object, or its default value given in 'value_data'.
        :raises TypeError: If a mismatch between the expected and received data's types is found, requires
         'validate_type' to be set to 'True'.
        """
        
        print("> _deserialize_value: '{}', '{}', {}, {}, {}".format(value_class, value_data, allow_unknown,
                                                                    validate_type, parsing_depth))
        
        # Checking if we have reached the end of the allowed recursive depth.
        if parsing_depth == 0:
            print(">> Ignoring due to depth !")
            return value_data
        
        # Validating the type.
        if validate_type:
            if not cls._is_type_valid(value_class, type(value_data)):
                raise TypeError(">> The '{}' type is supported by '{}'".format(type(value_data), value_class))
        
        print("{} -> {}".format(value_class, value_data))
        
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
    
    @classmethod
    def from_dict(cls, data_dict: dict, allow_unknown: bool = False, add_unknown_as_is: bool = False,
                  allow_as_is_unknown_overloading: bool = False, allow_missing_required: bool = False,
                  allow_missing_nullable: bool = True, add_unserializable_as_dict: bool = False,
                  validate_type: bool = True, parsing_depth: int = -1, do_deep_copy: bool = False):
        """
        ???
        
        :param data_dict:
        :param allow_unknown:
        :param add_unknown_as_is:
        :param allow_as_is_unknown_overloading:
        :param allow_missing_required:
        :param allow_missing_nullable:
        :param add_unserializable_as_dict:
        :param validate_type:
        :param parsing_depth:
        :param do_deep_copy:
        :return: The parsed 'ISerializable' class.
        :raises TypeError: If a mismatch between the expected and received data's types is found, requires
         'validate_type' to be set to 'True'.
        """
        
        # TODO: allow_primitive_type_casting: bool = False
        
        # FIXME: Check for missing required fields, or let the interpreter do it during instantiation ?
        
        print("> from_dict: '{}', '{}'".format(data_dict, allow_unknown))
        
        # Checking if we have reached the end of the allowed recursive depth.
        if parsing_depth == 0:
            print(">> ")
            return data_dict
        
        # Checking if we need to do a deep copy to prevent weird interactions if the dict is passed by reference.
        _temp_data_dict: dict[str, Any]
        if do_deep_copy:
            print(">> Doing deep copy !")
            _temp_data_dict = copy.deepcopy(data_dict)
        else:
            print(">> Doing shallow copy !")
            _temp_data_dict = copy.copy(data_dict)
        
        # Checking for unknown fields.
        _unknown_data: Optional[dict[str, Any]] = dict() if allow_unknown and add_unknown_as_is else None
        """
        Nullable dictionary that may exist and contain any unknown field that will be handled when instantiating the
        'ISerializable' class itself.
        May be left as 'None' if it shouldn't be used !
        """
        
        for field_name in _temp_data_dict.keys():
            print(">> Checking what to do with {}...".format(field_name))
            if not cls._is_field_serializable(field_name):
                if allow_unknown:
                    if add_unknown_as_is:
                        print(">> Separating")
                        # Separating them out for later.
                        _unknown_data[field_name] = _temp_data_dict.pop(field_name)
                    else:
                        print(">> Removing")
                        # Removing them to simply ignore them.
                        _temp_data_dict.pop(field_name)
                else:
                    print(">> Spazing out")
                    # Not allowing any.
                    raise ValueError("The field '{}' is not present in the '{}' class !".format(
                        field_name, cls.__name__))
        
        # Analysing all valid fields before using them to instantiate a new 'ISerializable' class.
        for expected_field_name, expected_field_definition in cls._get_serializable_fields().items():
            print(">> Analysing '{}' => '{}'...".format(expected_field_name, expected_field_definition))
            
            # Checking if the field is present in the given data and fixing it if possible.
            if expected_field_name not in _temp_data_dict:
                print(">> Not found in given dict !")
                # Checking if it has a default value in its class' definition.
                if expected_field_definition.default is dataclasses.MISSING:
                    raise ValueError("Could not get a default value for the '{}' expected field in '{}' !".format(
                        expected_field_name, cls.__name__
                    ))
                else:
                    print(">> Assigned '{}' as default value !".format(expected_field_definition.default))
                    # TODO: Check if Field lists work properly !
                    _temp_data_dict[expected_field_name] = expected_field_definition.default
            
            # Getting some info on the field and its type for later.
            is_type_valid, field_simplified_type = cls._analyse_type(
                expected_type=expected_field_definition.type,
                actual_type=type(_temp_data_dict.get(expected_field_name)),
                process_listed_types=False)
            print(">> Grabbed more info: is_type_Valid:{}, field_simplified_type:{}".format(
                is_type_valid, field_simplified_type
            ))
            
            # Checking if the expected types are compatible.
            if validate_type and not is_type_valid:
                raise TypeError("The '{type_actual}' type is supported by '{type_expected}'".format(
                    type_actual=type(_temp_data_dict.get(expected_field_name)),
                    type_expected=expected_field_definition.type
                ))
            
            # print("FIELD_TYPE_UNKNOWN => '{}'".format(EFieldType.FIELD_TYPE_UNKNOWN))
            # print("FIELD_TYPE_PRIMITIVE => '{}'".format(EFieldType.FIELD_TYPE_PRIMITIVE))
            # print("FIELD_TYPE_ITERABLE => '{}'".format(EFieldType.FIELD_TYPE_ITERABLE))
            # print("FIELD_TYPE_SERIALIZABLE => '{}'".format(EFieldType.FIELD_TYPE_SERIALIZABLE))
            
            # Attempting to parse the data if, and only if, it is needed to do so.
            if field_simplified_type == EFieldType.FIELD_TYPE_ITERABLE:
                # We are checking for potentially listed 'ISerializable' classes.
                print(">> Type: Is iterable !")
                
                is_listed_type_valid, listed_field_simplified_type = cls._analyse_type(
                    expected_type=get_args(expected_field_definition.type),
                    actual_type=type(_temp_data_dict.get(expected_field_name)[0]),
                    process_listed_types=True)
                print(">> Grabbed more info on listed type: is_type_Valid:{}, field_simplified_type:{}".format(
                    is_listed_type_valid, listed_field_simplified_type
                ))
                
                """
                return [cls._deserialize_value(
                    value_class=get_args(value_class)[0],
                    value_data=x,
                    allow_unknown=allow_unknown
                ) for x in value_data]
                """
            
            if field_simplified_type == EFieldType.FIELD_TYPE_SERIALIZABLE:
                print(">> Type: Is serializable !")
                # FIXME: This !!!
                _temp_data_dict[expected_field_name] = _temp_data_dict.get(expected_field_name)
                # value_class: ISerializable
                # return value_class.from_dict(data_dict=value_data, allow_unknown=allow_unknown)
            else:
                print(">> Type: Other/primitive/list, will be using it as-is !")
                pass
        
        # TODO: Implement check for nullable fields !
        # TODO: Unknowns !
        
        # Preparing the returned class.
        return cls(**_temp_data_dict)
    
    @classmethod
    def from_json(cls, data_json: str, allow_unknown: bool = False):
        return ISerializable.from_dict(json.loads(data_json), allow_unknown)
    
    @classmethod
    def to_dict(cls):
        # raise NotImplementedError("The method 'to_dict()' is not implemented yet !")
        pass
    
    @classmethod
    def to_json(cls):
        return json.dumps(ISerializable.to_dict())
