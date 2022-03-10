# Imports
import copy
import json
from dataclasses import dataclass
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedPrimitiveClass(ISerializable):
    field_primitive_int: int
    field_primitive_bool: bool
    field_primitive_str: str
    field_primitive_float: float


@dataclass
class TestedDoubleNestedClass(ISerializable):
    field_int_double_nested: int


@dataclass
class TestedSingleNestedClass(ISerializable):
    field_int_single_nested: int
    field_class_double_nested: TestedDoubleNestedClass


@dataclass
class TestedRootNestedClass(ISerializable):
    field_int_root: int
    field_class_single_nested: TestedSingleNestedClass


class TestFromMethods(unittest.TestCase):
    def test_valid_primitive(self):
        """Testing if valid primitive types are properly deserialized."""
        
        print("Testing valid primitives...")
        data_valid = {
            'field_primitive_int': 42,
            'field_primitive_str': "Hello world !",
            'field_primitive_float': 2.0,
            'field_primitive_bool': True,
        }
        
        print("> Preparing classes...")
        test_class_dict: TestedPrimitiveClass = TestedPrimitiveClass.from_dict(data_dict=data_valid)
        test_class_json: TestedPrimitiveClass = TestedPrimitiveClass.from_json(data_json=json.dumps(data_valid))
        
        print("> Checking each class...")
        for deserialized_class in [test_class_dict, test_class_json]:
            self.assertEqual(data_valid.get('field_primitive_int'), deserialized_class.field_primitive_int)
            self.assertEqual(data_valid.get('field_primitive_str'), deserialized_class.field_primitive_str)
            self.assertEqual(data_valid.get('field_primitive_float'), deserialized_class.field_primitive_float)
            self.assertEqual(data_valid.get('field_primitive_bool'), deserialized_class.field_primitive_bool)
    
    def test_invalid_primitive(self):
        """Testing if invalid primitive types are properly treated."""
        
        print("Testing invalid primitives...")
        data_valid_base = {
            'field_primitive_int': 42,
            'field_primitive_str': "Hello world !",
            'field_primitive_float': 2.0,
            'field_primitive_bool': True,
        }
        data_invalid_fields = {
            'field_primitive_int': "abc",
            'field_primitive_str': 123,
            'field_primitive_float': False,
            'field_primitive_bool': "yo mama !",
        }
        
        print("> Testing the presence of raised exceptions...")
        for invalid_key, invalid_value in data_invalid_fields.items():
            print(">> Replacing '{}' from '{}' to '{}' !".format(
                invalid_key, data_valid_base.get(invalid_key), invalid_value
            ))
            new_dict = copy.deepcopy(data_valid_base)
            new_dict.update({invalid_key: invalid_value})
            self.assertRaises(TypeError, lambda: TestedPrimitiveClass.from_dict(data_dict=new_dict))
    
    def test_nested_serializable(self):
        """
        Testing if validly typed nested 'ISerializable' variables are properly deserialized.
        """
        
        print("Testing nested 'ISerializable' types...")
        
        # Preparing the data
        data = {
            "field_int_root": 42,
            "field_class_single_nested": {
                "field_int_single_nested": 120,
                "field_class_double_nested": {
                    "field_int_double_nested": 13
                }
            }
        }
        
        print("> Preparing classes...")
        class_dict: TestedRootNestedClass = TestedRootNestedClass.from_dict(data_dict=data)
        class_json: TestedRootNestedClass = TestedRootNestedClass.from_json(data_json=json.dumps(data))
        
        print("> Checking each class...")
        for deserialized_class in [class_dict, class_json]:
            # Checking the types of deserialized ISerializable classes
            self.assertEqual(TestedRootNestedClass, type(deserialized_class))
            self.assertEqual(TestedSingleNestedClass, type(deserialized_class.field_class_single_nested))
            self.assertEqual(
                TestedDoubleNestedClass, type(deserialized_class.field_class_single_nested.field_class_double_nested)
            )
            
            # Checking the value of other potentially nested variables.
            self.assertEqual(42, deserialized_class.field_int_root)
            self.assertEqual(120, deserialized_class.field_class_single_nested.field_int_single_nested)
            self.assertEqual(
                13, deserialized_class.field_class_single_nested.field_class_double_nested.field_int_double_nested
            )
    
    def test_allow_unknown(self):
        """
        Testing if the 'allow_unknown', 'add_unknown_as_is' and 'allow_as_is_unknown_overloading' parameters
        works properly.
        """
        
        print("Testing parameters related to unknown fields...")
        
        # Preparing the data
        data = {
            "field_int_double_nested": 42,
            "unknown_generic_value": 120,  # This value is not defined in the 'TestedDoubleNestedClass' class !
        }
        
        print("Testing with default and restrictive parameters...")
        print("|_> allow_unknown: False  (Explicit & Default)")
        self.assertRaises(ValueError, lambda: TestedDoubleNestedClass.from_dict(data_dict=data))
        self.assertRaises(ValueError, lambda: TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=False))
        
        print("Testing with permissive unknown parameters, and default ones for the future usage parameters...")
        print("|_> allow_unknown: True  (Explicit)")
        print("|_> add_unknown_as_is: False  (Explicit & Default)")
        print("|_> allow_as_is_unknown_overloading: False  (Explicit & Default)")
        classes_to_test = [
            TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=True),
            TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=True, add_unknown_as_is=False,
                                              allow_as_is_unknown_overloading=False)
        ]
        for class_to_test in classes_to_test:
            self.assertFalse(hasattr(class_to_test, "unknown_generic_value"))
        
        print("Testing with permissive unknown parameters while adding non-conflicting unknowns...")
        print("|_> allow_unknown: True  (Explicit)")
        print("|_> add_unknown_as_is: True  (Explicit)")
        print("|_> allow_as_is_unknown_overloading: False  (Explicit & Default)")
        classes_to_test = [
            TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=True, add_unknown_as_is=True),
            TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=True, add_unknown_as_is=True,
                                              allow_as_is_unknown_overloading=False)
        ]
        for class_to_test in classes_to_test:
            self.assertTrue(hasattr(class_to_test, "unknown_generic_value"))
            self.assertEqual(data.get("unknown_generic_value"), getattr(class_to_test, "unknown_generic_value"))
        
        # This is the one that should be the least likely to mess everything up if changed forcefully.
        print("Adding the '__repr__' unknown field to the 'data' dict to test 'allow_as_is_unknown_overloading'...")
        data.update({"__repr__": "fuck"})
        
        print("Testing unknown parameters overloading ability...")
        print("|_> allow_unknown: True  (Explicit)")
        print("|_> add_unknown_as_is: True  (Explicit)")
        print("|_> allow_as_is_unknown_overloading: True & False  (Explicit)")
        
        # Testing if the overloading field cannot be added back in the final class.
        self.assertRaises(ValueError, lambda: TestedDoubleNestedClass.from_dict(
            data_dict=data, allow_unknown=True, add_unknown_as_is=True, allow_as_is_unknown_overloading=False))
        
        # Testing if the overloading field can be added back in the final class.
        mutilated_class = TestedDoubleNestedClass.from_dict(data_dict=data, allow_unknown=True, add_unknown_as_is=True,
                                                            allow_as_is_unknown_overloading=True)
        self.assertEqual(data.get("__repr__"), getattr(mutilated_class, "__repr__"))


# Main
if __name__ == '__main__':
    unittest.main()
