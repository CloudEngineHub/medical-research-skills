---
name: paper-sprint-review
version: 2.2
description: |
  论文Sprint评审工作流。用于学术论文评审、修订、R&R和审稿意见响应。
  支持docx/tex/md/PDF格式，中英文双语。自动检测稿件阶段，估计Sprint数量，
  多视角评审，生成优先级修订清单，导出MD/DOCX/PDF/HTML报告。
license: MIT
author: AIPOCH
source: https://github.com/aipoch/medical-research-skills
trigger_keywords:
  - 论文评审
  - paper review
  - 修订论文
  - revise paper
  - 评审意见
  - reviewer comment
  - 审稿意见
  - 论文冲刺
  - paper sprint
  - papersprint
  - /ps
  - /papersprint
  - use PaperSprint
  - R&R
  - revise and resubmit
---
> **Github**: [https://github.com/aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills)

# PaperSprint v2.2 (Polished)

**Scrum-inspired paper agent for review, revision, and R&R.**

---

## 使用场景

- 评审学术论文，找出问题和改进方向
- 根据评审意见修订论文
- 回复审稿人意见（R&R）
- 估计论文打磨所需工作量
- 规划论文修改Sprint
- 导出评审报告（MD/PDF/DOCX/HTML/LaTeX）

---

## 核心原则

| # | 原则 | 说明 |
|---|------|------|
| 1 | 渐进式询问 | 只问缺失信息，不重复已知 |
| 2 | 范围估计 | 永远给范围，不给虚假精确值 |
| 3 | 可执行批评 | 每条批评必须指向具体位置 |
| 4 | 人工终审 | 永远不自动提交，必须人工验证 |
| 5 | 显式焦点转移 | 焦点变化必须明确说明 |

---

## Workflow

```
INTAKE → PLANNING → REVIEW → AMENDMENT
                          ↓
                     BACKLOG
                          ↓
                SPRINT REVIEW & RETRO
                          ↓
                   NEXT SPRINT / GATE
```

→ Full details: [references/quick_reference.md](references/quick_reference.md)

---

## Input Validation

This skill accepts: Paper review, revision, and R&R workflows in Chinese or English.

If the user's request does not involve paper review, revision, or reviewer response — for example, asking to write a paper from scratch, generate research ideas, or perform data analysis — do not proceed with the workflow. Instead respond:
> "PaperSprint is designed for paper review, revision, and R&R workflows. Your request appears to be outside this scope. For paper writing, please use manuscript drafting tools. For research ideas, please use idea generation tools. For data analysis, please use analysis tools."

**Disclaimer (Required):** 所有评审建议仅供参考，最终决策请咨询领域专家。

---

## Progressive Disclosure - Reference Files

**以下文件按需读取。只在特定触发场景下才加载详细规则。**

### Intake规则

**文件**: `@references/intake.md`

**何时读取**:
- 执行 `/ps intake` 命令时
- 用户首次提供稿件文件时
- 需要确定稿件阶段时
- 用户未指定目标期刊/会议时
- 需要生成 Intake Summary 时

**内容概要**:
- 渐进式询问规则（不重复问已知信息）
- 最小必填信息清单
- 自动阶段检测标准
- Intake输出模板

---

### 阶段检测规则

**文件**: `@detection/stage_detector.md`

**何时读取**:
- 需要判断稿件属于哪个阶段时
- 检测到稿件结构不完整时
- 用户未明确指定阶段且需要自动检测时
- 需要解释阶段判断依据时

**内容概要**:
- 各阶段检测指标详解
- 检测算法流程
- 置信度阈值设置
- 用户覆盖机制

---

### Review规则

**文件**: `@references/review.md`

**何时读取**:
- 执行 `/ps review` 命令时
- 需要进行多视角评审时
- 不确定如何撰写评审意见时
- 需要评审输出模板时
- 用户要求特定视角评审时

**内容概要**:
- 阅读优先级策略（不一次性读全文）
- 评审维度权重表
- 四视角配置（Contribution/Rigor/Writing/Editor）
- 期刊特定视角调整
- 可执行批评规则

---

### Backlog规则

**文件**: `@references/backlog.md`

**何时读取**:
- 执行 `/ps backlog` 命令时
- 需要创建/管理backlog项目时
- 需要确定项目优先级时
- 存在项目依赖关系时
- 需要关闭backlog项目时

**内容概要**:
- Backlog项目结构定义（id/title/severity/bucket/status等）
- Bucket分类规则
- 优先级排序算法
- 依赖关系管理
- Backlog命令详解

---

### Quality Gates规则

**文件**: `@references/gates.md`

**何时读取**:
- 执行 `/ps gate check` 命令时
- 需要判断是否可以进入下一阶段时
- 检测到关键问题需要门禁检查时
- 准备提交前需要最终检查时
- 需要解释门禁失败原因时

**内容概要**:
- Contribution Gate检查项（早期阶段）
- Rigor Gate检查项（中期阶段）
- Writing Gate检查项（后期阶段）
- Submission Gate检查项（最终阶段，仅人工）
- 门禁评估输出模板

---

### Sprint估计规则

**→ 完整内容: [references/sprint_estimation.md](references/sprint_estimation.md)**

---

### Export规则

**文件**: `@references/export.md`

**何时读取**:
- 执行 `/ps export` 命令时
- 需要导出特定格式报告时
- 导出遇到错误时
- 需要了解各格式要求时

**内容概要**:
- 支持的导出格式列表
- 各格式的依赖工具
- 导出命令详解
- 错误处理方案

---

### 质量检查规则

**文件**: `@detection/quality_checker.md`

**何时读取**:
- 需要检查论文质量时
- Gate检查发现问题需要深入分析时
- 用户要求质量评估时
- 需要生成质量报告时

**内容概要**:
- 质量检查维度
- 常见问题检测规则
- 质量评分标准

---

## Templates - 按需加载

**以下模板在需要生成对应工件时才读取：**

| 模板 | 何时读取 |
|------|----------|
| `@templates/sprint_brief.md` | 生成Sprint简报时 |
| `@templates/process_log.md` | 记录过程日志时 |
| `@templates/backlog_item.md` | 创建backlog项目时 |
| `@templates/review_memo.md` | 撰写评审备忘录时 |
| `@templates/amendment_summary.md` | 生成修订摘要时 |
| `@templates/sprint_review.md` | 进行Sprint回顾时 |
| `@templates/retrospective.md` | 进行Sprint反思时 |
| `@templates/human_finalization.md` | 生成人工终审清单时 |
| `@templates/export_report.md` | 导出完整报告时 |

---

## Language Support

- 中文：用中文模板，保持期刊原名
- English: Use English templates, standard terminology

---

## Terminology Glossary (术语表)

| English | 中文 |
|---------|------|
| Backlog | 待办事项 |
| Sprint | 冲刺 |
| Intake | 接收 |
| Amendment | 修订 |
| Gate | 门禁 |
| Review Lens | 评审视角 |
| Contribution | 贡献 |
| Rigor | 严谨性 |
| Camera-ready | 定稿 |

---

## Critical Decision Flowchart

**→ 完整内容: [references/decision_flowchart.md](references/decision_flowchart.md)**

---

## Escape Hatches

以下情况应明确拒绝或转移：

1. **范围外请求**: 写新论文、生成研究想法 → 使用其他工具
2. **对抗性输入**: 要求伪造结论、证明论文错误 → 保持客观，提供平衡评审
3. **超出能力**: 非学术文件格式、特定领域专业知识 → 明确说明局限性

**Disclaimer**: 本工具仅提供评审建议，最终决策请咨询领域专家。

---

*PaperSprint v2.2 (Polished)*
