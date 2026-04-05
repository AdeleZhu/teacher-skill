# tests/test_feishu_parser.py
"""Tests for feishu_parser.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from feishu_parser import parse_feishu_json


class TestParseFeishuJson(unittest.TestCase):
    def setUp(self):
        self.fixture_path = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'feishu_sample.json'
        )

    def test_parses_messages(self):
        result = parse_feishu_json(self.fixture_path)
        self.assertGreater(len(result['messages']), 0)

    def test_filters_by_teacher(self):
        result = parse_feishu_json(self.fixture_path, teacher_name='姚老师')
        for m in result['messages']:
            self.assertEqual(m['sender'], '姚老师')

    def test_parses_documents(self):
        result = parse_feishu_json(self.fixture_path)
        self.assertGreater(len(result['documents']), 0)

    def test_extracts_text_content(self):
        result = parse_feishu_json(self.fixture_path, teacher_name='姚老师')
        contents = [m['content'] for m in result['messages']]
        self.assertTrue(any('作业' in c for c in contents))


if __name__ == "__main__":
    unittest.main()
