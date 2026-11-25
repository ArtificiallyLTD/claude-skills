# Actor reference for us-government-contracts

Generated from the Actors' input schemas. Pass inputs as JSON to `scripts/apify_run.py run <actor> --input ...`.

## `samgov-opportunities-scraper`

Store page: https://apify.com/artificially/samgov-opportunities-scraper

### Input

- `keywords` (string): Free-text search in the notice title, description and solicitation number. All words must match. Example: "cybersecurity" or "janitorial services". Leave empty to return everything that matches the other filters.
- `noticeTypes` (array; one of `o`, `k`, `p`, `r`, `s`, `a`, `u`, `i`, `g`): Notice type codes to include. Allowed values: o = Solicitation, k = Combined Synopsis/Solicitation, p = Presolicitation, r = Sources Sought, s = Special Notice, a = Award Notice, u = Justification (J&A), i = Intent to Bundle, g = Sale of Surplus Property. Example: ["o", "k"] for open solicitations, ["a"] for award notices. Leave empty for all types.
- `naicsCodes` (array): NAICS industry codes (digits only). A shorter prefix matches every code under it. Example: ["541512", "5415"] (541512 = Computer Systems Design Services). Leave empty for all industries.
- `pscCodes` (array): Product Service Codes (4 characters) or prefixes. Example: ["R425", "DA01"] (R425 = Engineering and Technical Support). Leave empty for all.
- `setAsideTypes` (array; one of `SBA`, `SBP`, `8A`, `8AN`, `HZC`, `HZS`, `SDVOSBC`, `SDVOSBS`, `WOSB`, `WOSBSS`, `EDWOSB`, `EDWOSBSS`, `VSA`, `VSS`, `LAS`, `IEE`, `ISBEE`, `BICiv`): Only notices reserved for these small business programs. Use the codes from the allowed values, e.g. ["SBA"] (Total Small Business), ["8A"], ["SDVOSBC"], ["WOSB"], ["HZC"] (HUBZone). Leave empty for all notices, set-aside or not.
- `agencies` (array): Federal departments, agencies or offices by name or numeric SAM.gov organization ID. Each name is matched to the closest SAM.gov organization. Example: ["Department of Veterans Affairs", "NASA"] or ["Army"]. Leave empty for all agencies.
- `states` (array): Two-letter US state codes where the work is performed. Example: ["VA", "MD", "TX"]. Invalid codes are ignored. Leave empty for any location.
- `postedWithinDays` (integer): Only notices published in the last N days, as an integer from 1 to 3650. Example: 7. Ignored when postedFrom is set. Leave empty for no posted-date limit.
- `postedFrom` (string): Only notices published on or after this date. Format YYYY-MM-DD, e.g. "2026-01-31". Overrides postedWithinDays.
- `postedTo` (string): Only notices published on or before this date. Format YYYY-MM-DD, e.g. "2026-03-31".
- `responseDeadlineFrom` (string): Only notices whose response/offer due date is on or after this date. Format YYYY-MM-DD, e.g. "2026-02-01". Handy to skip opportunities you no longer have time to bid on. Notices without a deadline (e.g. award notices) are excluded when this is set.
- `responseDeadlineTo` (string): Only notices whose response due date is on or before this date. Format YYYY-MM-DD, e.g. "2026-04-30".
- `openForResponsesOnly` (boolean; default false): Set to true to get only notices whose response deadline is today or later, so you never get a solicitation you can no longer bid on. Notices without a deadline (e.g. award notices) are excluded when this is on. Ignored when responseDeadlineFrom is set.
- `activeOnly` (boolean; default true): true skips archived and inactive notices. Set to false to include them (e.g. for historical research).
- `sortBy` (string; default "-relevance"; one of `-relevance`, `-modifiedDate`): Order of results. "-relevance" = best keyword match first (only applies when keywords are set). "-modifiedDate" = most recently updated first. Without keywords, and always in monitoring mode, the most recently updated notices come first.
- `includeDescription` (boolean; default true): Add the full notice description as plain text (HTML removed) in the description field. Set to false for smaller output. Ignored when compactOutput is on.
- `includeAttachments` (boolean; default true): Add the name, size and download URL of every public attachment and external link. Files are not downloaded. With compactOutput on, only the attachmentsCount is returned.
- `compactOutput` (boolean; default false): Set to true to save a slim item per notice with only the key fields: noticeId, samUrl, title, solicitationNumber, noticeType, postedDate, responseDeadline, daysUntilDeadline, department, subTier, office, naicsCode, setAsideCode, setAside, placeOfPerformance.state, the first point of contact (name, email), attachmentsCount and award (amount, awardeeName). The full description, attachment list, addresses and other fields are dropped. Recommended when an AI agent or LLM reads the results. Leave false for the full item.
- `maxResults` (integer; default 100): Maximum number of notices to save in this run, from 1 to 10000. Each saved notice is one result. Example: 10 for a quick look, 500 for a full export.
- `onlyNewSinceLastRun` (boolean; default false): Set to true to skip notices already returned by earlier runs with the same filters. Use it with a Schedule to get only fresh opportunities each day. Seen notice IDs are kept in the named key-value store "samgov-opportunities-monitor".

### Output fields

`noticeId`, `samUrl`, `title`, `solicitationNumber`, `noticeType`, `noticeTypeCode`, `active`, `cancelled`, `postedDate`, `modifiedDate`, `responseDeadline`, `responseTimeZone`, `daysUntilDeadline`, `archiveDate`, `department`, `subTier`, `office`, `organizationPath`, `officeAddress`, `naicsCode`, `naicsCodes`, `pscCode`, `setAsideCode`, `setAside`, `placeOfPerformance`, `pointsOfContact`, `description`, `attachments`, `attachmentsCount`, `award`, `parentNoticeId`, `relatedNoticeId`, `scrapedAt`

## `us-contracts-scraper`

Store page: https://apify.com/artificially/us-contracts-scraper

### Input

- `searchQuery` (string): Keywords matched against federal contract award descriptions on USAspending.gov (at least 3 characters). Example: "cybersecurity" or "cloud migration".
- `agency` (string): Awarding top-tier agency name, exactly as it appears on USAspending.gov. Leave empty for all agencies. Example: "Department of Defense", "General Services Administration", "Department of Veterans Affairs".
- `naicsCodes` (array): List of NAICS industry codes (2-6 digits) to filter by. Example: ["541511", "541512"] for custom programming and computer systems design.
- `pscCodes` (array): List of Product and Service Codes (PSC) to filter by. Example: ["D310", "R425"].
- `maxContracts` (integer; default 100): Maximum number of contract awards to save (1-1000), largest awards first. Each saved contract is one dataset item. Use 5-20 for quick answers.
- `minValue` (integer): Minimum award amount in USD. Example: 1000000 for awards of at least $1M.
- `maxValue` (integer): Maximum award amount in USD. Example: 50000000.
- `dateFrom` (string): Only contracts with a transaction on or after this date, format YYYY-MM-DD. Example: "2025-01-01". Defaults to 2020-01-01; the earliest supported date is 2007-10-01.
- `dateTo` (string): Only contracts with a transaction on or before this date, format YYYY-MM-DD. Example: "2025-12-31". Defaults to today.
- `setAsideType` (string; one of `SBA`, `8A`, `HUB`, `WOSB`, `SDVOSB`, `ISBEE`): Small business set-aside program. Empty string = all contracts. Example: "SDVOSB" for service-disabled veteran-owned small business set-asides.
- `includeContractorProfile` (boolean; default true): If true, adds a contractorProfile object with business types, certifications, total contract count, top agencies, top NAICS codes and recent contracts (one extra request per contract). Set false for faster runs.
- `includeSubawards` (boolean; default false): If true, adds a subawards list of subcontracts under each prime contract (one extra request per contract).
- `maxSubawards` (integer; default 10): Maximum subawards listed per contract (1-100) when includeSubawards is true. Example: 10.
- `includeTransactionHistory` (boolean; default false): If true, adds transactionHistory with up to the 100 most recent modifications and obligations per contract (one extra request per contract).
- `includeRelatedContracts` (boolean; default false): If true, adds relatedContracts: the largest other awards to the same contractor (one extra request per contract).
- `maxRelatedContracts` (integer; default 5): Maximum related contracts listed per contract (1-20) when includeRelatedContracts is true. Example: 5.
- `compactOutput` (boolean; default false): If true, each dataset item is a slim record with only key decision fields (award ID, title, agency, recipient, UEI, amount, dates, NAICS/PSC, set-aside, competition, URL) and counts instead of contractor profiles, subaward lists, transaction history and related contracts. Recommended for AI agents and MCP clients. If false, the full record is returned.

### Output fields

`awardId`, `piid`, `title`, `description`, `awardingAgency`, `awardingSubAgency`, `awardingOffice`, `fundingAgency`, `recipientName`, `recipientDuns`, `recipientUei`, `parentRecipientName`, `recipientLocation`, `recipientState`, `awardAmount`, `obligatedAmount`, `potentialValue`, `baseAndExercisedOptionsValue`, `totalOutlays`, `startDate`, `endDate`, `potentialEndDate`, `lastModifiedDate`, `signedDate`, `naicsCode`, `naicsDescription`, `pscCode`, `pscDescription`, `contractType`, `pricingType`, `awardType`, `parentAwardId`, `setAsideType`, `setAsideCode`, `competitionType`, `numberOfOffers`, `isCompetitive`, `subawardCount`, `totalSubawardAmount`, `placeOfPerformance`, `placeOfPerformanceState`, `contractorProfile`, `subawards`, `transactionHistory`, `relatedContracts`, `transactionCount`, `relatedContractsCount`, `contractorTotalContractsWon`, `contractorIsSmallBusiness`, `contractDurationDays`, `averageModificationAmount`, `contractHealth`, `url`, `scrapedAt`
