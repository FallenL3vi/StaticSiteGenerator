import unittest
from copy_content import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_export_title(self):
        markdown = """Big title test. Big big booom.
# Title here # or not
# - List herere
## Omgo h2"""
        
        self.assertEqual("Title here # or not", extract_title(markdown))


if __name__ == "__main__":
    unittest.main()
