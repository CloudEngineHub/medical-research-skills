<div align="center">

# AIPOCH Medical Research Skills

Add Skills. Run Your Research.

<br>

[![License](https://img.shields.io/badge/License-MIT-ff6b6b?style=for-the-badge)](./LICENSE)
![Skills Count](https://img.shields.io/badge/Skills-200%2B-4dabf7?style=for-the-badge)
![Work%20with](https://img.shields.io/badge/Work%20with-OpenClaw%20%7C%20Opencode%20%7C%20Claude-9775fa?style=for-the-badge)
[![Follow on X](https://img.shields.io/badge/Follow%20on%20X-%40aipoch__ai-212529?style=for-the-badge&logo=x&logoColor=white)](https://x.com/aipoch_ai)
[![YouTube](https://img.shields.io/badge/YouTube-%40AIPOCH__AI-ff0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@AIPOCH_AI)

<br>

<p align="center">
  <a href="https://www.aipoch.com/">
    <img src="https://github.com/user-attachments/assets/1a6a7005-d9fc-49d5-8dba-3cb822d7e71d" alt="AIPOCH Demo GIF" width="800"/>
  </a>
</p>

<br>

*450+ medical research skills · Evidence Insights · Protocol Design · Data Analysis · Academic Writing*

</div>

---

## 🤔 What it is?

AIPOCH is a curated library of 450+ Medical Research Agent Skills, built to work with**​ OpenClaw** and other AI agent platforms, including​**​ OpenCode and Claude**​.

It supports the research workflow across four core areas: Evidence Insights, Protocol Design, Data Analysis, and Academic Writing.

Equip your AI agent with Medical Research Skills, and turn it into a capable medical research assistant.

AIPOCH also introduces **Medical ​Skill Auditor (in development) ​**​— a structured evaluation framework designed to score and validate skills, bringing measurable quality standards to the ecosystem.  [View evaluation report example here. ](https://www.aipoch.com/agent-skills/medical-research-literature-reader-pro/eval-result)

> ⭐ If you find this repository useful, consider giving it a star! It helps more researchers discover Medical Research Agent Skills and supports the continued development of this library.

---

## 🗂️ Skills Overview

All skills in AIPOCH are ​**originally designed and developed in-house**​, built to reflect medical research workflows and standards.

The library is primarily organized into five categories: ​**Evidence Insights, Protocol Design, ​Data Analysis,  Academic Writing**​, and Others.

| 📚**Category** | **Highlights**                                                                                                                        |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
|🔍 **Evidence Insight**   | e.g., search strategy design, database selection, evidence-level prioritization, critical appraisal, literature synthesis and gap identification.|
| 🧪 **Protocol Design**    |e.g., experimental design generation, study type selection, causal inference planning, statistical power calculation, validation strategy.        |
|📊 **Data Analysis**      | e.g., R/Python bioinformatics code generation, statistical modeling, data cleaning pipelines, machine learning workflows, result visualization.  |
|✍️ **Academic Writing**   |  e.g., SCI manuscript drafting, methods/results/discussion writing, meta-analysis narrative, cover letters, abstract generation.|
| 🌍 **Other (General / Non-Research)**          | all general skills that do not fall into categories 1–4.                                                                                   |

**📌 Total Skills in Library: 454 and growing**

## 🎬 AIPOCH Medical Research Skills — Demo

<p align="center">
  <a href="https://www.youtube.com/watch?v=Pq4E9mCO1t8" target="_blank">
<img width="4480" height="2516" alt="medical research literature reader pro" src="https://github.com/user-attachments/assets/c3de83ec-43d8-4c37-8079-6354c138b0fa" />
  </a>
</p>

<p align="center">
A brief showcase of AIPOCH Medical Research Skills in action across research workflows.
</p>

## 🚀 How to Start?

### ⚙️ Requirements

​**Host Platform**​: **OpenClaw (installed and running)** or any compatible AI Agent framework that supports Skill integration.

If you don't have OpenClaw,[ please follow the official OpenClaw setup guide.](https://github.com/openclaw/openclaw)

​**Git**​: Required for cloning the repository. [Git LFS](https://git-lfs.com/)

### 🦞 Connect with OpenClaw

#### **Method 1:**

**I'm a human**

```markdown
Read https://aipoch.com/skill.md and follow the instructions to join Aipoch
```

1. Run the command to initialize setup
2. Select 'OpenClaw' as your target agent
3. Follow the prompts to link your library

**I'm an agent**

```markdown
curl -sL https://aipoch.com/skill.md > ./skills/aipoch.md
```

1. Download the integration guide
2. Manually configure your agent's skill path
3. Verify the connection in your dashboard

---

#### **Method 2:**

**🦞 Install into OpenClaw Plug-in**

[OpenClaw](https://openclaw.ai) is a self-hosted AI agent gateway. You can install all AIPOCH skills into OpenClaw with a single command.

**macOS / Linux / WSL:**

```bash
bash <(curl -s https://raw.githubusercontent.com/aipoch/medical-research-skills/main/scientific-skills/scripts/openclaw-install.sh)
```

**Windows (Git Bash):**

```bash
curl -s https://raw.githubusercontent.com/aipoch/medical-research-skills/main/scientific-skills/scripts/openclaw-install.sh -o /tmp/install.sh
bash /tmp/install.sh
```

The script will:

1. Clone this repository into a temporary directory
2. Copy all `SKILL.md` skill folders into `~/.openclaw/skills/`
3. Skip any skills that are already installed

After installation, restart your gateway to pick up the new skills:

```bash
openclaw gateway restart
```

> **Tip:** Run with `--dry-run` first to preview what will be installed without making any changes.
> 
> ```bash
> bash <(curl -s https://raw.githubusercontent.com/aipoch/medical-research-skills/main/scientific-skills/scripts/openclaw-install.sh) --dry-run
> ```

> **Note:** Skills are installed to `~/.openclaw/skills/` by default (visible to all agents). To install into a specific workspace instead, set the environment variable before running:
> 
> ```bash
> OPENCLAW_SKILLS_DIR=~/.openclaw/workspace/skills bash <(curl -s https://raw.githubusercontent.com/aipoch/medical-research-skills/main/scientific-skills/scripts/openclaw-install.sh)
> ```

---



## 🧠 AIPOCH Medical Skill Auditor (in development)

### 🧩**What is Medical Skill Auditor?**

Skill Auditor is AIPOCH’s evaluation framework under active development for scoring Medical Research Agent Skills with ​**rigorous, multi‑dimensional quality metrics**​. It’s intended to go beyond static descriptions by measuring both **core capability** and ​**real execution performance**​—giving users and developers a clearer, data‑driven understanding of skill quality.

### ⚙️**How does it work?**

#### 🧰 **Core Capability**

Evaluates a skill’s design and contract against key dimensions such as **Functional Suitability​, reliability, performance & context, Agent Usability, human usability, Security, Agent-Specific and maintainability**​.

#### 📊 **Medical Task**

Assesses actual outputs of a skill with layered criteria, weighting general competence and category‑specific behaviors to reflect real‑world execution quality.

#### 🚫**Veto​ Gates**

To enforce strict quality control, Skill Auditor is designed with two layers of ​**veto mechanisms**​. Any failure in these checks may lead to immediate rejection of a skill.

##### **Skill ​Veto**

- Operational Stability
- Structural Consistency
- Result Determinism
- System Security

##### **Research ​Veto**

- Scientific Integrity
- Practice Boundaries
- Methodological Ground
- Code Usability

### 👥**Who can use it?**

You can already view [evaluation results for selected AIPOCH skills on the website](https://www.aipoch.com/agent-skills/medical-research-literature-reader-pro/eval-result). In the future, Skill Auditor will extend to evaluate third-party skills, enabling a unified and transparent scoring system across the ecosystem.

### 💡**Why it matters?**

By systematically quantifying how well a skill performs in practice and in design, Skill Auditor will help **users identify high‑confidence skills** and ​**guide developers in improving their contributions**​—paving the way for a dependable and transparent ecosystem of medical research agent capabilities, with concrete evaluation results like those shown for example skills.
