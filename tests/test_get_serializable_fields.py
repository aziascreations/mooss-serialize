# Imports
from dataclasses import dataclass
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedParentClass(ISerializable):
    field1: int


@dataclass
class TestedChildrenClass(TestedParentClass):
    field2: int


class TestSerializableFieldGetter(unittest.TestCase):
    def test_parent(self):
        """
        Testing if a parent/root class reports its serializable fields properly with the 'get_serializable_fields'
        getter.
        """
        
        expected_variables = ['field1']
        
        self.assertListEqual(
            sorted(expected_variables),
            sorted(list(TestedParentClass._get_serializable_fields().keys()))
        )
    
    def test_children(self):
        """
        Testing if a children class reports its serializable fields properly with the 'get_serializable_fields'
        getter.
        """
        
        expected_variables = ['field1', 'field2']
        
        self.assertListEqual(
            sorted(expected_variables),
            sorted(list(TestedChildrenClass._get_serializable_fields().keys()))
        )


# Main
if __name__ == '__main__':
    unittest.main()
