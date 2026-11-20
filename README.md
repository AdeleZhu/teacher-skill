[English](./README_EN.md) | 中文

# Teacher Skill — 蒸馏你的老师

<!-- yarkr:badges:start -->
[![Indexed on Yarkr](https://api.yarkr.com/functions/v1/api/api/v1/badges/repos/AdeleZhu/teacher-skill/version.svg)](https://yarkr.com/arks/adelezhu/teacher-skill)
<!-- yarkr:badges:end -->

**把你最喜欢的老师变成 AI，随时随地请 TA 给你讲题。**

你有没有遇到过这样的情况：换了老师之后，新老师讲的你怎么都听不懂？或者毕业了，再也没有人能像那个老师一样给你讲明白？

Teacher Skill 就是为了解决这个问题。它能把一个老师的**教学方式**、**性格特点**和**学科知识**提取出来，生成一个 AI 技能文件。加载之后，AI 就会像你的老师一样跟你互动——用 TA 的口头禅，按 TA 的方式讲题，甚至用 TA 编的口诀帮你记公式。

> 灵感来自 [colleague-skill](https://github.com/titanwings/colleague-skill)（蒸馏同事），我们把同样的思路带到了教育场景。

## 它能做什么？

### 三维度蒸馏

| 维度 | 捕捉什么 | 示例 |
|------|----------|------|
| **教学能力** | 上课流程、出题风格、批改习惯、讲题方式 | "姚老师每次讲新概念前，会先在黑板上写一道生活场景题" |
| **人格特征** | 口头禅、语气、对不同学生的态度、底线 | "当学生说'我不会'时，姚老师会反问'你卡在哪一步了？'" |
| **学科知识** | 讲解路径、记忆口诀、重点难点、知识串联 | "完全平方公式：首平方，尾平方，首尾二倍在中央" |

### 蒸馏后你能得到什么？

一套结构化的老师档案：

```
teachers/yao-laoshi/
├── meta.json          # 老师基本信息
├── teaching.md        # 教学能力（怎么上课、怎么出题、怎么批改）
├── persona.md         # 人格特征（口头禅、态度、5层性格模型）
├── knowledge.md       # 学科知识（口诀、类比、重点难点、知识串联）
├── SKILL.md           # 三合一技能文件（加载这个就行）
├── teaching_skill.md  # 只加载教学维度
├── persona_skill.md   # 只加载人格维度
└── knowledge_skill.md # 只加载知识维度
```

加载 `SKILL.md` 后，AI 会按照三维度协调规则工作：
1. 先用老师的**性格**判断怎么回应你
2. 再用老师的**教学方式**决定怎么讲
3. 最后用老师的**知识库**提供具体内容

## 快速开始

### 安装

```bash
git clone https://github.com/AdeleZhu/teacher-skill ~/.claude/skills/create-teacher
```

### 使用

在 Claude Code 中输入：

```
/create-teacher
```

AI 会引导你完成三轮问答：
1. **基本信息** — 老师叫什么、教什么、教了多少年
2. **教学特点** — 怎么上课、怎么出题、有什么口诀
3. **性格特征** — 口头禅、脾气、对学生的态度

回答完毕，你的 AI 老师就生成了。

### 导入聊天记录（可选）

如果你有老师在群里的聊天记录，可以导入让蒸馏更准确：

```
/create-teacher yao-laoshi
```

支持的数据源：

| 来源 | 说明 |
|------|------|
| 微信 | 导出聊天记录为 txt 文件 |
| QQ | 导出聊天记录为 txt 文件 |
| 钉钉 | 自动采集（需要 App 权限） |
| 飞书 | 自动采集 / 浏览器方式 / MCP 方式 |
| 邮件 | 支持 .eml / .mbox / .txt |

## 示例

项目自带两位示例老师，可以直接体验：

### 姚老师（数学，20年教龄）

> 粉笔字写得像印刷体，讲题从来不直接给答案，非要你自己先试。

- 口头禅："这道题你们再想想"、"不难吧？"
- 讲题方式：先沉默30秒让学生想，再点名回答
- 独门口诀："首平方，尾平方，首尾二倍在中央"
- 知识串联："方程就像一家人——一元一次是小弟，一元二次是大哥"

### 周老师（英语，20年教龄）

> 上课全程英文但学生听不懂时秒切中文，表情特别丰富。

- 口头禅："Come on, try it!"、"Very good! 但是呢…"
- 讲题方式：先表扬再纠正，鼓励开口说
- 独门记忆法："since 像GPS定位，for 像卷尺量长度"
- 知识串联："从句就是大句子里的小句子，记住它们'打工'的位置"

## 管理你的老师

```bash
/list-teachers              # 查看所有已蒸馏的老师
/teacher-rollback yao 1     # 回滚到旧版本
/delete-teacher yao-laoshi  # 删除老师档案
```

老师档案支持**增量更新**——随时补充新素材，AI 会自动合并到已有档案。对话中发现 AI 表现不对，直接说"我们老师不会这么说"，AI 会自动纠正。

## 工作原理

```
学生填写问卷 + 导入聊天记录
        ↓
   ┌────┴────┐────────┐
   ↓         ↓        ↓
教学分析器  人格分析器  知识分析器
   ↓         ↓        ↓
教学构建器  人格构建器  知识构建器
   ↓         ↓        ↓
teaching.md persona.md knowledge.md
   └────┬────┘────────┘
        ↓
     SKILL.md（三合一）
```

**9 个 Prompt 模板** 驱动整个流程：
- `intake.md` — 三轮问卷，含人格标签库和教学风格标签库
- `teaching_analyzer.md` — 7 个学科的专用提取模板
- `persona_analyzer.md` — 5 层人格模型（核心人格→身份→表达→决策→互动→边界）
- `knowledge_analyzer.md` — 提取讲解路径、口诀、重点难点、知识串联
- 3 个 builder — 把分析结果转化为结构化 markdown
- `merger.md` + `correction_handler.md` — 增量更新和纠错

**10 个 Python 工具** 处理数据和文件：
- 4 个聊天记录解析器（微信、QQ、飞书、邮件）
- 飞书自动采集（3种方式）、钉钉自动采集
- 技能文件写入器、版本管理器

## 与 colleague-skill 的区别

| | colleague-skill | teacher-skill |
|---|---|---|
| 蒸馏对象 | 同事 | 老师 |
| 维度 | 2 个（工作 + 人格） | **3 个**（教学 + 人格 + 知识） |
| 数据源 | 飞书、钉钉、Slack | 飞书、钉钉、**QQ、微信** |
| 目标用户 | 职场人 | 学生 |
| 学科适配 | 无 | **7 个学科专用模板** |
| 场景对话 | 5 个职场场景 | **5 个师生场景** |

## 贡献

欢迎贡献！你可以：
- 补充更多学科的专用提取模板
- 优化 prompt 质量
- 添加更多数据源的解析器
- 提交你的示例老师（脱敏后）

## 开源协议

MIT License

<!-- yarkr:install:start -->
## Install with Yarkr

This repo is indexed on [Yarkr](https://yarkr.com/arks/adelezhu/teacher-skill) as the ark [adelezhu/teacher-skill](https://yarkr.com/arks/adelezhu/teacher-skill), so its skills install into Claude Code, Codex, Cursor and other agent harnesses with one command.

### CLI

Install the whole ark, which Yarkr keeps equal to this repo:

```bash
npx yarkr-cli sync adelezhu/teacher-skill
```

Or add individual skills:

```bash
npx yarkr-cli add skill:adelezhu/teacher-skill/create-teacher
```

No Node.js? `curl -fsSL https://yarkr.com/install.sh | sh` (macOS, Linux) or `irm https://yarkr.com/install.ps1 | iex` (Windows PowerShell) installs `yarkr` as a standalone binary; then type `yarkr` in place of `npx yarkr-cli`.

### MCP

Connect your agent to the ark over MCP:

```bash
npx yarkr-cli mcp add adelezhu/teacher-skill
```

Or point any MCP client at `https://api.yarkr.com/functions/v1/api/mcp/o/adelezhu/teacher-skill`.
<!-- yarkr:install:end -->
