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
class TestFieldDeserialization(unittest.TestCase):
    def test_valid(self):
        """
        Testing if validly types are properly detected.
        """
        
        print("Testing valid options in '_deserialize_value'...")
    
    def test_invalid(self):
        """
        Testing if invalid types are properly detected.
        """
        
        print("Testing invalid options in '_deserialize_value'...")


# Main
if __name__ == '__main__':
    unittest.main()
