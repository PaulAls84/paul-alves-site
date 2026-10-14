#!/usr/bin/env python3
"""Helper: call WordPress REST routes through the WordPress MCP endpoint (JWT)."""
import json, sys, urllib.request
T = json.load(open('/Users/pleacompagnie/.claude.json'))['mcpServers']['wordpress-paul-alves']['env']['JWT_TOKEN']
URL = 'https://navajowhite-turkey-402641.hostingersite.com/wp-json/wp/v2/wpmcp'
def mcp(method, params=None):
    body = json.dumps({'method': method, 'params': params or {}}).encode()
    req = urllib.request.Request(URL, data=body, headers={'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)
def api(route, method='GET', data=None):
    args = {'route': route, 'method': method}
    if data is not None: args['data'] = data
    res = mcp('tools/call', {'name': 'run_api_function', 'arguments': args})
    txt = res.get('content', [{}])[0].get('text', '') if 'content' in res else json.dumps(res)
    try: return json.loads(txt)
    except Exception: return txt
if __name__ == '__main__':
    r = api(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'GET', json.loads(sys.argv[3]) if len(sys.argv) > 3 else None)
    print(json.dumps(r, ensure_ascii=False)[:int(sys.argv[4]) if len(sys.argv) > 4 else 3000])
