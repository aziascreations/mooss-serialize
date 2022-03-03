# Imports
from dataclasses import dataclass
import random
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedClass(ISerializable):
    field1: int


class TestSerializableFieldGetter(unittest.TestCase):
    def test_serializable_fields(self):
        self.assertTrue(TestedClass.is_field_serializable("field1"))
    
    def test_unserializable_fields(self):
        for member_name in dir(TestedClass):
            if member_name != "field1":
                self.assertFalse(TestedClass.is_field_serializable(member_name))
    
    def test_non_existent_fields(self):
        for i in range(10):
            self.assertFalse(TestedClass.is_field_serializable("non_existent_{}".format(random.randint(100, 999))))


# Main
if __name__ == '__main__':
    unittest.main()
