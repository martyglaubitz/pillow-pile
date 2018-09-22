import os
import sys
import unittest

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import graph

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.graph_json = {
            'de': {
                'id': '8d738-78s7d8-89sd8-998ff',
                'de': {
                    'id': '49865-jhjzg34-987372-937z',
                    'home': {
                        'id': '786fg-72e6d-7262d-81738'
                    }
                }
            }
        }

    def test_resolve_existing_path(self):
        result, parent_doc = graph.get_document_entry_for_path(self.graph_json, ['de', 'de', 'home'])
        self.assertEqual(parent_doc['id'], '49865-jhjzg34-987372-937z')
        self.assertEqual(result['id'], '786fg-72e6d-7262d-81738')

    def test_resolve_nonexisting_path(self):
        result, parent_doc = graph.get_document_entry_for_path(self.graph_json, ['de', 'es', 'home'])
        self.assertIsNone(result)
        self.assertEqual(parent_doc['id'], '8d738-78s7d8-89sd8-998ff')


if __name__ == '__main__':
    unittest.main()