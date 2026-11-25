#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = 'https://api.apify.com/v2'
OWNER = 'artificially'


def token():
    value = os.environ.get('APIFY_TOKEN') or os.environ.get('APIFY_API_TOKEN')
    if value:
        return value.strip()
    path = os.path.expanduser('~/.apify/auth.json')
    if os.path.exists(path):
        try:
            with open(path) as handle:
                return json.load(handle).get('token', '').strip()
        except (OSError, ValueError):
            pass
    fail('No Apify API token found. Create a free account at https://console.apify.com/sign-up, copy the token from Settings > API & Integrations, and set it as the APIFY_TOKEN environment variable.')


def fail(message, code=1):
    print(json.dumps({'error': message}, indent=2))
    sys.exit(code)


def call(method, path, body=None):
    request = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json', 'User-Agent': 'artificially-claude-skills/1.0'},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors='replace')[:400]
            if error.code == 401:
                fail('Apify rejected the API token (401). Check APIFY_TOKEN.')
            if error.code == 402:
                fail('Apify says the account is out of credit or over its usage limit (402). Add credit or raise the limit at https://console.apify.com/billing.')
            if error.code == 400:
                fail(f'Apify rejected the input (400): {detail}')
            if error.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            fail(f'Apify API error {error.code}: {detail}')
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            fail(f'Could not reach api.apify.com: {error}. If you are in a sandbox, allow network access to api.apify.com.')


def load_input(raw):
    if raw.startswith('@'):
        with open(raw[1:]) as handle:
            return json.load(handle)
    try:
        return json.loads(raw)
    except ValueError as error:
        fail(f'--input is not valid JSON: {error}')


def fetch_items(dataset_id):
    items, offset = [], 0
    while True:
        page = call('GET', f'/datasets/{dataset_id}/items?clean=1&offset={offset}&limit=1000')
        items += page
        offset += len(page)
        if len(page) < 1000:
            return items


def shorten(value, limit=300):
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + '…'
    if isinstance(value, list):
        return [shorten(v, limit) for v in value[:5]] + ([f'…{len(value) - 5} more'] if len(value) > 5 else [])
    if isinstance(value, dict):
        return {k: shorten(v, limit) for k, v in value.items()}
    return value


def summarize(run, items, out_path, fields, preview):
    rows = items[:preview]
    if fields:
        rows = [{f: item.get(f) for f in fields} for item in rows]
    return {
        'actor': run.get('_actor'),
        'runId': run['id'],
        'status': run['status'],
        'statusMessage': run.get('statusMessage'),
        'itemCount': len(items),
        'outputFile': out_path,
        'runUrl': f"https://console.apify.com/actors/runs/{run['id']}",
        'preview': [shorten(r) for r in rows],
    }


def write_items(actor, run_id, items, out_path):
    path = out_path or os.path.join('apify-output', f'{actor}-{run_id}.json')
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, 'w') as handle:
        json.dump(items, handle, ensure_ascii=False, indent=1)
    return path


def wait(run, max_wait):
    deadline = time.time() + max_wait
    while run['status'] in ('READY', 'RUNNING') and time.time() < deadline:
        run = call('GET', f"/actor-runs/{run['id']}?waitForFinish={min(60, max(1, int(deadline - time.time())))}")['data']
    return run


def main():
    parser = argparse.ArgumentParser(description='Run an Artificially Apify Actor and save its results.')
    sub = parser.add_subparsers(dest='command', required=True)
    run_cmd = sub.add_parser('run', help='Start an Actor run and wait for its results')
    run_cmd.add_argument('actor', help='Actor name, e.g. linkedin-jobs-scraper')
    run_cmd.add_argument('--input', required=True, help='Input as JSON text, or @path/to/input.json')
    run_cmd.add_argument('--max-wait', type=int, default=600, help='Seconds to wait before returning a RUNNING run (default 600)')
    run_cmd.add_argument('--out', help='Where to save all items as JSON (default apify-output/<actor>-<runId>.json)')
    run_cmd.add_argument('--fields', help='Comma-separated fields to show in the preview')
    run_cmd.add_argument('--preview', type=int, default=3, help='How many items to print (default 3)')
    res_cmd = sub.add_parser('results', help='Wait for an earlier run and save its results')
    res_cmd.add_argument('run_id')
    res_cmd.add_argument('--max-wait', type=int, default=600)
    res_cmd.add_argument('--out')
    res_cmd.add_argument('--fields')
    res_cmd.add_argument('--preview', type=int, default=3)
    args = parser.parse_args()

    if args.command == 'run':
        actor = args.actor.split('/')[-1].split('~')[-1]
        run = call('POST', f'/acts/{OWNER}~{actor}/runs?waitForFinish=60', load_input(args.input))['data']
    else:
        run = call('GET', f'/actor-runs/{args.run_id}')['data']
        actor = call('GET', f"/acts/{run['actId']}")['data']['name']
    run = wait(run, args.max_wait)
    run['_actor'] = actor
    fields = [f.strip() for f in args.fields.split(',')] if args.fields else None
    if run['status'] in ('READY', 'RUNNING'):
        print(json.dumps({'actor': actor, 'runId': run['id'], 'status': run['status'], 'note': f"Still running. Fetch the results later with: apify_run.py results {run['id']}"}, indent=2))
        return
    items = fetch_items(run['defaultDatasetId'])
    out_path = write_items(actor, run['id'], items, args.out)
    print(json.dumps(summarize(run, items, out_path, fields, args.preview), indent=2, ensure_ascii=False))


TOKEN = None
if __name__ == '__main__':
    TOKEN = token()
    main()
