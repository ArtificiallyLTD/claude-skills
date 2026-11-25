#!/usr/bin/env python3
import json
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACTORS_DIR = os.environ.get('ACTORS_DIR', os.path.expanduser('~/Desktop/actors'))
SKILLS = {
    'linkedin-research': ['linkedin-profile-scraper', 'linkedin-company-scraper', 'linkedin-posts-scraper', 'linkedin-employees-scraper'],
    'us-government-contracts': ['samgov-opportunities-scraper', 'us-contracts-scraper'],
    'eu-public-tenders': ['eu-tenders-scraper'],
    'hiring-signals': ['linkedin-jobs-scraper', 'career-site-jobs-scraper'],
    'b2b-lead-lists': ['ycombinator-scraper', 'company-contact-extractor', 'website-tech-stack-detector'],
}
SKIP_INPUTS = {'proxyConfiguration', 'maxConcurrency', 'residentialFallback', 'maxAttemptsPerProfile', 'maxAttemptsPerCompany', 'maxAttemptsPerPage', 'maxAttempts', 'apiKey'}
EXTRA_OUTPUT = {
    'linkedin-profile-scraper': ['profileUrl', 'username', 'fullName', 'headline', 'location', 'about', 'connectionsCount', 'followersCount', 'currentCompany', 'experience', 'education', 'skills', 'certifications', 'languages', 'volunteerExperience', 'isRestricted', 'scrapedAt'],
}


def actor_reference(name):
    folder = os.path.join(ACTORS_DIR, name, '.actor')
    meta = json.load(open(os.path.join(folder, 'actor.json')))
    schema = json.load(open(os.path.join(folder, 'input_schema.json')))
    dataset = (meta.get('storages') or {}).get('dataset') or {}
    if isinstance(dataset, str):
        dataset = json.load(open(os.path.join(folder, dataset)))
    outputs = list(((dataset.get('fields') or {}).get('properties') or {}).keys()) or EXTRA_OUTPUT.get(name, [])
    required = set(schema.get('required') or [])
    lines = [f'## `{name}`', '', f'Store page: https://apify.com/artificially/{name}', '', '### Input', '']
    for key, prop in schema['properties'].items():
        if key in SKIP_INPUTS:
            continue
        kind = prop.get('type', '')
        allowed = prop.get('enum') or (prop['items'].get('enum') if isinstance(prop.get('items'), dict) else None)
        default = prop.get('default')
        bits = [kind + (', required' if key in required else '')]
        if default not in (None, '', []):
            bits.append(f'default {json.dumps(default)}')
        if allowed:
            bits.append('one of ' + ', '.join(f'`{a}`' for a in allowed if a != ''))
        description = ' '.join((prop.get('description') or '').split())
        lines.append(f"- `{key}` ({'; '.join(bits)}): {description}")
    lines += ['', '### Output fields', '', ', '.join(f'`{o}`' for o in outputs) if outputs else 'See the Store page.', '']
    return '\n'.join(lines)


def build():
    dist = os.path.join(ROOT, 'dist')
    shutil.rmtree(dist, ignore_errors=True)
    os.makedirs(dist)
    for skill, actors in SKILLS.items():
        folder = os.path.join(ROOT, 'skills', skill)
        if not os.path.exists(os.path.join(folder, 'SKILL.md')):
            sys.exit(f'{skill}: SKILL.md missing')
        os.makedirs(os.path.join(folder, 'references'), exist_ok=True)
        header = f'# Actor reference for {skill}\n\nGenerated from the Actors\' input schemas. Pass the input as the `input` object of the `run_data_source` tool, with the Actor name as `actor`.\n\n'
        with open(os.path.join(folder, 'references', 'actors.md'), 'w') as handle:
            handle.write(header + '\n'.join(actor_reference(a) for a in actors))
        with zipfile.ZipFile(os.path.join(dist, f'{skill}.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
            for base, _, files in os.walk(folder):
                for file in sorted(files):
                    if file.endswith('.pyc'):
                        continue
                    path = os.path.join(base, file)
                    archive.write(path, os.path.join(skill, os.path.relpath(path, folder)))
        print(f'{skill}: built')


if __name__ == '__main__':
    build()
