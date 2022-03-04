# Imports
from dataclasses import dataclass
from typing import Union, Any, Optional
import unittest

from mooss.serialize.interface import ISerializable


# Classes
@dataclass
class TestedValidClass(ISerializable):
    pass


class TestedInvalidClass(ISerializable):
    pass


# Unit tests
class TestTypeValidity(unittest.TestCase):
    def test_valid(self):
        """
        Testing if validly types are properly detected.
        """
        
        print("Testing valid primitive types...")
        self.assertTrue(ISerializable._is_type_valid(int, int))
        self.assertTrue(ISerializable._is_type_valid(str, str))
        self.assertTrue(ISerializable._is_type_valid(float, float))
        self.assertTrue(ISerializable._is_type_valid(bool, bool))
        
        print("Testing valid list, dict, tuple, set...")
        self.assertTrue(ISerializable._is_type_valid(list, list))
        self.assertTrue(ISerializable._is_type_valid(dict, dict))
        self.assertTrue(ISerializable._is_type_valid(tuple, tuple))
        self.assertTrue(ISerializable._is_type_valid(set, set))
        
        print("Testing valid composed list, dict, tuple, set...")
        self.assertTrue(ISerializable._is_type_valid(list[str, int], type(["abc"])))
        self.assertTrue(ISerializable._is_type_valid(dict[str, int], type({'text': 'test', 'number': 123})))
        self.assertTrue(ISerializable._is_type_valid(tuple[str, int], type(("abc",))))
        # FIXME: self.assertTrue(ISerializable.is_type_valid(set[str, int], list))
        
        print("Testing valid individual types in list...")
        self.assertTrue(ISerializable._is_type_valid([str, int], int, process_listed_types=True))
        
        print("Testing valid serializable class...")
        self.assertTrue(ISerializable._is_type_valid(TestedValidClass, dict))
        
        print("Testing valid typing special types...")
        self.assertTrue(ISerializable._is_type_valid(Union[str, int], int))
        self.assertTrue(ISerializable._is_type_valid(Optional[str], str))
        self.assertTrue(ISerializable._is_type_valid(Optional[str], None))
        self.assertTrue(ISerializable._is_type_valid(None, None))
        
        print("Testing validity with 'Any'...")
        for tested_type in [int, str, float, bool, [str, int]]:
            self.assertTrue(ISerializable._is_type_valid(Any, tested_type, process_listed_types=True))
        
        print("Testing the absence of 'TypeError' with 'Any' and list of individual types...")
        self.assertTrue(ISerializable._is_type_valid(Any, int, process_listed_types=False))
    
    def test_invalid(self):
        """
        Testing if invalid types are properly detected.
        """
        
        print("Testing invalid primitive types...")
        self.assertFalse(ISerializable._is_type_valid(int, float))
        self.assertFalse(ISerializable._is_type_valid(str, int))
        self.assertFalse(ISerializable._is_type_valid(float, bool))
        self.assertFalse(ISerializable._is_type_valid(bool, str))
        self.assertFalse(ISerializable._is_type_valid(bool, None))
        self.assertFalse(ISerializable._is_type_valid(None, bool))
        
        print("Testing invalid list, dict, tuple, set...")
        self.assertFalse(ISerializable._is_type_valid(list, set))
        self.assertFalse(ISerializable._is_type_valid(dict, list))
        self.assertFalse(ISerializable._is_type_valid(tuple, dict))
        self.assertFalse(ISerializable._is_type_valid(set, tuple))
        self.assertFalse(ISerializable._is_type_valid(list, None))
        self.assertFalse(ISerializable._is_type_valid(None, list))
        
        print("Testing invalid serializable class...")
        self.assertFalse(ISerializable._is_type_valid(TestedInvalidClass, int))
        self.assertFalse(ISerializable._is_type_valid(TestedInvalidClass, None))
        self.assertFalse(ISerializable._is_type_valid(None, TestedInvalidClass))
        
        print("Testing invalid typing special types...")
        self.assertFalse(ISerializable._is_type_valid(Union[str, int], bool))
        self.assertFalse(ISerializable._is_type_valid(Optional[str], float))
        
        print("Testing invalid individual types in list...")
        self.assertRaises(TypeError, lambda: ISerializable._is_type_valid([str, int], int, process_listed_types=False))
        self.assertFalse(ISerializable._is_type_valid([str, int], bool, process_listed_types=True))


# Main
if __name__ == '__main__':
    unittest.main()
