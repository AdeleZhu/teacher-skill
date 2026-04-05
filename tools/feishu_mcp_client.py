#!/usr/bin/env python3
"""
feishu_mcp_client.py — Collect teacher data from Feishu Bitable via MCP protocol.

Uses the Model Context Protocol (MCP) to connect to a Feishu Bitable
(多维表格) and export structured records. Suitable for teams that maintain
teacher observation records or feedback databases in Feishu Bitable.

Requires:
    pip install requests

Usage:
    python3 feishu_mcp_client.py \\
        --app-token "bascn4ecqxxxxxxxx" \\
        --table-id "tblxxxxxxxx" \\
        --output output.json
"""
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Collect teacher data from Feishu Bitable via MCP protocol.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--app-token',
        required=True,
        help='Feishu Bitable app token (bascnXXX format, from bitable URL)',
    )
    parser.add_argument(
        '--table-id',
        required=True,
        help='Feishu Bitable table ID (tblXXX format, from bitable URL)',
    )
    parser.add_argument(
        '--output',
        default='feishu_mcp_output.json',
        help='Output JSON file path (default: feishu_mcp_output.json)',
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print('Not yet implemented. Coming soon.')
    print(f'Would collect from Feishu Bitable via MCP:')
    print(f'  app-token: {args.app_token}')
    print(f'  table-id: {args.table_id}')
    print(f'  output: {args.output}')
    sys.exit(0)


if __name__ == '__main__':
    main()
