# Actor reference for b2b-lead-lists

Generated from the Actors' input schemas. Pass the input as the `input` object of the `run_data_source` tool, with the Actor name as `actor`.

## `ycombinator-scraper`

Store page: https://apify.com/artificially/ycombinator-scraper

### Input

- `searchQuery` (string): Free-text search over company name, one-liner, description, tags and industries, exactly like the search box on ycombinator.com/companies. Example: "ai agents" or "payments". Leave empty to list all companies that match the filters.
- `batches` (array): Keep companies from ANY of these YC batches. Accepts short codes (W24, S25, F24, P25 or X25 for Spring), full names ("Winter 2025", "Summer 2021") or a year ("2024" = every batch of that year). Example: ["W24", "Summer 2025"]. Leave empty for all batches.
- `industries` (array): Keep companies in ANY of these YC industries or sub-industries (case-insensitive). Top level: B2B, Consumer, Education, Fintech, Government, Healthcare, Industrials, Real Estate and Construction. Sub-industries include Engineering, Product and Design; Infrastructure; Security; Sales; Marketing; Analytics; Payments; Insurance; Healthcare IT; Therapeutics; Manufacturing and Robotics; Climate; Defense and more. Example: ["B2B", "Fintech"].
- `regions` (array): Keep companies in ANY of these YC regions (case-insensitive exact names from the directory). Examples: "United States of America", "America / Canada", "Europe", "United Kingdom", "Germany", "India", "Latin America", "Southeast Asia", "Remote", "Fully Remote", "Partly Remote". Example: ["Europe", "Canada"].
- `locations` (array): Keep companies whose location text or region contains ANY of these strings (case-insensitive substring). Use for cities, e.g. ["San Francisco", "New York", "London"]. Applied after the search, so it may need more scanning than the regions filter.
- `tags` (array): Keep companies with ANY of these YC tags (case-insensitive exact tag names). Examples: "Artificial Intelligence", "AI", "Generative AI", "SaaS", "Developer Tools", "Open Source", "Fintech", "Robotics", "Climate". Example: ["Developer Tools", "Open Source"].
- `status` (array; one of `Active`, `Acquired`, `Public`, `Inactive`): Keep companies with ANY of these statuses. Allowed values: Active, Acquired, Public, Inactive. Example: ["Active"]. Leave empty for all.
- `teamSizeMin` (integer): Keep companies with at least this many employees, as listed on YC. Example: 10.
- `teamSizeMax` (integer): Keep companies with at most this many employees, as listed on YC. Example: 50.
- `isHiring` (boolean; default false): Set to true to keep only companies YC marks as hiring (they have open roles on Work at a Startup). Combine with includeJobs to get the roles.
- `nonprofit` (boolean; default false): Set to true to keep only nonprofit YC companies.
- `topCompany` (boolean; default false): Set to true to keep only companies on YC's Top Companies list (e.g. Airbnb, Stripe, DoorDash).
- `sortBy` (string; default "relevance"; one of `relevance`, `launchDate`): relevance = the directory's default order (best search match first); launchDate = most recently launched first.
- `includeFounders` (boolean; default false): Set to true to add founders (name, title, bio, LinkedIn, X/Twitter) from each company's public YC page. Needs one extra page request per company, so runs are slower.
- `includeJobs` (boolean; default false): Set to true to add open roles (title, location, type, salary, equity, experience, visa, skills, URL) listed on each company's public YC page. Needs one extra page request per company; combine with isHiring to skip companies without jobs.
- `includeSocials` (boolean; default false): Set to true to add LinkedIn, X/Twitter, Facebook, Crunchbase and GitHub links plus year founded, city, country and YC partner from each company's YC page. Also filled automatically whenever includeFounders or includeJobs is on (same page request).
- `maxResults` (integer): Stop after saving this many companies. Example: 100. Leave empty for all matches (the run also stops at your maximum cost per run).
- `onlyNewSinceLastRun` (boolean; default false): Set to true to remember companies already returned for this exact search (query + filters) and return only companies you have not seen before. Ideal with Apify Schedules to catch each new batch: you pay only for new companies.
- `compactOutput` (boolean; default false): Set to true to save a slim item per company with only: name, slug, ycUrl, website, oneLiner, batch, status, industries, location, teamSize, isHiring, linkedin, founders (name, title, linkedin) and jobs (title, location, salary, url). Recommended when an AI agent or LLM reads the results. Leave false for the full item.

### Output fields

`ycId`, `name`, `slug`, `ycUrl`, `website`, `oneLiner`, `longDescription`, `batch`, `batchShort`, `status`, `stage`, `industry`, `industries`, `subindustry`, `tags`, `regions`, `location`, `city`, `country`, `teamSize`, `launchedAt`, `yearFounded`, `isHiring`, `topCompany`, `nonprofit`, `formerNames`, `logoUrl`, `primaryPartner`, `socials`, `linkedin`, `founders`, `jobs`, `jobCount`, `scrapedAt`

## `company-contact-extractor`

Store page: https://apify.com/artificially/company-contact-extractor

### Input

- `websites` (array, required): Required. One company website per entry: a bare domain (e.g. stripe.com), a domain with www (e.g. www.hetzner.com) or a full URL (e.g. https://apify.com or https://apify.com/contact to start on a specific page). http/https and www/non-www are resolved automatically and redirects are followed. Only the company's own website is crawled; do not enter LinkedIn, Facebook or Google Maps URLs. Example: ["stripe.com", "https://www.manufactum.de", "fancourier.ro"].
- `maxPagesPerDomain` (integer; default 10): How many pages to load per website, from 1 to 50, including the home page. The actor starts on the home page and then opens the most promising internal pages first (contact, imprint/Impressum, about, team, support, legal/privacy, careers; keywords in 20+ languages). Example: 5 for fast runs, 10 (default) for good coverage, 20 for large sites. More pages means more contacts but a slower run.
- `includeEmails` (boolean; default true): Collect email addresses from mailto: links, page text (including obfuscated forms like info [at] example [dot] com and Cloudflare-protected emails) and schema.org data. Set to false to skip emails.
- `emailFilter` (string; default "all"; one of `all`, `generic_only`, `exclude_generic`): Which emails to keep. "all" keeps every plausible email. "generic_only" keeps role addresses such as info@, sales@, contact@, support@, office@, press@ (safest for GDPR). "exclude_generic" keeps only addresses that look personal (e.g. jane.doe@). Each email in the output also carries type (generic or personal) so you can filter later.
- `includePhones` (boolean; default true): Collect phone numbers from tel: links, schema.org data and labeled text (e.g. "Tel.: 030 1234567", "Phone: +1 415 555 2671"). Numbers are validated and normalized to E.164 with libphonenumber, using the website's country (from the domain ending, address or page language) for local formats. Fax numbers are skipped. Set to false to skip phones.
- `includeSocials` (boolean; default true): Find the company's own profiles on LinkedIn, X/Twitter, Facebook, Instagram, YouTube, TikTok, GitHub and Crunchbase. Share buttons and unrelated profiles are ignored; when several profiles exist the one linked in the header/footer, in schema.org sameAs, or matching the domain name wins. Set to false to skip socials.
- `compactOutput` (boolean; default false): Set to true to save a slim item per domain: domain, companyName, emails (plain strings), phones (E.164 strings), socials (only the networks found) and contactPageUrl. Source URLs, email types, address and crawl stats are dropped. Recommended when an AI agent or LLM reads the results. Leave false for the full item.
- `sameDomainOnly` (boolean; default true): If true (default), only pages on the website's own host are crawled (www and non-www count as the same). Set to false to also follow links to subdomains of the same company domain, e.g. support.example.com or about.example.com. External websites are never crawled.
- `respectRobotsTxt` (boolean; default true): If true (default), pages disallowed by the website's robots.txt are not loaded, and domains that disallow everything are reported in FAILED_DOMAINS with reason blocked_by_robots. Set to false only if you have the right to crawl those pages.

### Output fields

`input`, `domain`, `websiteUrl`, `companyName`, `emails`, `phones`, `socials`, `contactPageUrl`, `contactFormUrl`, `address`, `pagesCrawled`, `scrapedAt`

## `website-tech-stack-detector`

Store page: https://apify.com/artificially/website-tech-stack-detector

### Input

- `websites` (array, required): Required. One company website per entry: a bare domain (e.g. allbirds.com), a domain with www (e.g. www.stripe.com) or a full URL (e.g. https://vercel.com or https://shop.example.com/de to start on a specific page). http/https and www/non-www are resolved automatically and redirects are followed. Example: ["allbirds.com", "stripe.com", "https://www.hubspot.com"].
- `maxPagesPerDomain` (integer; default 3): How many important internal pages to scan in addition to the home page, from 0 to 10. The actor picks at most one page per type from the home page links: pricing, careers, shop/collections, contact, demo/signup, blog, support, about, product. Different page types often load different tools (checkout, ATS, forms, chat). Example: 0 for the fastest run (home page only), 3 (default) for good coverage, 6 for deep scans.
- `includeDns` (boolean; default true): If true (default), also reads the domain's public DNS records: MX (email provider such as Google Workspace, Microsoft 365, Zoho, Proton), SPF includes and TXT verification records (e.g. HubSpot, Salesforce, Mailchimp, SendGrid, Atlassian, Stripe, Facebook, Zoom, DocuSign), DMARC reporting provider, nameservers (Cloudflare, Route 53, ...) and the website CNAME. Very cheap and a strong B2B signal. Set to false to analyze the website only.
- `categories` (array): Optional. Keep only technologies in these categories (case-insensitive, Wappalyzer category names). Leave empty to keep everything. Common names: Ecommerce, CMS, Page builders, Analytics, Advertising, Tag managers, CDN, Hosting, PaaS, Email, Webmail, Marketing automation, CRM, Live chat, Payment processors, JavaScript frameworks, Web frameworks, Cookie compliance, Security, Recruitment & staffing, Reviews, A/B Testing. Example: ["Ecommerce", "CMS", "Analytics"]. Domains with nothing left after filtering are not saved and not charged.
- `onlyDomainsUsing` (array): Optional lead filter. Save only domains that use at least one of these technologies (case-insensitive, names as they appear in the output). Domains that do not match are listed in FAILED_DOMAINS with reason no_matching_technology and are not charged. Example: ["Shopify"] for Shopify store leads, ["WordPress", "WooCommerce"], ["HubSpot"], ["Google Workspace"].
- `minConfidence` (integer; default 50): Drop detections below this confidence (0-100). Each fingerprint pattern carries a confidence and matches are added up per technology. 50 (default) removes weak single hints such as a URL merely allowed in a Content-Security-Policy header. Use 100 for only the most certain detections, 0 to keep everything.
- `compactOutput` (boolean; default false): Set to true to save a slim item per domain: domain, technologies (names only), highlights (cms, ecommerce, analytics, advertising, tagManagers, cdn, hosting, emailProvider, frameworks, chat, crm, payment) and emailProvider. Versions, confidence, evidence, DNS records and categories are dropped. Recommended when an AI agent or LLM reads the results. Leave false for the full item.
- `respectRobotsTxt` (boolean; default true): If true (default), pages disallowed by the website's robots.txt are not loaded, and websites that disallow everything are reported in FAILED_DOMAINS with reason blocked_by_robots. Set to false only if you have the right to scan those pages.

### Output fields

`input`, `domain`, `websiteUrl`, `finalUrl`, `siteStatus`, `title`, `technologies`, `byCategory`, `highlights`, `emailProvider`, `dns`, `pagesScanned`, `scrapedAt`
