#!/usr/bin/env python3
"""
feishu_browser.py — Collect Feishu documents and messages via browser automation.

Uses Playwright to control a Chromium browser, reusing an existing Chrome
login session so no credentials are required. Ideal when you don't have
Feishu Open API app permissions but are already logged in via browser.

Requires:
    pip install playwright
    playwright install chromium

Usage:
    python3 feishu_browser.py \\
        --urls "https://xxx.feishu.cn/docs/abc,https://xxx.feishu.cn/messages/def" \\
        --output output.json
"""
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Collect Feishu documents/messages via Playwright browser automation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--urls',
        required=True,
        help='Comma-separated Feishu document or message URLs to collect',
    )
    parser.add_argument(
        '--output',
        default='feishu_browser_output.json',
        help='Output JSON file path (default: feishu_browser_output.json)',
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    urls = [u.strip() for u in args.urls.split(',') if u.strip()]
    print('Not yet implemented. Coming soon.')
    print(f'Would collect {len(urls)} URL(s) via Playwright browser:')
    for url in urls:
        print(f'  - {url}')
    print(f'  output: {args.output}')
    sys.exit(0)


if __name__ == '__main__':
    main()
