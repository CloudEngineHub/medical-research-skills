# 🏥 AIPOCH — Medical Research AI Skill Library
### A structured, validated skill repository for AI-supported medical research

A curated collection of **200+ medical research skills** designed for scientists, researchers, and AI agents.

This repository is part of the **AIPOCH ecosystem** — a community platform for sharing and discovering biomedical agent skills.

🌐 [Learn more](https://AIPOCH.com)

---

## 🧠 About AIPOCH

AIPOCH is a professional AI skill library dedicated to medical research.

We curate and structure reusable research skills that support clinical investigation, biomedical analysis, and scientific reasoning. Each skill represents a well-defined medical research capability designed to be both human-understandable and AI-compatible.

Our mission is to make medical research expertise:

- Structured  
- Reproducible  
- Modular  
- Integrable into AI systems  

AIPOCH provides a foundational skill layer for next-generation medical research workflows.

---

## 📚 What Is a Medical Research AI Skill?

A Medical Research AI Skill is a structured representation of a specific research capability, such as:

- Clinical data interpretation  
- Study design evaluation  
- Biomedical data analysis  
- Literature synthesis  
- Hypothesis development  
- Research result structuring  

Each skill includes:

- Clearly defined objectives  
- Expected inputs and outputs  
- Logical reasoning steps  
- Reusable execution structure  

This ensures consistency, reliability, and integration potential.

---

## 🦞 Install into OpenClaw

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
> ```bash
> OPENCLAW_SKILLS_DIR=~/.openclaw/workspace/skills bash <(curl -s https://raw.githubusercontent.com/aipoch/medical-research-skills/main/scientific-skills/scripts/openclaw-install.sh)
> ```

---

## 📦 What’s Inside This Repository

### 🗂️ Skill Domains

The library spans major domains of medical research:

- 🏥 Clinical Research  
- 🔬 Experimental Research  
- 📊 Medical Data Analysis  
- 🧬 Bioinformatics  
- 📚 Literature & Evidence Synthesis  
- 💊 Pharmaceutical & Translational Research  
- 🧾 Grant & Research Strategy  
- 🧠 Scientific Reasoning & Interpretation  

The repository currently contains **200+ structured skills**, with validated modules continuously expanding.



### 🗂️ Skill Categories

This repository organizes medical agent skills into structured domains.  
Each category represents a key area of biomedical research, professional practice, or scientific workflow.


> 📌 *Skill counts will continue to grow as the community contributes.*

| Category | Description | # of Skills |
|----------|-------------|-------------|
| 🏥 **Clinical** | Clinical research workflows, patient data interpretation, medical reasoning support | `20` |
| 🎓 **Education** | Learning guides, training-oriented skills, and knowledge-building workflows | `11` |
| 🔬 **Research** | Experimental design, research strategy, and scientific reasoning skills | `20` |
| 🌍 **General** | Cross-domain biomedical workflows and foundational research utilities | `13` |
| ✍️ **Writing** | Scientific writing, manuscript structuring, and academic communication skills | `9` |
| 📊 **Data** | Biomedical data analysis, interpretation, and structured data workflows | `9` |
| 💊 **Pharma** | Drug development, pharmacology insights, and translational research skills | `29` |
| 🚀 **Career** | Academic career development, grant planning, and professional growth skills | `9` |
| 🧬 **Bioinfo** | Bioinformatics analysis, omics interpretation, and computational biology workflows | `25` |
| ℹ️ **Info** | Information extraction, literature processing, and knowledge structuring skills | `7` |
| 🎤 **Present** | Scientific presentation, slide structuring, and research communication skills | `6` |
| 🧪 **Wet Lab** | Experimental lab workflows, protocol reasoning, and bench research support | `12` |
| 🧰 **Utility** | General-purpose biomedical utilities and cross-workflow helper skills | `7` |
| 💰 **Grant** | Grant writing, funding strategy, and proposal development skills | `7` |
| ⚙️ **Operations** | Research operations, project coordination, and lab or team management skills | `6` |


#### 📈 Total Skills in Library: **200+ and growing**

---

## 🤖 AI-Compatible by Design

All skills are formatted to support:

- Programmatic parsing  
- Workflow integration  
- Multi-step reasoning pipelines  
- Human–AI collaborative research  

This makes AIPOCH not only a knowledge repository, but an infrastructure layer for AI-assisted medical research systems.

---

## ❤️ Built for the Medical Research Community

Medical research increasingly depends on structured knowledge and intelligent systems.

AIPOCH is building a professional, reusable AI skill foundation to support high-quality, scalable, and future-ready medical research.
