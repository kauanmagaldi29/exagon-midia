"""Lê pedido.json: {"buscas": [...], "escolhidas": [...ids]}.
Buscas -> miniaturas em thumbs/ + resultados.json. Escolhidas -> original em resolução máxima em originais/ + creditos.json.
Só fotos gratuitas (licença Unsplash), sem Unsplash+."""
import json, os, re, time, urllib.request, urllib.parse
D = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept': 'application/json'}
def get(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60); b = r.read()
    return b if binary else json.loads(b)
ped = json.load(open(os.path.join(D, 'pedido.json')))
res_path = os.path.join(D, 'resultados.json')
res = json.load(open(res_path)) if os.path.exists(res_path) else {}
os.makedirs(os.path.join(D, 'thumbs'), exist_ok=True); os.makedirs(os.path.join(D, 'originais'), exist_ok=True)
for q in ped.get('buscas', []):
    slug = re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')
    if slug in res: continue
    try:
        data = get('https://unsplash.com/napi/search/photos?' + urllib.parse.urlencode({'query': q, 'per_page': 24}))
    except Exception as e:
        print('erro busca', q, e); continue
    out = []
    for p in data.get('results', []):
        if p.get('premium') or p.get('plus') or p.get('sponsorship'): continue
        u = p['urls']; item = {'id': p['id'], 'w': p['width'], 'h': p['height'], 'desc': p.get('alt_description') or p.get('description'),
            'autor': p['user']['name'], 'autor_user': p['user']['username'], 'link': p['links']['html']}
        try:
            open(os.path.join(D, 'thumbs', f"{slug}__{p['id']}.jpg"), 'wb').write(get(u['small'], True)); out.append(item)
        except Exception as e: print('erro thumb', p['id'], e)
    res[slug] = out; print(q, len(out)); time.sleep(1)
json.dump(res, open(res_path, 'w'), ensure_ascii=False, indent=1)
cred_path = os.path.join(D, 'creditos.json')
cred = json.load(open(cred_path)) if os.path.exists(cred_path) else {}
for pid in ped.get('escolhidas', []):
    dest = os.path.join(D, 'originais', f'{pid}.jpg')
    if os.path.exists(dest): continue
    try:
        info = get(f'https://unsplash.com/napi/photos/{pid}')
        if info.get('premium') or info.get('plus'): print('pulado (Unsplash+)', pid); continue
        open(dest, 'wb').write(get(f'https://unsplash.com/photos/{pid}/download?force=true', True))
        cred[pid] = {'autor': info['user']['name'], 'link': info['links']['html'], 'w': info['width'], 'h': info['height']}
        print('baixada', pid, info['width'], 'x', info['height'])
    except Exception as e: print('erro original', pid, e)
json.dump(cred, open(cred_path, 'w'), ensure_ascii=False, indent=1)
