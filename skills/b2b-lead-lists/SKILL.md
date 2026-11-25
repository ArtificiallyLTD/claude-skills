---
name: b2b-lead-lists
description: Build and enrich B2B lead lists. Finds startups in the Y Combinator directory by industry, batch, location, team size and hiring status (with founders and socials), extracts public emails, phone numbers and social profiles from company websites, and detects each website's tech stack (CMS, ecommerce, analytics, CRM, email provider, payments, hosting). Use for prospect lists, enriching a list of domains, finding companies that use a given technology (e.g. Shopify, HubSpot), founder outreach research, or market maps of startups.
---

# B2B lead lists

Three Apify Actors by Artificially that chain together:

- `ycombinator-scraper`: companies from the public YC directory, optionally with founders, open jobs and social links.
- `company-contact-extractor`: public emails, phones, social profiles and contact page for a list of websites.
- `website-tech-stack-detector`: technologies used by a list of websites, plus email provider from DNS.

## Setup

The runner needs an Apify API token in the `APIFY_TOKEN` environment variable (or a logged-in Apify CLI). If it is missing, tell the user to create a free account at https://console.apify.com/sign-up and copy the token from Settings > API & Integrations.

## Cost (billed to the user's Apify account)

| Actor | Per run | Per result |
| --- | --- | --- |
| `ycombinator-scraper` | $0.05 | $0.00315 per company |
| `company-contact-extractor` | $0.05 | $0.009 per website with contacts found |
| `website-tech-stack-detector` | $0.05 | $0.015 per website |

Websites with no contacts found, or that fail to load, are not charged. Enriching 100 domains with both contacts and tech stack costs about $2.50. Put the whole list into one run per Actor, and before a job above about $2 tell the user the estimate and ask.

## How to run

Run `scripts/apify_run.py` from this skill's folder by its full path while staying in the user's working directory (do not `cd` into the skill folder), so results are saved next to the user's work. It needs Python 3 and no packages:

```bash
python3 scripts/apify_run.py run ycombinator-scraper \
  --input '{"industries": ["Fintech"], "batches": ["W25", "S25"], "isHiring": true, "maxResults": 30, "compactOutput": true}' \
  --fields name,website,oneLiner,teamSize,location --preview 10

python3 scripts/apify_run.py run company-contact-extractor \
  --input '{"websites": ["stripe.com", "plausible.io"], "emailFilter": "generic_only", "compactOutput": true}'

python3 scripts/apify_run.py run website-tech-stack-detector \
  --input '{"websites": ["allbirds.com", "gymshark.com"], "compactOutput": true}'
```

For long lists, write the input to a file and pass `--input @input.json`. All items are saved to `apify-output/<actor>-<runId>.json`; join the files on `domain`/`website` rather than re-running. If a run returns `"status": "RUNNING"`, call `python3 scripts/apify_run.py results <runId>` later.

Full input options and output fields are in [references/actors.md](references/actors.md).

## Building good inputs

- **YC:** `searchQuery` works like the directory's search box; `industries` (e.g. `B2B`, `Fintech`, `Healthcare`, `Consumer`), `tags` (e.g. `Artificial Intelligence`, `SaaS`, `Developer Tools`), `batches` (`W25`, `S24`, or "Winter 2025"), `locations` (city substrings), `teamSizeMin`/`teamSizeMax`, `status: ["Active"]`, `isHiring`. Add `includeFounders` for founder names and LinkedIn URLs (one extra page per company, so keep `maxResults` modest).
- **Contacts:** `websites` takes bare domains or URLs. `emailFilter: "generic_only"` keeps role inboxes (info@, sales@), `exclude_generic` keeps personal addresses only. `maxPagesPerDomain` 5-10 is usually enough.
- **Tech stack:** narrow with `categories` (e.g. `["Ecommerce", "Analytics", "CRM"]`) or keep only domains using a technology with `onlyDomainsUsing` (e.g. `["Shopify"]`), which is the way to build "companies using X" lists from a domain list.

## Lead list workflow

1. Source companies: YC search, or the user's own list of domains.
2. Enrich: one `website-tech-stack-detector` run and one `company-contact-extractor` run over all domains.
3. Join on domain and deliver a table (or CSV via Python): company, website, one-liner, size, location, key technologies, generic email, phone, LinkedIn. Mark missing values as empty; never invent emails or guess address patterns.

## Notes

- Only publicly published contact details are collected, robots.txt is respected by default, and personal emails are subject to GDPR/CAN-SPAM: remind the user to use them lawfully (legitimate interest, opt-out in every message).
- YC data reflects the public directory at run time; `onlyNewSinceLastRun: true` returns only companies not seen by earlier runs with the same filters, which suits weekly "new YC companies" alerts.
