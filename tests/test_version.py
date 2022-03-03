# Imports
import semver
import unittest

import mooss.serialize.__version__ as __version__


# Tests
class TestVersion(unittest.TestCase):
    def test_version(self):
        """
        Testing if the version follows the 'Semantic Versioning' format.
        """
        
        # Assertion is done through the absence of any 'ValueError' exception.
        semver.parse(__version__.VERSION)


# Main
if __name__ == '__main__':
    unittest.main()
