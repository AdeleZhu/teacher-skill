# Teacher Skill 设计文档

> 一个开源工具，让学生把老师的教学能力、人格特征和学科知识"蒸馏"成 AI 技能，随时请出你的 AI 老师。

**日期**：2026-04-05
**参照项目**：[colleague-skill](https://github.com/titanwings/colleague-skill)
**分发形式**：独立 GitHub 开源仓库 + Claude Code Skill 插件（`/create-teacher`）
**方案**：参照 colleague-skill 架构从零重写，所有代码和 prompt 原创

---

## 一、项目定位

colleague-skill 让职场人蒸馏同事的工作技能和人格特征。teacher-skill 将同样的思路迁移到教育场景：让初中生蒸馏自己老师的教学能力、人格特征和学科知识，生成可加载的 AI 老师技能文件。

### 与 colleague-skill 的核心区别

| 维度 | colleague-skill | teacher-skill |
|------|----------------|---------------|
| 蒸馏对象 | 同事 | 老师 |
| 蒸馏维度 | 2（work + persona） | 3（teaching + persona + knowledge） |
| 数据源 | 飞书、钉钉、Slack、邮件 | 飞书、钉钉、QQ、微信、邮件 |
| 目标用户 | 职场人 | 学生（初中生为主） |
| 输出文件 | work.md + persona.md | teaching.md + persona.md + knowledge.md |
| 管理命令 | /list-colleagues, /colleague-rollback, /delete-colleague | /list-teachers, /teacher-rollback, /delete-teacher |
| 双语支持 | 自动检测中英文 | 同样支持 |

---

## 二、目录结构

```
teacher-skill/
├── README.md                          # 项目说明（中文为主）
├── README_EN.md                       # English README
├── SKILL.md                           # Skill 格式规范 + Claude Code 入口（含 frontmatter）
├── INSTALL.md                         # 安装指南
├── requirements.txt                   # Python 依赖
├── docs/
│   └── PRD.md                         # 产品规格说明
├── prompts/                           # AI 分析与生成模板
│   ├── intake.md                      # 学生采集问卷
│   ├── teaching_analyzer.md           # 提取教学能力
│   ├── teaching_builder.md            # 生成 teaching.md
│   ├── persona_analyzer.md            # 提取人格特征
│   ├── persona_builder.md             # 生成 persona.md
│   ├── knowledge_analyzer.md          # 提取学科知识
│   ├── knowledge_builder.md           # 生成 knowledge.md
│   ├── merger.md                      # 增量知识合并
│   └── correction_handler.md          # 处理用户纠错
├── tools/                             # Python 工具
│   ├── skill_writer.py                # 写入/更新技能文件
│   ├── version_manager.py             # 版本控制与回滚
│   ├── feishu_auto_collector.py       # 飞书采集
│   ├── feishu_parser.py               # 飞书数据解析
│   ├── feishu_browser.py              # 飞书浏览器自动化采集
│   ├── dingtalk_auto_collector.py     # 钉钉采集
│   ├── feishu_mcp_client.py           # 飞书 MCP 协议客户端
│   ├── wechat_parser.py              # 微信聊天记录解析（新增）
│   ├── qq_parser.py                   # QQ 聊天记录解析（新增）
│   └── email_parser.py               # 邮件解析
├── teachers/                          # 生成的老师档案
│   ├── example_yao_math/              # 示例：姚老师（数学）
│   └── example_zhou_english/          # 示例：周老师（英语）
```

---

## 三、老师档案输出格式

每位老师生成一个目录：

```
teachers/example_yao_math/
├── meta.json              # 元数据
├── teaching.md            # Part A：教学能力
├── persona.md             # Part B：人格特征
├── knowledge.md           # Part C：学科知识
├── SKILL.md               # 三合一技能文件
├── teaching_skill.md      # 独立教学技能文件（可单独加载）
├── persona_skill.md       # 独立人格技能文件（可单独加载）
├── knowledge_skill.md     # 独立知识技能文件（可单独加载）
├── versions/              # 历史版本归档
└── sources/               # 原始素材
```

### meta.json

```json
{
  "name": "姚老师",
  "slug": "yao-laoshi",
  "version": 1,
  "created_at": "2026-04-05T10:00:00Z",
  "updated_at": "2026-04-05T10:00:00Z",
  "profile": {
    "school": "",
    "subject": "数学",
    "grade": "初二",
    "role": "数学老师",
    "gender": "female",
    "teaching_years": 20,
    "mbti": ""
  },
  "tags": {
    "personality": [],
    "teaching": []
  },
  "impression": "",
  "knowledge_sources": [],
  "corrections_count": 0
}
```

profile 字段对比 colleague-skill：`company/department/level` → `school/subject/grade/teaching_years`。

### teaching.md（Part A — 对标 work.md）

五个章节：

1. **教学范围** — 科目、年级、负责模块
2. **教学风格** — 板书/PPT、互动程度、节奏快慢、课堂习惯
3. **教学流程** — 导入→讲授→练习→总结的具体习惯
4. **出题与批改** — 出题偏好、批改风格、考试侧重点
5. **教学经验** — 常见易错点的独特讲法、踩坑提醒

要求：提取**具体行为**而非笼统标签（"每节课前5分钟复习"而非"注重复习"）。

### persona.md（Part B — 5 层人格模型）

复用 colleague-skill 的 5 层模型，场景词替换：

- **Layer 0：核心人格** — 最高优先级，不可违反的特质
- **Layer 1：身份认同** — 角色、MBTI、学校文化影响
- **Layer 2：表达风格** — 口头禅、用词、句式、emoji 习惯
- **Layer 3：决策框架** — 优先级排序（如：课堂纪律 > 教学进度 > 学生情绪）
- **Layer 4：师生互动** — 对优等生/中等生/后进生的不同态度（对标原项目的上级/同事/下属）
- **Layer 5：边界** — 不能接受的行为、拒绝模式

每层要求有具体的 if-then 行为规则。

### knowledge.md（Part C — 全新维度）

四个章节：

1. **知识讲解路径** — 老师讲某个知识点的顺序和逻辑
2. **记忆口诀与类比** — 老师的独门记忆法、生活类比、金句
3. **重点难点标注** — 易错点、难点、老师的特殊应对方法
4. **知识串联** — 老师怎么把不同知识点连起来讲

### SKILL.md（三合一）

合并 teaching.md + persona.md + knowledge.md，顶部注入优先级规则和三维度运行时协调逻辑：

> Layer 0 人格规则优先级最高，不可违反。教学风格次之。学科知识为辅助素材。

**三维度运行时协调规则**（对标原项目的 persona 判断 → work 执行）：

1. **Part B（persona）先判断**：这个老师会接受这个问题吗？以什么态度回应？
2. **Part A（teaching）决定方法**：用什么教学方式来讲？按什么流程引导？
3. **Part C（knowledge）提供内容**：调用老师的知识讲解路径、口诀、类比
4. **输出时保持 Part B 的表达风格**：用老师的口头禅和语气输出

### 独立维度技能文件

除了合并的 SKILL.md，还生成三个独立的技能文件（对标原项目的 `work_skill.md` 和 `persona_skill.md`）：

- `teaching_skill.md` — 只加载教学能力，适合"我想让 AI 用这个老师的方式出题"
- `persona_skill.md` — 只加载人格特征，适合"我想让 AI 用这个老师的语气跟我聊天"
- `knowledge_skill.md` — 只加载学科知识，适合"我想复习这个老师讲过的知识点"

---

## 四、Prompts 设计

共 9 个 prompt 文件：

### 4.1 intake.md — 学生采集问卷

分三轮引导学生描述老师：

**第一轮：基本信息**
- 老师姓名、科目、年级、学校
- 教龄、性别、是否班主任
- MBTI（可选）
- 一句话印象

**Slug 生成规则**：中文名用 pypinyin 转拼音，空格用 `-` 连接。如"姚雪梅" → `yao-xuemei`。

**人格标签库**（学生选择，多选）：

| 分类 | 标签 |
|------|------|
| 教学态度 | 严格认真、随和佛系、因材施教、一视同仁、急性子、慢工出细活 |
| 沟通风格 | 幽默风趣、严肃正经、苦口婆心、言简意赅、爱讲故事、爱举例子 |
| 管理风格 | 铁面无私、恩威并施、民主型、放养型、事无巨细、抓大放小 |
| 情绪风格 | 喜怒不形于色、情绪外露、暴脾气、永远温柔、阴晴不定 |
| 特殊标签 | 偏心、拖堂王、作业狂魔、段子手、知心姐姐/大哥、考试机器 |

**教学风格标签库**：

| 分类 | 标签 |
|------|------|
| 授课方式 | 板书派、PPT派、互动派、实验派、讨论派、题海派 |
| 节奏特点 | 快节奏、慢讲细磨、前松后紧、节奏稳定 |
| 重点风格 | 反复强调重点、一笔带过、画重点狂魔、从不划重点 |

每个标签映射到具体行为规则，在 persona_analyzer 和 teaching_analyzer 中使用。

**确认摘要格式**：采集完成后展示结构化摘要供学生确认。

**第二轮：教学能力采集**
- 老师上课的典型流程
- 最常用的教学方法
- 出题和批改风格
- 讲题的独特方式
- 口诀、类比、金句

**第三轮：人格特征采集**
- 口头禅
- 生气/高兴时的表现
- 对不同学生的态度差异
- 最不能接受学生做什么
- 一件印象深刻的事

### 4.2 teaching_analyzer.md — 教学能力分析器

- 输入：学生回答 + 导入的聊天记录/文档
- 输出：结构化教学能力要点
- 分析逻辑：提取具体行为、区分高频/偶尔行为、标记缺失维度

**内容权重优先级**：
1. 老师亲自写的文档/教案（最高权重）
2. 老师的答疑回复、批改评语
3. 老师在群里发的通知、作业布置
4. 日常闲聊消息（最低权重）

**学科专用提取模板**（对标原项目的岗位专用模板）：

| 学科 | 专用提取维度 |
|------|-------------|
| 数学 | 证明方法偏好、计算技巧、几何辅助线套路、公式推导 vs 直接记忆 |
| 英语 | 语法讲解方式、单词记忆法、阅读理解解题策略、口语训练方式 |
| 语文 | 阅读赏析方法、作文结构教学、文言文翻译技巧、诗词背诵策略 |
| 物理 | 实验教学方式、公式推导偏好、生活类比、受力分析方法 |
| 化学 | 实验演示风格、方程式记忆法、元素周期表教学、实验安全强调 |
| 历史 | 时间线教学法、因果链分析、历史人物评价方式、横向对比 |
| 生物 | 图解教学、实验观察引导、知识分类方法、生活联系 |

未匹配学科使用通用模板。

**素材不足标记**：每个维度如果证据不足，标记为 `(素材不足，建议补充相关材料)`。

### 4.3 teaching_builder.md — 生成 teaching.md

- 输入：分析器的结构化要点
- 输出：按五章节格式生成 teaching.md

**底部附加使用说明**（对标原项目 work_builder 的 usage instructions）：
```
- 学生问作业 → 按"教学流程"的讲题习惯引导
- 学生要复习 → 按"教学经验"中的重点难点梳理
- 学生做练习 → 按"出题与批改"的风格出题
- 学生问概念 → 按"教学风格"的方式讲解
```

**内容质量标准**：
- BAD: "姚老师讲课很认真"
- GOOD: "姚老师每次讲新概念前，会先在黑板左上角写一道生活场景题，让学生先试着列式"

### 4.4 persona_analyzer.md — 人格分析器

复用 colleague-skill 的 5 层分析逻辑，场景词替换：
- "上级/同事/下属" → "校长/同事老师/学生/家长"
- "需求评审/代码审查" → "课堂管理/作业批改/考试/家长会"

### 4.5 persona_builder.md — 生成 persona.md

按 Layer 0-5 格式生成。

**场景对话示例**（对标原项目的 5 个场景）：生成时必须包含 5 个典型师生场景的模拟对话：
1. 学生回答问题答错了
2. 学生上课迟到
3. 学生说"老师我不会"
4. 家长在群里质疑教学方式
5. 学生考试进步很大

**Layer 0 质量标准**：
- BAD: "姚老师性格很严格"
- GOOD: "当学生说'我不会'时，姚老师不会直接给答案，而是反问'你卡在哪一步了？把你试过的写出来'"

### 4.6 knowledge_analyzer.md — 学科知识分析器（全新）

- 输入：学生描述 + 课堂笔记 + 聊天记录中的答疑
- 输出：结构化知识点讲解图谱
- 分析逻辑：提取讲解路径、口诀/类比/金句、重点难点和易错点、知识串联关系

### 4.7 knowledge_builder.md — 生成 knowledge.md

按四章节格式生成。

### 4.8 merger.md — 增量合并

基于 colleague-skill 逻辑，扩展为三维分类：
- 新素材 → **三维分类**到 teaching / persona / knowledge（原项目只分 work/persona 两类）
- 检测冲突 → 生成补丁 → 用户确认 → 应用更新

**4 步结构化补丁格式**：
1. 分类判断（teaching / persona / knowledge）
2. 冲突检查（与现有内容对比）
3. 定向补丁（指明具体章节）
4. 摘要 + 版本号递增

**冲突解决选项**：保留现有 / 用新内容替换 / 两者都保留（加时间戳）

### 4.9 correction_handler.md — 纠错处理

- 识别对话中的纠错意图（"我们姚老师不会这么说"）
- 定位到具体段落
- 检测与现有规则是否矛盾，有矛盾时请用户确认
- 生成修正补丁 → 自动归档旧版本

**纠错上限**：每个文件最多 50 条纠错。超过时自动合并语义相近的条目，并通知用户合并了多少条。

---

## 五、Tools 工具层

| 文件 | 功能 | 来源 |
|------|------|------|
| `skill_writer.py` | 写入/更新 teaching.md、persona.md、knowledge.md、SKILL.md | 改写 |
| `version_manager.py` | 版本归档（保留最近10个版本）、回滚 | 复用逻辑 |
| `feishu_auto_collector.py` | 飞书消息/文档/知识库采集 | 保留 |
| `feishu_parser.py` | 飞书数据解析 | 保留 |
| `feishu_browser.py` | 飞书浏览器自动化采集 | 保留 |
| `feishu_mcp_client.py` | 飞书 MCP 协议客户端（App Token API） | 保留 |
| `dingtalk_auto_collector.py` | 钉钉消息/文档采集 | 保留 |
| `wechat_parser.py` | 微信聊天记录解析 | **新增** |
| `qq_parser.py` | QQ 聊天记录解析 | **新增** |
| `email_parser.py` | 邮件解析（EML/MBOX/TXT） | 保留 |

### wechat_parser.py（新增）

- 导入微信聊天记录导出文件（微信"迁移与备份"导出，或第三方工具导出为 txt/html）
- 解析消息格式，过滤出老师发的消息
- 按消息长度和内容分类：闲聊、通知、答疑、知识讲解
- 答疑和知识讲解类消息权重最高

### qq_parser.py（新增）

- 解析 QQ 导出的文本格式（`日期 时间 昵称(QQ号)` 开头）
- 过滤出老师消息，按内容分类
- 处理 QQ 群消息中的 @回复关系，保留上下文

### skill_writer.py 改动

从两个写入函数变成四个：
- `write_teaching()` → 生成 teaching.md
- `write_persona()` → 生成 persona.md
- `write_knowledge()` → 生成 knowledge.md
- `write_skill()` → 合并三文件生成 SKILL.md
- `write_standalone_skills()` → 生成独立的 teaching_skill.md、persona_skill.md、knowledge_skill.md

### 依赖（requirements.txt）

```
requests>=2.28.0           # HTTP 客户端
pypinyin>=0.48.0           # 中文名转拼音 slug
playwright>=1.40.0         # 飞书浏览器采集（可选）
```

QQ 和微信解析器纯文本处理，无额外依赖。

---

## 六、安装与使用

### 根目录 SKILL.md Frontmatter

```yaml
---
name: create-teacher
description: 蒸馏老师的教学能力、人格特征和学科知识，生成 AI 老师技能
argument-hint: "[teacher-name-or-slug]"
allowed-tools: Read, Write, Edit, Bash
---
```

所有工具路径使用 `${CLAUDE_SKILL_DIR}/tools/...` 确保可移植性。

自动检测用户语言：从第一条消息判断中文或英文，全程使用对应语言。

### 管理命令

| 命令 | 功能 |
|------|------|
| `/create-teacher` | 创建新的老师技能 |
| `/create-teacher [slug]` | 对已有老师追加素材 |
| `/list-teachers` | 列出所有已蒸馏的老师 |
| `/teacher-rollback {slug} {version}` | 回滚到指定版本 |
| `/delete-teacher {slug}` | 删除老师档案 |

### 触发词检测

进入增量更新模式的触发词：
- "我有新的资料" / "补充一下" / "追加"
- "不对" / "TA 不会这么说" / "改一下"
- `/update-teacher {slug}`

### 安装为 Claude Code Skill

```bash
git clone https://github.com/<username>/teacher-skill ~/.claude/skills/create-teacher
```

### 使用流程

```
学生安装 teacher-skill
        ↓
输入 /create-teacher
        ↓
AI 引导填写基本信息（姚老师、数学、初二…）
        ↓
AI 逐步提问教学风格、人格、知识点
        ↓
可选：导入钉钉/飞书/QQ/微信聊天记录
        ↓
AI 生成 teaching.md + persona.md + knowledge.md
        ↓
学生确认，生成 SKILL.md
        ↓
之后随时追加素材（merger.md）或纠错（correction_handler.md）
```

### 生成的 AI 老师用途

加载 SKILL.md 到 Claude Code 或其他 AI 工具后：
- **问作业**：AI 用老师的方式讲题
- **复习**：AI 按老师的知识串联逻辑帮你复习
- **模拟课堂**：AI 用老师的口头禅、语气、教学节奏互动

---

## 七、示例老师

| 示例 | 目录 | 科目 | 性别 | 教龄 |
|------|------|------|------|------|
| 姚老师 | `teachers/example_yao_math/` | 数学 | 女 | 20年 |
| 周老师 | `teachers/example_zhou_english/` | 英语 | 女 | 20年 |

示例应包含完整的 teaching.md + persona.md + knowledge.md + SKILL.md，质量对标 colleague-skill 的 example_tianyi（persona.md 约 180 行，含 5 个场景对话）。

---

## 八、系统约束

| 约束项 | 限制值 |
|--------|--------|
| 单个 PDF 文件大小 | 10MB |
| 单次会话最多导入 PDF | 10 个 |
| 纠错上限（每文件） | 50 条，超过自动合并 |
| 版本归档上限 | 保留最近 10 个版本 |
| Word/Excel 文件 | 需手动转为 PDF 或文本后导入 |

---

## 九、实现优先级

| 优先级 | 内容 | 说明 |
|--------|------|------|
| **P0（MVP）** | 主流程 + 9 个 prompts + skill_writer + 手动输入 | 核心蒸馏能力，无需任何采集工具即可用 |
| **P1** | feishu_parser + email_parser + wechat_parser + qq_parser | 数据导入能力 |
| **P2** | correction_handler + merger + version_manager | 增量演化能力 |
| **P3** | feishu_auto_collector + feishu_browser + feishu_mcp_client + dingtalk_auto_collector | 自动化采集能力 |
| **P3** | 管理命令（list/rollback/delete） | 档案管理 |

---

## 十、Git 配置

- 用户名：AdeleZhu
- 邮箱：arthurzhu85@gmail.com
