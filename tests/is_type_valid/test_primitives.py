# Imports
import inspect
from dataclasses import dataclass
import unittest
from typing import Union

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedClass(ISerializable):
    integer: int
    string: str
    float: float
    boolean: bool


class TestPrimitiveTypeValidity(unittest.TestCase):
    def test_valid_primitives(self):
        """
        Testing if validly typed primitives are properly deserialized.
        """
        
        print("Testing primitive types individually against direct type...")
        self.assertTrue(ISerializable.is_type_valid(int, int))
        self.assertTrue(ISerializable.is_type_valid(str, str))
        self.assertTrue(ISerializable.is_type_valid(float, float))
        self.assertTrue(ISerializable.is_type_valid(bool, bool))
        
        print("Testing primitive types individually against primitive type set...")
        for tested_type in [int, str, float, bool]:
            self.assertTrue(ISerializable.is_type_valid([int, str, float, bool], tested_type))
        
        print("Testing primitive types individually against primitive type Union...")
        for tested_type in [int, str, float, bool]:
            self.assertTrue(ISerializable.is_type_valid(Union[int, str, float, bool], tested_type))
    
    def test_invalid_primitives(self):
        """
        Testing if invalidly typed primitives raise the appropriate exceptions.
        """
        
        pass

# Main
if __name__ == '__main__':
    unittest.main()
