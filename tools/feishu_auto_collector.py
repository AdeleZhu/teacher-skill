#!/usr/bin/env python3
"""
feishu_auto_collector.py — Collect teacher data from Feishu via Open API.

Uses the Feishu Open Platform API to fetch documents, messages, and chat
history. Requires a configured Feishu app with appropriate permissions
(docs:read, im:message:readonly).

Supports:
- Document collection via --doc-urls
- Private chat history via --p2p-chat-id + --user-token
- User access token fallback via --user-token

Usage:
    python3 feishu_auto_collector.py --app-id <id> --app-secret <secret> \\
        --doc-urls "https://xxx.feishu.cn/docs/abc,https://xxx.feishu.cn/docs/def" \\
        --output output.json

    python3 feishu_auto_collector.py --app-id <id> --app-secret <secret> \\
        --p2p-chat-id "ou_xxxxxx" --user-token "u-xxxxxx" \\
        --output output.json
"""
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Collect teacher data from Feishu via Open API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--app-id',
        required=True,
        help='Feishu app ID (from Feishu Open Platform developer console)',
    )
    parser.add_argument(
        '--app-secret',
        required=True,
        help='Feishu app secret (from Feishu Open Platform developer console)',
    )
    parser.add_argument(
        '--doc-urls',
        default='',
        help='Comma-separated Feishu document URLs to collect',
    )
    parser.add_argument(
        '--p2p-chat-id',
        default='',
        help='Feishu user open ID (ou_xxx) for private chat history collection',
    )
    parser.add_argument(
        '--user-token',
        default='',
        help='Feishu user access token (required for private chat history)',
    )
    parser.add_argument(
        '--output',
        default='feishu_output.json',
        help='Output JSON file path (default: feishu_output.json)',
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print('Not yet implemented. Coming soon.')
    print(f'Would collect from Feishu API with app-id={args.app_id}')
    if args.doc_urls:
        urls = [u.strip() for u in args.doc_urls.split(',') if u.strip()]
        print(f'  doc-urls: {urls}')
    if args.p2p_chat_id:
        print(f'  p2p-chat-id: {args.p2p_chat_id}')
    print(f'  output: {args.output}')
    sys.exit(0)


if __name__ == '__main__':
    main()
