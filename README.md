# Artificially Data for Claude

Live business data inside Claude. Ask a question and Claude pulls fresh results from public sources: LinkedIn profiles and companies, US government contracts, EU public tenders, hiring activity and B2B leads. Five skills tell Claude which data source to use, how to build a good query, what it costs and how to turn the results into a brief, a shortlist or a table. You pay per answer from prepaid credits, with no subscription and no other account needed.

| Skill | Ask Claude things like | Data sources |
| --- | --- | --- |
| [`linkedin-research`](skills/linkedin-research/SKILL.md) | "Research Acme Corp and the two people I'm meeting there tomorrow" | LinkedIn profiles, company pages, company posts, featured employees |
| [`us-government-contracts`](skills/us-government-contracts/SKILL.md) | "Find open cybersecurity contracts for a small business in Virginia, and who won similar ones" | SAM.gov opportunities, USAspending awards |
| [`eu-public-tenders`](skills/eu-public-tenders/SKILL.md) | "Open software tenders in Germany and Austria over €200k, due in at least 3 weeks" | TED (Tenders Electronic Daily) |
| [`hiring-signals`](skills/hiring-signals/SKILL.md) | "What are our five competitors hiring for right now?" | LinkedIn Jobs, company career sites (Greenhouse, Lever, Ashby, Workday and more) |
| [`b2b-lead-lists`](skills/b2b-lead-lists/SKILL.md) | "Fintech YC companies from 2025 that are hiring, with their contact emails and tech stack" | Y Combinator directory, company websites |

## Install in Claude Code

```
/plugin install artificially-data --marketplace ArtificiallyLTD/claude-skills
```

On older Claude Code versions, run `/plugin marketplace add ArtificiallyLTD/claude-skills` and then `/plugin install artificially-data@artificially`.

## Add your API key

1. Buy prepaid credits at **[artificially-data.netlify.app](https://artificially-data.netlify.app)**: card payment by Stripe, credits never expire. Your API key (it starts with `art_`) is shown right after payment.
2. Claude Code asks for the key when you install the plugin. To add or change it later, run `/plugin`, open **Installed**, choose **artificially-data** and select **Configure**. The key is stored in your system's secure credential store, not in a settings file.

## What it costs

Each data source costs a fixed amount per run (5 to 40 cents) plus a fraction of a cent per result. For example, 50 open SAM.gov opportunities cost about $0.36. The current price list is on [the credits page](https://artificially-data.netlify.app), and Claude can show it with the `list_data_sources` tool. Every run has a hard spending cap (5 dollars unless you agree to more), pages that fail to load are never charged, a run can never spend more than your balance, and the skills tell Claude to ask you before any job above about $2.

## How it works and what it sends

The plugin adds one remote MCP server, `https://artificially-data.netlify.app/mcp`, operated by Artificially, with five tools: `run_data_source`, `get_run_results`, `get_balance`, `buy_credits` and `list_data_sources`. When Claude uses a tool, the plugin sends:

- your API key, in the `Authorization` header, from the plugin's configuration;
- the request: which data source to run and its input, such as search keywords, company websites or LinkedIn URLs.

Our server runs the request on [Apify](https://apify.com), using [Artificially's data collection Actors](https://apify.com/artificially), and returns the results to Claude. It does not receive your conversation, files or anything else from your machine, and the plugin runs no local scripts or hooks. Results are kept for up to 30 days so you can fetch them again. See the [privacy policy](https://artificially-data.netlify.app/privacy.html) and [terms](https://artificially-data.netlify.app/terms.html).

## Responsible use

The data sources collect publicly available information only, without logging in to any site. Results are third-party web content, and the skills tell Claude to treat them as data, never as instructions. You are responsible for using the results lawfully, including privacy rules such as the GDPR and anti-spam laws when contacting people.

## Support

Open an [issue](https://github.com/ArtificiallyLTD/claude-skills/issues) or email contact@artificially.io.

## License

MIT. Built by [Artificially](https://apify.com/artificially). Also available as an [MCP server for Apify users](https://github.com/ArtificiallyLTD/business-data-mcp), [n8n templates](https://github.com/ArtificiallyLTD/n8n-business-data-templates) and [open datasets](https://github.com/ArtificiallyLTD/open-business-datasets).
