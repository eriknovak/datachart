---
title: AI Assistants
---

# AI Assistants

A coding assistant writes better `datachart` code when it reads the current documentation instead of recalling an older release: chart types, parameters, and constants change between versions, and a guessed keyword argument fails at runtime. The site is published in formats made for that. This page shows how to hand the docs to an assistant, from a link pasted into a prompt to a server the assistant queries on its own, and ends with a rules snippet that tells it how the package is meant to be used.

## What the site publishes

Every build of the documentation writes three machine-readable views next to the pages:

| View | URL | What it holds |
| --- | --- | --- |
| Index | [llms.txt](https://eriknovak.github.io/datachart/latest/llms.txt) | Every page with a one-line description, grouped by section. Small enough to paste. |
| Full text | [llms-full.txt](https://eriknovak.github.io/datachart/latest/llms-full.txt) | The whole site in one file: guide prose, code, and the API reference. |
| Per page | append `index.md` to a page URL | The page as plain markdown, for example [how-to-guides/charts/linechart/index.md](https://eriknovak.github.io/datachart/latest/how-to-guides/charts/linechart/index.md). |

The `latest` segment in the URLs is the released version. Replace it with `dev` for the documentation of the main branch, or with a version number such as `0.9.1` to pin a release.

## Paste a link

The simplest route needs no setup: put the URL of the index or of the page you need in the prompt. Assistants with web access fetch it and read from the current docs.

```text
Draw a grouped bar chart of the medal table with datachart. Read the guide
first: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/barchart/index.md
```

For a longer task, paste `llms.txt` once at the start of the session; the assistant then knows which page to fetch for each question.

## Connect an MCP server

An assistant that supports the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) can query the docs without a link in every prompt. Two hosted servers cover this repository; neither needs anything installed.

### Context7

[Context7](https://context7.com/eriknovak/datachart) indexes the documentation per version and returns the pages that match a question. The library ID is `/eriknovak/datachart`.

=== "Claude Code"

    ```bash
    claude mcp add --transport http context7 https://mcp.context7.com/mcp
    ```

=== "Cursor and others"

    ```json
    {
      "mcpServers": {
        "context7": {
          "url": "https://mcp.context7.com/mcp"
        }
      }
    }
    ```

Then name the library in the prompt, or add "use context7" to have the assistant resolve it:

```text
Use context7 to look up datachart's Panel, then overlay a histogram and a
cumulative line with the line on a secondary axis.
```

### GitMCP

[GitMCP](https://gitmcp.io/eriknovak/datachart) serves the repository's documentation as an MCP endpoint at `https://gitmcp.io/eriknovak/datachart`, with tools to fetch and search it.

=== "Claude Code"

    ```bash
    claude mcp add --transport sse datachart-docs https://gitmcp.io/eriknovak/datachart
    ```

=== "Cursor and others"

    ```json
    {
      "mcpServers": {
        "datachart-docs": {
          "url": "https://gitmcp.io/eriknovak/datachart"
        }
      }
    }
    ```

Once connected, the assistant calls the server whenever a question is about `datachart`; no prompt wording is needed.

## Describe the package in the project rules

A link tells the assistant where the docs are; a rules file tells it how the package fits together, so it reaches for the right function before it reads anything. Add the block below to the file your assistant reads at the start of a session: `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex and others, `.cursor/rules` for Cursor.

```markdown
## Charts: datachart

Charts are drawn with the `datachart` package (built on matplotlib).
Docs: https://eriknovak.github.io/datachart/latest/ (index for LLMs: /llms.txt;
any page as markdown by appending index.md to its URL).

- Every chart is one function from `datachart.charts` (LineChart, BarChart,
  ScatterChart, Histogram, ...) that takes a list of series, each a list of
  dicts. Look up the dict keys and parameters of a chart in its guide before
  using it: https://eriknovak.github.io/datachart/latest/how-to-guides/charts/
- Style is global: `config.set_theme(THEME.X)` and `config.update_config(...)`
  from `datachart.config` and `datachart.constants`. Per-chart overrides go in
  the chart's `style` argument. Do not restyle through matplotlib directly.
- Combine finished figures with `Panel` (overlay on shared axes) and `Grid`
  (arrange in cells) from `datachart.utils`; write files with `save_figure`.
- Every chart returns a matplotlib `Figure`.
```

The block is deliberately short. The assistant fetches the details from the guides once it knows they exist, and a long copy of the reference goes stale with the next release.
