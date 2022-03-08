# Imports
from dataclasses import dataclass
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedSuperNestedClass(ISerializable):
    field_int_super_nested: int


@dataclass
class TestedNestedClass(ISerializable):
    field_int_nested: int
    field_class_super_nested: TestedSuperNestedClass


@dataclass
class TestedParentClass(ISerializable):
    field_int_parent: int
    field_class_nested: TestedNestedClass


class TestSerializableTypeValidity(unittest.TestCase):
    def test_valid_single_serializable(self):
        """
        Testing if validly typed non-nested 'ISerializable' variables are properly deserialized.
        """
        
        print("Testing non-nested 'ISerializable' types...")
        
        # Preparing the data
        data = {
            "field_int_super_nested": 13
        }
        value: TestedSuperNestedClass = TestedSuperNestedClass.from_dict(data_dict=data, allow_unknown=False)
        
        # Testing
        self.assertEqual(TestedSuperNestedClass, type(value))
        self.assertEqual(13, value.field_int_super_nested)
        
        print("Done !")
    
    def test_valid_nested_serializable(self):
        """
        Testing if validly typed nested 'ISerializable' variables are properly deserialized.
        """
        
        print("Testing nested 'ISerializable' types...")
        
        # Preparing the data
        data = {
            "field_int_parent": 42,
            "field_class_nested": {
                "field_int_nested": 120,
                "field_class_super_nested": {
                    "field_int_super_nested": 13
                }
            }
        }
        value: TestedParentClass = TestedParentClass.from_dict(data_dict=data, allow_unknown=False)
        
        print(value)
        
        # Testing
        self.assertEqual(TestedParentClass, type(value))
        self.assertEqual(TestedNestedClass, type(value.field_class_nested))
        self.assertEqual(TestedSuperNestedClass, type(value.field_class_nested.field_class_super_nested))
        self.assertEqual(42, value.field_int_parent)
        self.assertEqual(120, value.field_class_nested.field_int_nested)
        self.assertEqual(13, value.field_class_nested.field_class_super_nested.field_int_super_nested)
        
        print("Done !")
    
    def test_invalid_single_serializable(self):
        """
        Testing if invalidly typed non-nested 'ISerializable' raise the appropriate exceptions.
        """
        
        pass
    
    def test_invalid_nested_serializable(self):
        """
        Testing if invalidly typed nested 'ISerializable' raise the appropriate exceptions.
        """
        
        pass


# Main
if __name__ == '__main__':
    unittest.main()
