#!/usr/bin/env python3
"""
feishu_parser.py — Parse Feishu (Lark) exported JSON data.

Supports messages and documents exported via feishu_auto_collector.

Usage:
    python3 feishu_parser.py --input feishu_data.json --teacher-name "姚老师"
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from wechat_parser import classify_message


def parse_feishu_json(filepath: str, teacher_name: str | None = None) -> dict:
    """Parse Feishu JSON export.

    Returns dict with 'messages' and 'documents' lists.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = []
    for msg in data.get('messages', []):
        if msg.get('msg_type') != 'text':
            continue

        sender = msg.get('sender', {}).get('name', '')
        content_str = msg.get('body', {}).get('content', '{}')
        try:
            content_data = json.loads(content_str)
            content = content_data.get('text', '')
        except (json.JSONDecodeError, AttributeError):
            content = content_str

        parsed = {
            'timestamp': msg.get('create_time', ''),
            'sender': sender,
            'content': content,
            'category': classify_message(content),
        }
        messages.append(parsed)

    documents = []
    for doc in data.get('documents', []):
        documents.append({
            'title': doc.get('title', ''),
            'owner': doc.get('owner', {}).get('name', ''),
            'content': doc.get('content', ''),
        })

    if teacher_name:
        messages = [m for m in messages if m['sender'] == teacher_name]
        documents = [d for d in documents if d['owner'] == teacher_name]

    return {
        'source': 'feishu',
        'messages': messages,
        'documents': documents,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse Feishu data")
    parser.add_argument("--input", required=True, help="Path to Feishu JSON file")
    parser.add_argument("--teacher-name", help="Filter by teacher name")
    parser.add_argument("--output", help="Output JSON file")

    args = parser.parse_args()
    result = parse_feishu_json(args.input, teacher_name=args.teacher_name)

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
