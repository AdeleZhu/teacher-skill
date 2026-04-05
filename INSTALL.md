# 安装指南

## 安装为 Claude Code Skill

```bash
git clone https://github.com/AdeleZhu/teacher-skill ~/.claude/skills/create-teacher
```

安装后在 Claude Code 中输入 `/create-teacher` 即可开始蒸馏老师。

## 依赖安装（可选）

如果你需要使用自动化采集工具：

```bash
cd ~/.claude/skills/create-teacher
pip install -r requirements.txt
```

Playwright 浏览器驱动（仅飞书浏览器采集需要）：

```bash
playwright install chromium
```

## 平台选择指南

| 数据来源 | 工具 | 需要安装 | 使用方式 |
|----------|------|----------|----------|
| 手动描述 | 无 | 无 | 直接在对话中输入 |
| 微信聊天记录 | wechat_parser | 无 | 导出聊天记录为 txt，传入文件路径 |
| QQ 聊天记录 | qq_parser | 无 | 导出聊天记录为 txt，传入文件路径 |
| 邮件 | email_parser | 无 | 传入 .eml/.mbox/.txt 文件路径 |
| 飞书（有App权限） | feishu_auto_collector | `pip install requests` | 配置 App ID 和 Secret |
| 飞书（无App权限） | feishu_browser | `pip install playwright` | 复用 Chrome 登录状态 |
| 飞书（多维表格） | feishu_mcp_client | `pip install requests` | 配置 App Token |
| 钉钉 | dingtalk_auto_collector | `pip install requests` | 配置 App Key 和 Secret |

## 验证安装

```bash
python3 ~/.claude/skills/create-teacher/tools/skill_writer.py --action list --base-dir ~/.claude/skills/create-teacher/teachers
python3 ~/.claude/skills/create-teacher/tools/wechat_parser.py --help
python3 ~/.claude/skills/create-teacher/tools/qq_parser.py --help
```
