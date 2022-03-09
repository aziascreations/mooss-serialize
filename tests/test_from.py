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
        
        print("> With 'from_dict'...")
        class_dict: TestedRootNestedClass = TestedRootNestedClass.from_dict(data_dict=data)
        
        self.assertEqual(TestedRootNestedClass, type(class_dict))
        self.assertEqual(TestedSingleNestedClass, type(class_dict.field_class_single_nested))
        self.assertEqual(TestedDoubleNestedClass, type(class_dict.field_class_single_nested.field_class_double_nested))
        
        self.assertEqual(42, class_dict.field_int_root)
        self.assertEqual(120, class_dict.field_class_single_nested.field_int_single_nested)
        self.assertEqual(13, class_dict.field_class_single_nested.field_class_double_nested.field_int_double_nested)
        
        print("> With 'from_json'...")
        class_json: TestedRootNestedClass = TestedRootNestedClass.from_json(data_json=json.dumps(data))
        
        self.assertEqual(TestedRootNestedClass, type(class_json))
        self.assertEqual(TestedSingleNestedClass, type(class_json.field_class_single_nested))
        self.assertEqual(TestedDoubleNestedClass, type(class_json.field_class_single_nested.field_class_double_nested))
        
        self.assertEqual(42, class_json.field_int_root)
        self.assertEqual(120, class_json.field_class_single_nested.field_int_single_nested)
        self.assertEqual(13, class_json.field_class_single_nested.field_class_double_nested.field_int_double_nested)


# Main
if __name__ == '__main__':
    unittest.main()
