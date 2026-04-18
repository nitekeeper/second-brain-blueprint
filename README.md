# LLM Wiki — Second Brain Blueprint

> A personal knowledge system where an AI agent maintains a persistent, compounding wiki for you. Knowledge builds over time instead of being re-derived on every question.

---

## What Is This?

Most AI tools re-derive answers from scratch every time you ask a question. Nothing accumulates.

This system is different. An AI agent reads your sources, builds a wiki of interconnected markdown pages, and maintains it over time — cross-referencing, flagging contradictions, and compounding knowledge with every new source you add.

**The longer you use it, the more valuable it gets.**

---

## What You Need

| Tool | Purpose | Cost |
|---|---|---|
| [Claude Desktop (Cowork)](https://claude.ai/download) | The AI agent that maintains your wiki | Claude Pro ($20/mo) |
| [Obsidian](https://obsidian.md) | Browse and view your wiki locally | Free |
| [Obsidian Web Clipper](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf) | Clip web articles as clean markdown | Free (Chrome) |

---

## How to Set Up

### 1. Install the tools
- Install **Obsidian** (you'll point it at `wiki/` after setup — don't create a vault yet)
- Install **Claude Desktop** and enable Cowork mode
- Install the **Obsidian Web Clipper** Chrome extension

### 2. Clone this repo into your vault folder
```bash
cd /path/to/your/vault
git clone https://github.com/nitekeeper/second-brain-blueprint blueprint
```

### 3. Select your working folder in Cowork
In the Cowork window, click **"Select folder"** and choose the folder where you cloned the repo (the parent folder containing `blueprint/`). This is your working directory — **not** `wiki/`.

### 4. Tell your AI to set it up
Open Claude Desktop (Cowork) and send this message:

```
Read blueprint/setup-guide.md and set up the wiki system for me.
```

Claude will execute the full setup — creating folders, copying files, and initializing the wiki. You only need to answer one question: your name.

### 5. Start using it
Once setup is complete, follow `blueprint/user-guide.md` for daily usage.

---

## Key Features

- **Lean startup** — agent cold-starts in ~1,000 tokens; reads only what it needs
- **Approval before every write** — agent shows a plan + token estimate before touching any file
- **Query waterfall** — answers from training first, then wiki, then web search
- **Web Clipper optimized** — clipping articles before ingesting saves 40–60% in tokens vs URL fetch
- **Pros/cons on every suggestion** — agent always shows trade-offs before recommending changes

---

## Daily Usage

See `blueprint/user-guide.md` for the full daily workflow.

**The three things you'll do most:**
- Clip an article → `ingest [filename]`
- Ask a question → just ask, no command needed
- Health check → `lint all`
