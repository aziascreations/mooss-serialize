# Imports
from dataclasses import dataclass
import unittest

from mooss.serialize.interface import ISerializable


# Unit tests
@dataclass
class TestedClass(ISerializable):
    integer: int
    string: str
    float: float
    boolean: bool


class TestPrimitiveTypes(unittest.TestCase):
    def test_all_set(self):
        """Testing if a class with primitive types can be properly deserialized."""
        
        data = {
            'integer': 42,
            'string': "Hello world !",
            'float': 2.0,
            'boolean': True,
        }
        
        test_class: TestedClass = TestedClass.from_dict(data_dict=data, allow_unknown=False)
        
        self.assertEqual(data.get('integer'), test_class.integer)
        self.assertEqual(data.get('string'), test_class.string)
        self.assertEqual(data.get('float'), test_class.float)
        self.assertEqual(data.get('boolean'), test_class.boolean)
    
    def test_invalid_type(self):
        """Testing if an invalidly typed primitive raises a value error with standard types."""
        
        data = {
            'integer': 42,
            'string': False,
            'float': 2.0,
            'boolean': True,
        }
        
        self.assertRaises(ValueError, lambda: TestedClass.from_dict(data_dict=data, allow_unknown=False))


# Main
if __name__ == '__main__':
    unittest.main()
