#!/usr/bin/env python3
"""
qq_parser.py — Parse QQ exported chat logs.

Supports the standard QQ txt export format:
    2026-03-15 09:00:01 昵称(QQ号)
    消息内容

Usage:
    python3 qq_parser.py --input chat.txt --teacher-name "姚老师"
"""
import argparse
import json
import re
import sys

# Import classify_message from wechat_parser (shared logic)
import os
sys.path.insert(0, os.path.dirname(__file__))
from wechat_parser import classify_message

# Pattern: "2026-03-15 09:00:01 姚老师(12345678)"
QQ_MSG_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)\((\d+)\)$'
)

# Pattern for @replies
AT_PATTERN = re.compile(r'^@(\S+)\s+')


def parse_qq_txt(filepath: str, teacher_name: str | None = None) -> list[dict]:
    """Parse a QQ txt export file into structured messages.

    Args:
        filepath: Path to the exported txt file.
        teacher_name: If provided, only return messages from this sender.

    Returns:
        List of message dicts with keys: timestamp, sender, qq_number, content,
        category, reply_to.
    """
    messages = []
    current_msg = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                if current_msg is not None:
                    messages.append(current_msg)
                    current_msg = None
                continue

            match = QQ_MSG_PATTERN.match(line)
            if match:
                if current_msg is not None:
                    messages.append(current_msg)
                current_msg = {
                    'timestamp': match.group(1),
                    'sender': match.group(2),
                    'qq_number': match.group(3),
                    'content': '',
                    'reply_to': None,
                }
            elif current_msg is not None:
                if current_msg['content']:
                    current_msg['content'] += '\n' + line
                else:
                    current_msg['content'] = line
                    # Check for @reply
                    at_match = AT_PATTERN.match(line)
                    if at_match:
                        current_msg['reply_to'] = at_match.group(1)

        if current_msg is not None:
            messages.append(current_msg)

    # Classify messages
    for msg in messages:
        msg['category'] = classify_message(msg['content'])

    # Filter by teacher
    if teacher_name:
        messages = [m for m in messages if m['sender'] == teacher_name]

    return messages


def main():
    parser = argparse.ArgumentParser(description="Parse QQ chat logs")
    parser.add_argument("--input", required=True, help="Path to exported txt file")
    parser.add_argument("--teacher-name", help="Filter by teacher name")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")

    args = parser.parse_args()
    messages = parse_qq_txt(args.input, teacher_name=args.teacher_name)

    result = {
        "source": "qq",
        "file": args.input,
        "teacher_filter": args.teacher_name,
        "total_messages": len(messages),
        "by_category": {},
        "messages": messages,
    }

    for msg in messages:
        cat = msg['category']
        result['by_category'][cat] = result['by_category'].get(cat, 0) + 1

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Saved {len(messages)} messages to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
