# Imports
from dataclasses import dataclass, Field
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedClass(ISerializable):
    field1: int
    field2: bool


class TestSerializableFieldInfoGetter(unittest.TestCase):
    def test_all(self):
        """
        Testing if all the serializable fields return the same 'Field' objects in the different getters.
        """
        
        tested_data: dict[str, Field] = TestedClass._get_serializable_fields()
        
        for field_key, field_definition_value in tested_data.items():
            self.assertEqual(field_definition_value, TestedClass._get_field_definition(field_key))


# Main
if __name__ == '__main__':
    unittest.main()
