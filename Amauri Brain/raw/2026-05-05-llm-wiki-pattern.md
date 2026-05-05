# LLM Wiki — A pattern for building personal knowledge bases using LLMs

*Source: idea file shared by Amauri, 2026-05-05*

## Core idea

Most RAG systems re-derive knowledge from scratch on every query. The LLM Wiki is different: the LLM incrementally builds and maintains a persistent wiki — structured, interlinked markdown files — that sits between you and raw sources. When a new source arrives, the LLM reads it, extracts key information, and integrates it into the existing wiki: updating entity pages, revising summaries, flagging contradictions.

The wiki is a persistent, compounding artifact. Cross-references already exist. Contradictions already flagged. Synthesis already reflects everything you've read.

## Three layers

1. **Raw sources** — immutable. LLM reads, never modifies.
2. **Wiki** — LLM-generated markdown. LLM owns this entirely.
3. **Schema** (CLAUDE.md / AGENTS.md) — rules for how the LLM operates. Co-evolved over time.

## Operations

- **Ingest:** drop source → LLM reads → discusses → writes summary → updates entity/concept pages → updates index → logs entry
- **Query:** LLM reads index → reads relevant pages → synthesizes with citations → offers to file answer as synthesis page
- **Lint:** periodic health check — contradictions, stale claims, orphan pages, missing links, gaps

## Indexing and logging

- **index.md** — content-oriented catalog. LLM reads this first on every query to find relevant pages.
- **log.md** — append-only chronological record. Grep-friendly if entries start with `## [YYYY-MM-DD]`.

## Optional tooling

- **Obsidian** as the IDE for browsing the wiki in real time (graph view, Dataview, Marp)
- **Obsidian Web Clipper** for converting web articles to markdown
- **qmd** — local search engine for markdown with BM25/vector hybrid + LLM re-ranking, has CLI and MCP server
- **Marp** — markdown-based slide deck format

## Key insight

The tedious part of a knowledge base is the bookkeeping: updating cross-references, noting contradictions, keeping pages current. Humans abandon wikis because maintenance cost grows faster than value. LLMs don't get bored. The wiki stays maintained because maintenance cost is near zero.

## Vannevar Bush / Memex connection

Related in spirit to Bush's Memex (1945): private, actively curated, with connections between documents as valuable as the documents themselves. The part Bush couldn't solve: who does the maintenance. The LLM handles that.
