# tests/test_qq_parser.py
"""Tests for qq_parser.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from qq_parser import parse_qq_txt


class TestParseQqTxt(unittest.TestCase):
    def setUp(self):
        self.fixture_path = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'qq_sample.txt'
        )

    def test_parses_all_messages(self):
        messages = parse_qq_txt(self.fixture_path)
        self.assertEqual(len(messages), 5)

    def test_extracts_sender_name(self):
        messages = parse_qq_txt(self.fixture_path)
        self.assertEqual(messages[0]['sender'], '姚老师')

    def test_extracts_qq_number(self):
        messages = parse_qq_txt(self.fixture_path)
        self.assertEqual(messages[0]['qq_number'], '12345678')

    def test_filters_by_teacher(self):
        messages = parse_qq_txt(self.fixture_path, teacher_name='姚老师')
        self.assertEqual(len(messages), 3)

    def test_extracts_at_replies(self):
        messages = parse_qq_txt(self.fixture_path)
        # Message from 姚老师 @张小明
        reply_msg = messages[2]
        self.assertEqual(reply_msg['reply_to'], '张小明')

    def test_classifies_messages(self):
        messages = parse_qq_txt(self.fixture_path, teacher_name='姚老师')
        categories = [m['category'] for m in messages]
        self.assertIn('通知', categories)


if __name__ == "__main__":
    unittest.main()
