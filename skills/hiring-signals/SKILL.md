---
name: hiring-signals
description: Track who is hiring and for what. Searches LinkedIn job postings by keyword, location, seniority, job type and remote filter, and pulls every open role straight from company career sites and applicant tracking systems (Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable, Recruitee, Personio). Use for competitor hiring analysis, sales trigger events ("companies hiring a Head of Data"), job market research, salary and skills scans, recruiting lead lists, or monitoring a list of companies for new roles.
---

# Hiring signals

Two Apify Actors by Artificially:

- `linkedin-jobs-scraper`: search LinkedIn Jobs like a job seeker would (keywords + location + filters). Best for "who is hiring X in Y".
- `career-site-jobs-scraper`: every open role at specific companies, read directly from their careers page or ATS. Best for "what is company Z hiring for", with full descriptions and often salary ranges.

## Setup

The runner needs an Apify API token in the `APIFY_TOKEN` environment variable (or a logged-in Apify CLI). If it is missing, tell the user to create a free account at https://console.apify.com/sign-up and copy the token from Settings > API & Integrations.

## Cost (billed to the user's Apify account)

| Actor | Per run | Per result |
| --- | --- | --- |
| `linkedin-jobs-scraper` | $0.25 | $0.002 per job |
| `career-site-jobs-scraper` | $0.05 | $0.00315 per job |

100 LinkedIn jobs cost about $0.45. Put several search queries or companies into one run (one per-run fee). Before a job above about $2, tell the user the estimate and ask.

## How to run

Run `scripts/apify_run.py` from this skill's folder by its full path while staying in the user's working directory (do not `cd` into the skill folder), so results are saved next to the user's work. It needs Python 3 and no packages:

```bash
python3 scripts/apify_run.py run linkedin-jobs-scraper \
  --input '{"searchQueries": ["data engineer"], "location": "Berlin, Germany", "datePosted": "past-week", "maxJobs": 50, "compactOutput": true}' \
  --fields title,company,location,listingDateParsed,jobUrl --preview 10

python3 scripts/apify_run.py run career-site-jobs-scraper \
  --input '{"companies": ["greenhouse:stripe", "https://jobs.lever.co/palantir", "notion.com/careers"], "keywords": ["engineer"], "includeDescription": false, "maxJobsPerCompany": 50}' \
  --fields company,title,department,location,isRemote,jobUrl --preview 10
```

All items are saved to `apify-output/<actor>-<runId>.json`; analyze that file (counts by company, department, location, seniority) rather than re-running. If it returns `"status": "RUNNING"`, call `python3 scripts/apify_run.py results <runId>` later.

Full input options and output fields are in [references/actors.md](references/actors.md).

## Building good inputs

- **LinkedIn search:** one entry in `searchQueries` per distinct role; `location` as typed on LinkedIn ("United States", "London, England, United Kingdom", "San Francisco Bay Area"). Filters: `datePosted` (`past-24h`, `past-week`, `past-month`), `experienceLevel` (`entry`, `mid-senior`, `director`, `executive`...), `jobType`, `remoteFilter` (`remote`, `hybrid`, `on-site`).
- **Career sites:** `companies` accepts an ATS URL, the shorthand `platform:slug` (`greenhouse:stripe`, `lever:palantir`, `ashby:ramp`), a company's own careers page (the embedded ATS is detected), or a bare slug that is probed on common platforms. Filter with `keywords`, `excludeKeywords`, `locations`, `departments`, `remoteOnly`, `postedWithinDays`.
- Set `includeDescription: false` for counts and lists; turn it on for skills, tech stack or salary analysis of a smaller set.
- For monitoring, `onlyNewSinceLastRun: true` (career sites) returns only roles not seen by earlier runs with the same input.

## Workflows

**Competitor hiring analysis:** run `career-site-jobs-scraper` on the competitors (descriptions off), then summarize open roles by company, department and location, what that implies (new markets, products, teams being built), and quote 2-3 notable senior roles with links.

**Sales trigger list:** `linkedin-jobs-scraper` for the role that signals need (e.g. "Head of RevOps", "first data engineer") with `datePosted: past-week`; deduplicate by company and output company, role, location, posting date and link.

**Job market scan:** LinkedIn search for the role and location, then summarize top hiring companies, remote share, seniority mix and, for a sample with descriptions from career sites, the most requested skills and stated salary ranges.

## Notes

- LinkedIn shows logged-out visitors up to about 1,000 results per search; split very broad searches by location.
- Career-site results come straight from the employer, so they are the most complete and current list for that company.
- Report blocked pages or unknown career sites (listed in the run's status message) instead of guessing.
