# Business data skills for Claude

Five [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that let Claude pull fresh business data on request: LinkedIn profiles and companies, US government contracts, EU public tenders, hiring activity and B2B leads. Each skill tells Claude which [Apify Actor](https://apify.com/artificially) to run, how to build a good input, what it costs and how to turn the results into a brief, a shortlist or a table.

| Skill | Ask Claude things like | Actors used |
| --- | --- | --- |
| [`linkedin-research`](skills/linkedin-research/SKILL.md) | "Research Acme Corp and the two people I'm meeting there tomorrow" | LinkedIn Profile, Company, Posts and Employees scrapers |
| [`us-government-contracts`](skills/us-government-contracts/SKILL.md) | "Find open cybersecurity contracts for a small business in Virginia, and who won similar ones" | SAM.gov Opportunities, USAspending contracts |
| [`eu-public-tenders`](skills/eu-public-tenders/SKILL.md) | "Open software tenders in Germany and Austria over €200k, due in at least 3 weeks" | EU Tenders (TED) |
| [`hiring-signals`](skills/hiring-signals/SKILL.md) | "What are our five competitors hiring for right now?" | LinkedIn Jobs, Career Site Jobs (Greenhouse, Lever, Ashby, Workday and more) |
| [`b2b-lead-lists`](skills/b2b-lead-lists/SKILL.md) | "Fintech YC companies from 2025 that are hiring, with their contact emails and tech stack" | Y Combinator, Company Contacts, Website Tech Stack |

## Install in Claude Code

```
/plugin marketplace add ArtificiallyLTD/claude-skills
/plugin install business-data-skills@artificially
```

Then give the skills an Apify API token. Create a free account at [console.apify.com](https://console.apify.com/sign-up), copy the token from **Settings → API & Integrations**, and export it before starting Claude Code:

```bash
export APIFY_TOKEN=your_token_here
```

If you already use the Apify CLI (`apify login`), the skills pick up its token automatically.

## Use the skills elsewhere

Each skill is a self-contained folder (`SKILL.md`, a reference file and a small Python runner with no dependencies). The [releases page](https://github.com/ArtificiallyLTD/claude-skills/releases) has one zip per skill for uploading to Claude apps that support custom skills. The runner needs Python 3, network access to `api.apify.com` and the `APIFY_TOKEN` environment variable, so it works best where Claude can run code with your environment, such as Claude Code or the Claude Agent SDK.

## What it costs

The skills are free. Runs are billed by Apify to your own account at each Actor's pay-per-result price, typically a few cents to $0.40 per run plus a fraction of a cent per result (for example, 50 open SAM.gov opportunities cost about $0.36). Apify's free plan includes monthly credit for trying them out. Blocked or empty pages are never charged, and every skill tells Claude to batch inputs into one run and to ask you before any job above about $2.

## How it works

`scripts/apify_run.py` starts the Actor through the Apify API, waits for it, saves every result to `apify-output/<actor>-<runId>.json` in your working folder and prints a short summary for Claude. Claude then reads the saved file to sort, filter, join and summarize. Your token is only sent to `api.apify.com`.

## Responsible use

The Actors collect publicly available data only, without logging in to any site. You are responsible for using it lawfully, including privacy rules such as GDPR and anti-spam laws when contacting people.

## License

MIT. Built by [Artificially](https://apify.com/artificially). Also available as an [MCP server](https://github.com/ArtificiallyLTD/business-data-mcp), [n8n templates](https://github.com/ArtificiallyLTD/n8n-business-data-templates) and [open datasets](https://github.com/ArtificiallyLTD/open-business-datasets).
