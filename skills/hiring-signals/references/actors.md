# Actor reference for hiring-signals

Generated from the Actors' input schemas. Pass inputs as JSON to `scripts/apify_run.py run <actor> --input ...`.

## `linkedin-jobs-scraper`

Store page: https://apify.com/artificially/linkedin-jobs-scraper

### Input

- `searchQueries` (array, required): Job search keywords, one query per line; each is searched separately, e.g. "data engineer" or "product manager fintech". Required.
- `location` (string): Location to search in, as you would type it on LinkedIn Jobs: a city, region or country, e.g. "Berlin, Germany", "San Francisco Bay Area", "United States". Leave empty for worldwide.
- `maxJobs` (integer; default 100): Maximum number of jobs to save per search query. Integer 1-1000, e.g. 25. LinkedIn returns at most about 1000 jobs per search. Use a small number (10-25) for quick answers.
- `jobType` (array; one of `full-time`, `part-time`, `contract`, `temporary`, `internship`, `volunteer`): Filter by employment type. Array of any of: "full-time", "part-time", "contract", "temporary", "internship", "volunteer", e.g. ["full-time", "contract"]. Empty for all types.
- `experienceLevel` (array; one of `internship`, `entry`, `associate`, `mid-senior`, `director`, `executive`): Filter by seniority. Array of any of: "internship", "entry", "associate", "mid-senior", "director", "executive", e.g. ["mid-senior"]. Empty for all levels.
- `datePosted` (string; default "any"; one of `any`, `past-24h`, `past-week`, `past-month`): Only return jobs posted within this window. One of: "any", "past-24h", "past-week", "past-month". Default "any".
- `remoteFilter` (string; default "any"; one of `any`, `remote`, `on-site`, `hybrid`): Filter by workplace type. One of: "any", "remote", "on-site", "hybrid". Default "any".
- `compactOutput` (boolean; default false): If true, save a slimmer item per job with only: jobId, title, company, companyUrl, location, listingDateParsed, jobUrl. Drops the logo URL, relative listing date, searchQuery and scrapedAt. Recommended for AI agents and LLM pipelines. Default false keeps the full item.

### Output fields

`jobId`, `title`, `company`, `companyUrl`, `companyLogoUrl`, `location`, `listingDate`, `listingDateParsed`, `jobUrl`, `searchQuery`, `scrapedAt`

## `career-site-jobs-scraper`

Store page: https://apify.com/artificially/career-site-jobs-scraper

### Input

- `companies` (array, required): Required. One company per entry. Accepted formats: a job-board URL (e.g. https://job-boards.greenhouse.io/stripe, https://jobs.lever.co/palantir, https://jobs.ashbyhq.com/ramp, https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite, https://careers.smartrecruiters.com/ServiceNow, https://bunq.recruitee.com, https://apply.workable.com/huggingface, https://1komma5grad.jobs.personio.de); the shorthand platform:slug (e.g. greenhouse:stripe, lever:palantir, ashby:ramp, workday:nvidia.wd5/NVIDIAExternalCareerSite); a company's own careers page (e.g. https://www.notion.com/careers, the embedded ATS is detected automatically); or just a slug (e.g. stripe) to probe the common platforms. Example: ["greenhouse:stripe", "https://jobs.lever.co/palantir"].
- `keywords` (array): Keep jobs whose title (or description, see keywordsInDescription) contains ANY of these words or phrases. Case-insensitive. Example: ["engineer", "data scientist"]. Leave empty to keep all jobs.
- `keywordsInDescription` (boolean; default true): If true, a keyword match in the job description also counts. Set to false to match job titles only (stricter, fewer false positives).
- `excludeKeywords` (array): Drop jobs whose title contains ANY of these words. Case-insensitive. Example: ["senior", "intern", "manager"].
- `locations` (array): Keep jobs whose location contains ANY of these strings (city, state/region, country, or "remote"). Case-insensitive substring match. Example: ["London", "United States", "Germany"].
- `remoteOnly` (boolean; default false): Set to true to keep only jobs marked remote by the ATS or with "remote" in the location.
- `departments` (array): Keep jobs whose department or team contains ANY of these strings. Case-insensitive. Example: ["Engineering", "Sales"].
- `employmentTypes` (array; one of `full-time`, `part-time`, `contract`, `temporary`, `internship`, `other`): Keep only these employment types. Allowed values: full-time, part-time, contract, temporary, internship, other. Example: ["full-time", "contract"]. Jobs whose ATS does not publish a type are kept only when full-time is selected. Leave empty for all types.
- `postedWithinDays` (integer): Keep only jobs published in the last N days, as an integer from 1 to 3650. Example: 7. Leave empty for any date.
- `maxJobsPerCompany` (integer): Stop after saving this many jobs from a single company. Example: 10. Leave empty for no limit.
- `maxResults` (integer): Stop the run after saving this many jobs in total across all companies. Example: 50. Leave empty for no limit (the run also stops at your maximum cost per run).
- `includeDescription` (boolean; default true): Return the full description as both HTML (descriptionHtml) and clean plain text (descriptionText). Set to false for smaller, faster output (Workday and SmartRecruiters then skip per-job detail requests). Descriptions are never returned when compactOutput is on.
- `onlyNewSinceLastRun` (boolean; default false): Set to true to remember job IDs already returned for this exact input (companies + filters) and return only jobs you have not seen before. Ideal with Apify Schedules: you pay only for new postings.
- `compactOutput` (boolean; default false): Set to true to save a slim item per job with only the key fields: jobId, platform, company.name, title, department, location, isRemote, workplaceType, employmentType, salary (min, max, currency, interval), postedAt and jobUrl. Descriptions, parsed locations, raw fields and URLs other than jobUrl are dropped. Recommended when an AI agent or LLM reads the results; combine with includeDescription false for the fastest runs. Leave false for the full item.

### Output fields

`jobId`, `platform`, `company`, `title`, `department`, `team`, `location`, `locations`, `isRemote`, `workplaceType`, `employmentType`, `employmentTypeRaw`, `salary`, `postedAt`, `updatedAt`, `applyUrl`, `jobUrl`, `descriptionText`, `descriptionHtml`, `scrapedAt`
