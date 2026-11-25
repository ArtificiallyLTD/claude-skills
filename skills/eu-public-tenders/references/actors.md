# Actor reference for eu-public-tenders

Generated from the Actors' input schemas. Pass inputs as JSON to `scripts/apify_run.py run <actor> --input ...`.

## `eu-tenders-scraper`

Store page: https://apify.com/artificially/eu-tenders-scraper

### Input

- `searchQuery` (string): Full-text keywords searched in TED notices (newest first). Multi-word input is matched as an exact phrase. Leave empty to browse by filters only. Example: "software development".
- `country` (string): Buyer country as a 2-letter ISO 3166 code (EU/EEA plus UK, CH and candidate countries). Leave empty for all countries. Example: "DE" for Germany, "FR" for France.
- `cpvCodes` (array): List of Common Procurement Vocabulary (CPV) codes, digits only (2-8 digits; shorter codes match whole divisions). Matches notices with any of the codes. Example: ["72000000", "48000000"] for IT services and software.
- `noticeType` (string; one of `cn-standard`, `cn-social`, `pin-only`, `can-standard`, `can-social`, `veat`, `subco`): Type of TED notice. Use "cn-standard" for open calls you can still bid on, "can-standard" for awarded contracts (winners and values). Empty string = all types.
- `procedureType` (string; one of `open`, `restricted`, `neg-w-call`, `neg-wo-call`, `comp-dial`, `innovation`): Procurement procedure type. "open" = any qualified supplier may bid; "restricted" = prequalification required. Empty string = all procedures.
- `maxTenders` (integer; default 100): Maximum number of tenders to save (1-1000). Each saved tender is one dataset item. Use 5-20 for quick answers.
- `dateFrom` (string): Only notices published on or after this date, format YYYY-MM-DD. Example: "2026-01-01". If no search query and no dates are given, the last 30 days are used.
- `dateTo` (string): Only notices published on or before this date, format YYYY-MM-DD. Example: "2026-06-30".
- `onlyOpenDeadlines` (boolean; default false): If true, only return notices whose tender submission deadline is still in the future (notices without a deadline, such as award notices, are excluded).
- `minDaysUntilDeadline` (integer): Only return notices whose earliest submission deadline is at least this many days from today (0-365). Example: 14 for at least two weeks to prepare a bid.
- `includeBuyerProfile` (boolean; default true): If true, adds a buyerProfile object with the buyer's recent TED notices, top CPV codes and preferred procedures (one extra API request per new buyer). Set false for faster runs.
- `includeFullDetails` (boolean; default true): If true, fetches descriptions, lots, full buyer contact details, contract dates, place of performance and award details. Set false for faster, lighter results.
- `includeSimilarTenders` (boolean; default false): If true, adds a similarTenders list of recent notices with the same main CPV code in the same country (one extra API request per tender).
- `maxSimilarTenders` (integer; default 5): Maximum similar tenders listed per result (1-20) when includeSimilarTenders is true. Example: 5.
- `minEstimatedValue` (integer): Only return notices with an estimated value at or above this amount, in the notice currency (usually EUR). Notices without an estimated value are excluded. Example: 100000.
- `maxEstimatedValue` (integer): Only return notices with an estimated value at or below this amount, in the notice currency (usually EUR). Notices without an estimated value are excluded. Example: 5000000.
- `compactOutput` (boolean; default false): If true, each dataset item is a slim record with only key decision fields (notice ID, title, buyer, country, deadline, value, CPV, award winner, URL) and counts instead of long descriptions, lot lists, buyer profiles and similar tenders. Recommended for AI agents and MCP clients. If false, the full record is returned.

### Output fields

`noticeId`, `tedNoticeNumber`, `documentNumber`, `publicationDate`, `submissionDeadline`, `contractStartDate`, `contractEndDate`, `noticeType`, `noticeTypeDescription`, `procedureType`, `contractType`, `title`, `titleEnglish`, `shortDescription`, `fullDescription`, `estimatedValue`, `currency`, `valueRange`, `buyer`, `buyerName`, `buyerEmail`, `cpvCodes`, `cpvCount`, `mainCpvCode`, `nutsCode`, `nutsDescription`, `country`, `countryCode`, `region`, `city`, `numberOfLots`, `lots`, `lotsCount`, `awarded`, `winnerName`, `winnerCountry`, `awardedValue`, `numberOfTenders`, `url`, `pdfUrl`, `xmlUrl`, `buyerProfile`, `similarTenders`, `daysUntilDeadline`, `isExpired`, `competitionLevel`, `scrapedAt`
