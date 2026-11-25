# Actor reference for linkedin-research

Generated from the Actors' input schemas. Pass the input as the `input` object of the `run_data_source` tool, with the Actor name as `actor`.

## `linkedin-profile-scraper`

Store page: https://apify.com/artificially/linkedin-profile-scraper

### Input

- `profileUrls` (array): LinkedIn public profile URLs to scrape, one per line, e.g. "https://www.linkedin.com/in/williamhgates". Accepts full /in/ URLs with or without trailing slash or query string. Provide this and/or usernames; at least one profile is required.
- `usernames` (array): LinkedIn profile usernames (the vanity slug after /in/), one per line, e.g. "williamhgates". Use instead of or together with profileUrls; duplicates are removed.
- `includeExperience` (boolean; default true): If true, include the work history array (title, company, companyUrl, location, dates, description) in each item.
- `includeEducation` (boolean; default true): If true, include the education array (school, degree, field of study, dates) in each item.
- `includeSkills` (boolean; default true): If true, include the list of skills shown on the public profile.
- `includeCertifications` (boolean; default true): If true, include licenses and certifications (name, issuing organization, issue date, credential ID).
- `includeLanguages` (boolean; default true): If true, include the list of languages shown on the profile.
- `includeVolunteer` (boolean; default false): If true, include volunteer experience entries. Off by default.
- `compactOutput` (boolean; default false): If true, save a slimmer item per profile with only: profileUrl, username, fullName, headline, location, currentCompany, connectionsCount, followersCount, experience (title, company, companyUrl, startDate, endDate), education (school, degree, fieldOfStudy, dates), skills, languages, isRestricted (plus companies for restricted profiles). Drops photos, about text, descriptions, certifications and volunteer data. Recommended for AI agents and LLM pipelines. Default false keeps the full item.
- `includeRestrictedProfiles` (boolean; default false): LinkedIn shows logged-out visitors a restricted version of many ordinary profiles, with the headline, job titles and skills hidden. By default these are skipped and not charged. If true, restricted profiles are saved with the partial public data they still show (name, location, current company, companies worked at, schools, about, follower and connection counts, photo, certifications) and flagged isRestricted: true. They never include headline, job titles, experience entries or skills. They go to a separate "Restricted profiles" dataset (see the Output tab) and are charged at the lower restricted-profile price shown on the Pricing tab. Profiles without a real name plus at least a location, company or school are still skipped for free.

### Output fields

`profileUrl`, `username`, `fullName`, `headline`, `location`, `about`, `connectionsCount`, `followersCount`, `currentCompany`, `experience`, `education`, `skills`, `certifications`, `languages`, `volunteerExperience`, `isRestricted`, `scrapedAt`

## `linkedin-company-scraper`

Store page: https://apify.com/artificially/linkedin-company-scraper

### Input

- `companyUrls` (array): LinkedIn company page URLs to scrape, one per line, e.g. "https://www.linkedin.com/company/stripe". Also accepts /school/ and /showcase/ URLs. Provide this and/or companyIds; at least one company is required.
- `companyIds` (array): LinkedIn company slugs (the part after /company/ in the URL), one per line, e.g. "stripe". Use instead of or together with companyUrls; duplicates are removed.
- `includeLocations` (boolean; default true): If true, include the office locations array (address, city, country, isHeadquarters).
- `includeSpecialties` (boolean; default true): If true, include the list of company specialties (focus areas), e.g. ["Payments", "Fintech"].
- `includeFunding` (boolean; default true): If true, include funding info (total funding, last round, round date, investors) when LinkedIn shows it; null otherwise.
- `includeSimilarCompanies` (boolean; default false): If true, include the "similar pages" companies LinkedIn shows (name, url, industry, location). Off by default.
- `compactOutput` (boolean; default false): If true, save a slimmer item per company with only: companyUrl, companyId, name, tagline, website, industry, companySize, employeeCount, employeeCountOnLinkedIn, headquarters, foundedYear, type, specialties, followerCount, totalFunding, lastFundingRound. Drops the long description, logo and cover image URLs, locations and similar companies. Recommended for AI agents and LLM pipelines. Default false keeps the full item.

### Output fields

`companyUrl`, `companyId`, `name`, `tagline`, `description`, `website`, `industry`, `companySize`, `employeeCount`, `employeeCountOnLinkedIn`, `headquarters`, `foundedYear`, `type`, `logo`, `backgroundImage`, `specialties`, `locations`, `funding`, `similarCompanies`, `followerCount`, `scrapedAt`

## `linkedin-posts-scraper`

Store page: https://apify.com/artificially/linkedin-posts-scraper

### Input

- `companyUrls` (array): LinkedIn company page URLs whose recent public posts to scrape, one per line, e.g. "https://www.linkedin.com/company/stripe". Also accepts /showcase/ URLs. Provide this and/or companyIds; at least one company is required. Keyword or hashtag search is not supported.
- `companyIds` (array): LinkedIn company slugs (the part after /company/ in the URL), one per line, e.g. "stripe". Use instead of or together with companyUrls; duplicates are removed.
- `maxPosts` (integer; default 20): Maximum number of posts to save per company. Integer 1-100, e.g. 5. Without login LinkedIn shows only the most recent posts on the public page, typically up to about 10.
- `compactOutput` (boolean; default false): If true, save a slimmer item per post with only: postId, postUrl, authorName, text, timestamp, likeCount, commentCount, repostCount, mediaType, isRepost, companyName, companyId. Drops the author object (headline, photo), media and article URLs, hashtags, mentions, relative time and scrapedAt. Recommended for AI agents and LLM pipelines. Default false keeps the full item.

### Output fields

`postId`, `postUrl`, `author`, `authorName`, `text`, `timestamp`, `relativeTime`, `likeCount`, `commentCount`, `repostCount`, `mediaType`, `mediaUrl`, `articleTitle`, `articleLink`, `hashtags`, `mentions`, `isRepost`, `companyName`, `companyUrl`, `companyId`, `scrapedAt`

## `linkedin-employees-scraper`

Store page: https://apify.com/artificially/linkedin-employees-scraper

### Input

- `companyUrls` (array): LinkedIn company page URLs whose employees to list, one per line, e.g. "https://www.linkedin.com/company/stripe". Provide this and/or companyIds; at least one company is required.
- `companyIds` (array): LinkedIn company slugs (the part after /company/ in the URL), one per line, e.g. "stripe". Use instead of or together with companyUrls; duplicates are removed.
- `maxEmployees` (integer; default 50): Maximum number of employees to save per company. Integer 1-100, e.g. 10. Without login only the employees LinkedIn features on the public company page are available, typically fewer than 20 per company.
- `scrapeFullProfiles` (boolean; default true): If true, open each employee's public profile to get their current headline and location (slower, one extra request per employee). If false, return only the name, title and photo shown on the company page (fast).
- `compactOutput` (boolean; default false): If true, save a slimmer item per employee with only: profileUrl, username, fullName, title, location, companyName, companyId. Drops the photo URL, company URL, connectionDegree and scrapedAt. Recommended for AI agents and LLM pipelines. Default false keeps the full item.

### Output fields

`profileUrl`, `username`, `fullName`, `title`, `location`, `profilePhoto`, `connectionDegree`, `companyName`, `companyUrl`, `companyId`, `scrapedAt`
