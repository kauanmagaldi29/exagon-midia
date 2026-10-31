"""Artes da Exagon Digital (preto/branco, laranja só nos detalhes): 3 posts 1080x1350 + 3 stories 1080x1920."""
import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
FONTS = pathlib.Path(__file__).resolve().parent.parent / 'video' / 'node_modules' / '@fontsource' / 'outfit' / 'files'
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)
CSS = """
@font-face{font-family:Outfit;font-weight:400;src:url(FONTS/outfit-latin-400-normal.woff2)}
@font-face{font-family:Outfit;font-weight:500;src:url(FONTS/outfit-latin-500-normal.woff2)}
@font-face{font-family:Outfit;font-weight:600;src:url(FONTS/outfit-latin-600-normal.woff2)}
@font-face{font-family:Outfit;font-weight:700;src:url(FONTS/outfit-latin-700-normal.woff2)}
:root{--o:#FF4F1F;--mut:#8C8C8C}
*{box-sizing:border-box;margin:0}
body{width:Wpx;height:Hpx;overflow:hidden;font-family:Outfit,sans-serif;color:#fff;position:relative;background:radial-gradient(circle at 70% 20%,#1E1E1E 0%,#0E0E0E 55%,#080808 100%)}
body:before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.035) 2px,transparent 2px);background-size:90px 90px}
body.light{background:#F7F7F7;color:#111}
body.light:before{background-image:linear-gradient(rgba(0,0,0,.035) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.035) 2px,transparent 2px)}
.wrap{position:absolute;inset:0;padding:78px 76px}
.brand{display:flex;align-items:center;gap:16px;font-size:34px;font-weight:600;letter-spacing:-.01em}
h1{font-weight:700;letter-spacing:-.045em;line-height:.98}
.o{color:var(--o)}
.card{background:#171717;border:2px solid #2A2A2A;border-radius:36px}
.light .card{background:#fff;border:2px solid #E6E6E6;box-shadow:0 20px 50px rgba(0,0,0,.08)}
.num{width:76px;height:76px;border-radius:22px;border:3px solid var(--o);color:var(--o);font-size:40px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none}
.cta{position:absolute;left:76px;bottom:72px;display:inline-flex;align-items:center;gap:22px;height:100px;padding:0 16px 0 40px;border-radius:50px;background:#fff;color:#111;font-size:38px;font-weight:600}
.light .cta{background:#111;color:#fff}
.cta b{width:70px;height:70px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center}
.sm{font-size:30px;color:var(--mut);font-weight:500}
.ico{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
"""
MARK = '''<svg viewBox="0 0 120 104" style="width:WWpx;height:HHpx"><defs><mask id="xmID"><rect width="120" height="104" fill="#fff"/><rect x="74" y="18" width="50" height="68" fill="#000"/></mask></defs><path mask="url(#xmID)" fill-rule="evenodd" d="M120 51.96L90 103.92L30 103.92L0 51.96L30 0L90 0Z M99.21 51.96L79.6 85.92L40.4 85.92L20.79 51.96L40.4 18L79.6 18Z" fill="#FF4F1F"/><rect x="30" y="42.96" width="66" height="18" fill="#FF4F1F"/></svg>'''
def mark(w=52, uid='a'): return MARK.replace('WW', str(w)).replace('HH', str(round(w * 104 / 120))).replace('ID', uid)
def brand(): return f'<div class="brand">{mark(52)}<span>Exagon Digital</span></div>'
ARROW = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def cta(t): return f'<div class="cta">{t}<b>{ARROW}</b></div>'

P = {}
items = ['Abre em menos de 3 segundos', 'Aparece no Google quando te procuram', 'Leva o cliente pro WhatsApp em 1 toque', 'Guarda o contato e avisa sua equipe', 'Mostra quantas visitas viraram clientes']
bx = ''.join(f'<div style="display:flex;align-items:center;gap:26px;margin-top:{0 if i == 0 else 28}px"><span style="width:56px;height:56px;border-radius:14px;border:4px solid #444;flex:none"></span><span style="font-size:38px;font-weight:500">{t}</span></div>' for i, t in enumerate(items))
P['ex1'] = ('', f'''{brand()}
<h1 style="font-size:104px;margin-top:70px">Seu site trabalha ou só <span class="o">enfeita?</span></h1>
<div class="card" style="margin-top:56px;padding:46px 48px">{bx}</div>
<div style="margin-top:34px;font-size:40px;font-weight:600">Marcou menos de 4? <span class="o">Ele só enfeita.</span></div>
{cta('Chama no direct')}''')

sig = ['A mesma informação é digitada em 2 lugares', 'Só uma pessoa sabe onde está cada coisa', 'Um erro de fórmula já custou dinheiro', 'Você não sabe o número de hoje sem perguntar', 'Quando você sai, tudo para']
sg = ''.join(f'<div class="card" style="padding:18px 30px;display:flex;gap:26px;align-items:center;margin-top:{0 if i == 0 else 14}px"><span class="num">{i + 1}</span><span style="font-size:34px;font-weight:600;line-height:1.15">{t}</span></div>' for i, t in enumerate(sig))
P['ex2'] = ('light', f'''{brand()}
<h1 style="font-size:80px;margin-top:50px">5 sinais de que sua empresa já <span class="o">passou da planilha</span></h1>
<div style="margin-top:36px">{sg}</div>
{cta('Comenta SISTEMA')}''')

tasks = [('Responde clientes no WhatsApp', 'a qualquer hora, com as informações da sua empresa'), ('Lê pedidos, notas e e-mails', 'e lança tudo no sistema, sem digitação'), ('Monta o relatório do dia', 'e te manda pronto de manhã')]
tk = ''.join(f'<div class="card" style="padding:30px 36px;display:flex;gap:28px;align-items:center;margin-top:{0 if i == 0 else 20}px"><span class="num">{i + 1}</span><div><div style="font-size:40px;font-weight:600">{a}</div><div class="sm">{b}</div></div></div>' for i, (a, b) in enumerate(tasks))
P['ex3'] = ('', f'''{brand()}
<h1 style="font-size:94px;margin-top:70px">3 tarefas que a <span class="o">IA</span> já faz na sua empresa</h1>
<div style="margin-top:52px">{tk}</div>
<div style="margin-top:32px;font-size:38px;font-weight:500;color:#BDBDBD">Agentes de IA sob medida, ligados ao seu sistema.</div>
{cta('Comenta IA')}''')

S = {}
svc = [('Sistemas web sob medida', 'M3 5h18v12H3z M8 21h8 M12 17v4'), ('Aplicativos', 'M7 2h10v20H7z M11 18h2'), ('Automação no WhatsApp', 'M4 5h16v11H9l-5 4z'), ('Agentes de IA', 'M12 3v3 M12 18v3 M3 12h3 M18 12h3 M7 7h10v10H7z M10 11h.01 M14 11h.01'), ('Integração entre sistemas', 'M8 7h8 M8 17h8 M4 7a3 3 0 1 0 0 .01 M20 17a3 3 0 1 0 0 .01 M16 7l4 0 M4 17l4 0')]
sv = ''.join(f'<div class="card" style="padding:30px 36px;display:flex;gap:30px;align-items:center;margin-top:22px"><span style="width:86px;height:86px;border-radius:24px;background:#222;display:flex;align-items:center;justify-content:center;color:#FF4F1F"><svg viewBox="0 0 24 24" style="width:48px;height:48px"><path class="ico" d="{d}"/></svg></span><span style="font-size:46px;font-weight:600">{t}</span></div>' for t, d in svc)
S['es1'] = ('', f'''{brand()}
<div style="margin-top:150px;font-size:40px;font-weight:600;letter-spacing:.12em;color:var(--mut)">O QUE A GENTE FAZ</div>
<h1 style="font-size:104px;margin-top:24px">Tecnologia que <span class="o">trabalha por você</span></h1>
<div style="margin-top:50px">{sv}</div>
<div style="position:absolute;left:0;right:0;bottom:240px;text-align:center;font-size:44px;font-weight:600">Manda SISTEMA no direct</div>''')
S['es2'] = ('', f'''{brand()}
<div style="margin-top:220px;font-size:40px;font-weight:600;letter-spacing:.12em;color:var(--mut)">BASTIDORES</div>
<h1 style="font-size:116px;margin-top:30px">Software house da <span class="o">Serra Catarinense.</span></h1>
<div style="font-size:50px;line-height:1.3;margin-top:60px;color:#CFCFCF">Sistemas, aplicativos e IA sob medida, feitos em Lages (SC). E o projeto só termina quando você aprova a entrega.</div>
<div style="position:absolute;left:76px;bottom:240px;display:flex;align-items:center;gap:20px;font-size:56px;font-weight:600">{mark(80, 'b')}<span>Exagon Digital</span></div>''')
S['es3'] = ('light', f'''{brand()}
<h1 style="font-size:112px;margin-top:220px">Qual tarefa da sua empresa você queria que <span class="o">fizesse sozinha?</span></h1>
<div class="card" style="margin-top:90px;padding:50px 56px">
  <div class="sm" style="font-size:36px">Responde por mensagem</div>
  <div style="margin-top:22px;height:130px;border-radius:30px;background:#F2F2F2;display:flex;align-items:center;padding:0 40px;font-size:56px;font-weight:600;color:#B0B0B0">Ex.: lançar os pedidos...</div>
  <div style="margin-top:30px;font-size:42px;font-weight:500">e a gente te conta como automatizar.</div>
</div>''')

def html(w, h, body, cls=''):
    if h == 1920: body = '<div style="height:120px"></div>' + body
    css = CSS.replace('FONTS', FONTS.as_uri()).replace('Wpx', f'{w}px').replace('Hpx', f'{h}px')
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}"><div class="wrap">{body}</div></body></html>'
with sync_playwright() as p:
    b = p.chromium.launch()
    for d, (W, H) in [(P, (1080, 1350)), (S, (1080, 1920))]:
        for name, (cls, body) in d.items():
            pg = b.new_page(viewport={'width': W, 'height': H}); f = HERE / f'{name}.html'; f.write_text(html(W, H, body, cls))
            pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
            pg.screenshot(path=str(OUT / f'{name}.jpg'), type='jpeg', quality=92); pg.close()
    b.close()
print('ok')
