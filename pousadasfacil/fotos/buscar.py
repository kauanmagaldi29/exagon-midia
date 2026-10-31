"""Lê pedido.json: {"buscas": [...], "escolhidas": [...]}.
Buscas -> miniaturas em thumbs/ + resultados.json (Unsplash; se falhar, Openverse com licença comercial).
Escolhidas ("unsplash:ID" ou "openverse:ID") -> original em resolução máxima em originais/ + creditos.json.
Tudo que acontece fica em log.txt."""
import json, os, re, time, urllib.request, urllib.parse, traceback
D = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(D, 'log.txt'), 'w')
def log(*a): s = ' '.join(str(x) for x in a); print(s); LOG.write(s + '\n'); LOG.flush()
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept': 'application/json, image/*, */*', 'Accept-Language': 'en-US,en;q=0.9'}
def get(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60); b = r.read()
    return b if binary else json.loads(b)
def save(url, path):
    open(path, 'wb').write(get(url, True))
ped = json.load(open(os.path.join(D, 'pedido.json')))
res_path = os.path.join(D, 'resultados.json')
res = json.load(open(res_path)) if os.path.exists(res_path) else {}
os.makedirs(os.path.join(D, 'thumbs'), exist_ok=True); os.makedirs(os.path.join(D, 'originais'), exist_ok=True)
def unsplash(q):
    data = get('https://unsplash.com/napi/search/photos?' + urllib.parse.urlencode({'query': q, 'per_page': 24}))
    out = []
    for p in data.get('results', []):
        if p.get('premium') or p.get('plus') or p.get('sponsorship'): continue
        out.append({'id': 'unsplash:' + p['id'], 'w': p['width'], 'h': p['height'], 'desc': p.get('alt_description') or p.get('description'),
                    'autor': p['user']['name'], 'link': p['links']['html'], 'licenca': 'Unsplash', 'thumb': p['urls']['small']})
    return out
def openverse(q):
    data = get('https://api.openverse.org/v1/images/?' + urllib.parse.urlencode({'q': q, 'license_type': 'commercial,modification', 'category': 'photograph', 'page_size': 20, 'mature': 'false'}))
    out = []
    for p in data.get('results', []):
        out.append({'id': 'openverse:' + p['id'], 'w': p.get('width'), 'h': p.get('height'), 'desc': p.get('title'), 'autor': p.get('creator'),
                    'link': p.get('foreign_landing_url'), 'licenca': f"{p.get('license')} {p.get('license_version')}", 'fonte': p.get('source'),
                    'url': p.get('url'), 'thumb': p.get('thumbnail')})
    return out
for q in ped.get('buscas', []):
    slug = re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')
    if res.get(slug): continue
    out = []
    for fn in ((openverse,) if ped.get('so_openverse') else (unsplash, openverse)):
        try:
            out = fn(q); log(fn.__name__, q, len(out))
            if out: break
        except Exception as e: log('ERRO', fn.__name__, q, repr(e))
    ok = []
    for it in out:
        try: save(it['thumb'], os.path.join(D, 'thumbs', f"{slug}__{it['id'].replace(':', '_')}.jpg")); ok.append(it)
        except Exception as e: log('ERRO thumb', it['id'], repr(e))
    res[slug] = ok; time.sleep(1)
json.dump(res, open(res_path, 'w'), ensure_ascii=False, indent=1)
cred_path = os.path.join(D, 'creditos.json')
cred = json.load(open(cred_path)) if os.path.exists(cred_path) else {}
allitems = {it['id']: it for v in res.values() for it in v}
for pid in ped.get('escolhidas', []):
    src, _, i = pid.partition(':'); dest = os.path.join(D, 'originais', f'{src}_{i}.jpg')
    if os.path.exists(dest): continue
    try:
        if src == 'unsplash':
            info = get(f'https://unsplash.com/napi/photos/{i}')
            if info.get('premium') or info.get('plus'): log('pulado Unsplash+', i); continue
            save(f'https://unsplash.com/photos/{i}/download?force=true', dest)
            cred[pid] = {'autor': info['user']['name'], 'link': info['links']['html'], 'w': info['width'], 'h': info['height'], 'licenca': 'Unsplash'}
        else:
            it = allitems.get(pid) or {}
            info = get(f'https://api.openverse.org/v1/images/{i}/')
            save(info['url'], dest)
            cred[pid] = {'autor': info.get('creator'), 'link': info.get('foreign_landing_url'), 'w': info.get('width'), 'h': info.get('height'), 'licenca': f"{info.get('license')} {info.get('license_version')}"}
        log('baixada', pid, os.path.getsize(dest))
    except Exception as e: log('ERRO original', pid, repr(e))
json.dump(cred, open(cred_path, 'w'), ensure_ascii=False, indent=1)
