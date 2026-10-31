"""Gera as artes da semana (posts 1080x1350, stories 1080x1920) no estilo verde/laranja do reel 'não evolui'."""
import pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
FONTS = pathlib.Path(__file__).resolve().parent.parent / 'video' / 'node_modules' / '@fontsource' / 'outfit' / 'files'
OUT = HERE / 'out'; OUT.mkdir(exist_ok=True)

CSS = """
@font-face{font-family:Outfit;font-weight:400;src:url(FONTS/outfit-latin-400-normal.woff2)}
@font-face{font-family:Outfit;font-weight:500;src:url(FONTS/outfit-latin-500-normal.woff2)}
@font-face{font-family:Outfit;font-weight:600;src:url(FONTS/outfit-latin-600-normal.woff2)}
@font-face{font-family:Outfit;font-weight:700;src:url(FONTS/outfit-latin-700-normal.woff2)}
:root{--g:#1F4D3A;--g2:#2E6B4F;--lg:#E4EEDF;--o:#FF4F1F;--ink:#151515;--mut:#857F76}
*{box-sizing:border-box;margin:0}
body{width:Wpx;height:Hpx;overflow:hidden;font-family:Outfit,sans-serif;color:var(--ink);position:relative;
  background:radial-gradient(circle at 50% 30%,#FFFFFF 0%,#F5F1EA 50%,#E8E2D8 100%)}
body:before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(31,77,58,.10) 2px,transparent 2.4px);background-size:44px 44px;opacity:.5}
.dark{background:linear-gradient(165deg,#2A6249 0%,#1F4D3A 55%,#173B2C 100%);color:#fff}
.dark:before{background-image:radial-gradient(rgba(255,255,255,.07) 2px,transparent 2.4px)}
.wrap{position:absolute;inset:0;padding:78px 76px}
.brand{display:flex;align-items:center;gap:16px;font-size:32px;font-weight:600;letter-spacing:-.01em}
.brand .by{font-weight:500;color:var(--mut);margin-left:4px}
.dark .brand .by{color:rgba(255,255,255,.6)}
.pf{width:46px;height:46px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center;flex:none}
.pf i{width:16px;height:16px;border-radius:50%;background:#151515}
h1{font-weight:700;letter-spacing:-.045em;line-height:.98}
.o{color:var(--o)} .g{color:var(--g)}
.card{background:#fff;border-radius:40px;box-shadow:0 26px 60px rgba(50,38,24,.13),0 4px 14px rgba(50,38,24,.06)}
.chip{display:inline-flex;align-items:center;gap:16px;height:84px;padding:0 34px 0 18px;border-radius:42px;background:#fff;font-weight:600;font-size:34px;white-space:nowrap;box-shadow:0 14px 34px rgba(50,38,24,.12)}
.dot{width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}
.dot svg{width:32px;height:32px}
.cta{position:absolute;left:76px;bottom:72px;display:inline-flex;align-items:center;gap:22px;height:100px;padding:0 16px 0 40px;border-radius:50px;background:#151515;color:#fff;font-size:38px;font-weight:600}
.cta b{width:70px;height:70px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center}
.dark .cta{background:#fff;color:#151515}
.mark{position:absolute;right:76px;bottom:96px;display:flex;align-items:center;gap:12px;font-size:36px;font-weight:600}
.row{display:flex;align-items:center;gap:26px;font-size:40px;font-weight:500}
.ico{fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.sm{font-size:30px;color:var(--mut);font-weight:500}
"""

EXAGON = '''<svg viewBox="0 0 120 104" style="width:46px;height:40px"><defs><mask id="xm"><rect width="120" height="104" fill="#fff"/><rect x="74" y="18" width="50" height="68" fill="#000"/></mask></defs><path mask="url(#xm)" fill-rule="evenodd" d="M120 51.96L90 103.92L30 103.92L0 51.96L30 0L90 0Z M99.21 51.96L79.6 85.92L40.4 85.92L20.79 51.96L40.4 18L79.6 18Z" fill="#FF4F1F"/><rect x="30" y="42.96" width="66" height="18" fill="#FF4F1F"/></svg>'''
ARROW = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHECK = lambda c='#1F4D3A', w=2.8: f'<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
XMARK = lambda c='#fff': f'<svg viewBox="0 0 24 24"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11" fill="none" stroke="{c}" stroke-width="2.8" stroke-linecap="round"/></svg>'
WARN = '<svg viewBox="0 0 24 24"><path d="M12 4 21.5 20h-19z M12 10v4.5 M12 17.5v.3" fill="none" stroke="#000" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
USER = '<svg viewBox="0 0 24 24"><g class="ico" style="color:#1F4D3A"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></g></svg>'

def brand(): return '<div class="brand"><span class="pf"><i></i></span>Pousadas Fácil<span class="by">· por Exagon</span></div>'
def mark(): return f'<div class="mark">{EXAGON}<span>Exagon</span></div>'
def cta(t): return f'<div class="cta">{t}<b>{ARROW}</b></div>'

def lock(code='1234', w=250):
    h = int(w * 1.8)
    dots = ''.join('<i style="width:38px;height:38px;border-radius:50%;background:#333"></i>' for _ in range(9))
    return f'''<div style="width:{w}px;height:{h}px;border-radius:48px;background:linear-gradient(170deg,#2A2A2A,#151515);box-shadow:0 30px 70px rgba(0,0,0,.28);padding:38px 30px">
      <div style="height:100px;border-radius:22px;background:#0B0B0B;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:62px;letter-spacing:.05em;color:#FF7A45">{code}</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:34px;justify-items:center">{dots}</div>
      <div style="margin:28px auto 0;width:60px;height:10px;border-radius:5px;background:#FF4F1F"></div></div>'''

# ------------------------------------------------------------------ POSTS (1080x1350)
P = {}
P['p1'] = f'''{brand()}
<h1 style="font-size:92px;margin-top:70px">Quanto o feriadão te custou em <span class="o">comissão?</span></h1>
<div class="card" style="margin-top:56px;padding:44px 50px">
  <div style="display:flex;justify-content:space-between;align-items:center"><span class="sm">Faça a conta</span><span class="chip" style="height:56px;font-size:26px;padding:0 24px;background:#F2EEE7;box-shadow:none">exemplo</span></div>
  <div class="row" style="justify-content:space-between;margin-top:30px"><span>Reservas pela plataforma</span><b>10</b></div>
  <div style="height:3px;background:#F0EBE4;margin:24px 0"></div>
  <div class="row" style="justify-content:space-between"><span>Valor de cada reserva</span><b>R$ 560</b></div>
  <div style="height:3px;background:#F0EBE4;margin:24px 0"></div>
  <div class="row" style="justify-content:space-between"><span>Comissão</span><b>15%</b></div>
  <div style="margin-top:34px;border-radius:28px;background:#FFF0EA;padding:26px 34px;display:flex;justify-content:space-between;align-items:center">
    <span style="font-size:36px;font-weight:600;color:#B9381A">Foi pra plataforma</span><span style="font-size:76px;font-weight:700;color:var(--o);letter-spacing:-.03em">R$ 840</span></div>
</div>
{cta('Comenta QUERO')}{mark()}'''

P['p2'] = f'''{brand()}
<h1 style="font-size:86px;margin-top:70px">Fechadura com a mesma senha é só uma <span class="o">chave mais cara.</span></h1>
<div style="display:flex;gap:44px;margin-top:60px;align-items:flex-start">
  {lock('1234', 250)}
  <div style="display:flex;flex-direction:column;gap:22px;flex:1;margin-top:10px">
    <div class="card" style="padding:28px 30px;display:flex;gap:22px;align-items:center"><span class="dot" style="background:var(--o)">{WARN}</span><span style="font-size:36px;font-weight:600;line-height:1.1">Senha igual há meses</span></div>
    <div class="card" style="padding:28px 30px;display:flex;gap:22px;align-items:center"><span class="dot" style="background:var(--o)">{WARN}</span><span style="font-size:36px;font-weight:600;line-height:1.1">Ex-hóspede ainda sabe entrar</span></div>
    <div class="card" style="padding:28px 30px;display:flex;gap:22px;align-items:center"><span class="dot" style="background:var(--o)">{WARN}</span><span style="font-size:36px;font-weight:600;line-height:1.1">Troca manual, porta por porta</span></div>
  </div>
</div>
{cta('Salve este post')}{mark()}'''

boxes = ''.join(f'<div class="row" style="margin-top:{0 if i == 0 else 26}px"><span style="width:58px;height:58px;border-radius:16px;border:4px solid #D9D2C7;flex:none"></span><span style="font-size:38px">{t}</span></div>'
                for i, t in enumerate(['Mostra a disponibilidade na hora', 'Responde a dúvida na hora', 'Recebe por PIX ou cartão', 'Confirma a reserva sozinho', 'Envia as instruções de chegada']))
P['p3'] = f'''{brand()}
<h1 style="font-size:100px;margin-top:70px">Seu site é vitrine ou <span class="o">vendedor?</span></h1>
<div class="card" style="margin-top:56px;padding:46px 50px">{boxes}</div>
<div style="margin-top:34px;font-size:40px;font-weight:600">Marcou menos de 4? <span class="o">É só vitrine.</span></div>
{cta('Comenta QUERO')}{mark()}'''

steps = [('Reserva e paga no seu site', 'sem comissão'), ('Recebe a senha da porta', 'no WhatsApp'), ('Chegou tarde? Check-in no totem', 'a qualquer hora'), ('No check-out, a senha expira', 'sozinha')]
st = ''.join(f'<div class="card" style="padding:26px 34px;display:flex;gap:28px;align-items:center;margin-top:{0 if i == 0 else 20}px"><span style="width:76px;height:76px;border-radius:24px;background:var(--g);color:#fff;font-size:42px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none">{i + 1}</span><div><div style="font-size:38px;font-weight:600">{a}</div><div class="sm">{b}</div></div></div>' for i, (a, b) in enumerate(steps))
P['p4'] = f'''{brand()}
<h1 style="font-size:84px;margin-top:66px">Do celular até a porta do quarto, <span class="o">sem recepção.</span></h1>
<div style="margin-top:50px">{st}</div>
{cta('Comenta QUERO')}{mark()}'''

def bub(q, a, t):
    return f'''<div style="display:flex;justify-content:flex-end;margin-top:22px"><span style="background:#F1EDE7;border-radius:28px;padding:16px 28px;font-size:36px">{q}</span></div>
    <div style="display:flex;align-items:flex-end;gap:14px;margin-top:12px"><span style="background:var(--g);color:#fff;border-radius:28px;padding:16px 28px;font-size:36px">{a}</span><span class="sm" style="font-size:24px">{t}</span></div>'''
P['p5'] = f'''{brand()}
<h1 style="font-size:96px;margin-top:70px">3 perguntas que chegam <span class="o">às 23h</span></h1>
<div class="card" style="margin-top:48px;padding:34px 40px 40px">
  <div class="sm" style="display:flex;align-items:center;gap:14px">WhatsApp da pousada · resposta automática</div>
  {bub('Tem vaga pra amanhã?', 'Tem! Já te mandei o link.', '23:02')}
  {bub('Aceita pet?', 'Aceitamos, com aviso prévio.', '23:05')}
  {bub('Que horas é o check-in?', 'A partir das 14h, pelo totem.', '23:09')}
</div>
{cta('Comenta QUERO')}{mark()}'''

offers = [('Pacote de verão', 'pagamento antecipado garante o seu caixa'), ('Vale-hospedagem', 'presente de Natal que já entra no caixa'), ('Cupom no seu site', 'só pra quem reserva direto, sem plataforma')]
of = ''.join(f'<div class="card" style="padding:28px 34px;display:flex;gap:26px;align-items:center;margin-top:{0 if i == 0 else 20}px"><span style="width:76px;height:76px;border-radius:50%;background:{"var(--o)" if i == 2 else "var(--lg)"};font-size:40px;font-weight:700;color:{"#000" if i == 2 else "var(--g)"};display:flex;align-items:center;justify-content:center;flex:none">{i + 1}</span><div><div style="font-size:40px;font-weight:600">{a}</div><div class="sm">{b}</div></div></div>' for i, (a, b) in enumerate(offers))
P['p6'] = f'''{brand()}
<div class="chip" style="margin-top:60px;height:70px;font-size:30px;background:#151515;color:#fff;padding:0 30px">Black Friday · 27 de novembro</div>
<h1 style="font-size:92px;margin-top:30px">3 ofertas pra sua pousada <span class="o">vender direto</span></h1>
<div style="margin-top:46px">{of}</div>
{cta('Salve este post')}{mark()}'''

def cmp_row(a, b, last=False):
    bd = '' if last else 'border-bottom:3px solid #F0EBE4;'
    return f'''<div style="display:flex;{bd}">
      <div style="flex:1;padding:26px 30px;display:flex;gap:16px;align-items:center;font-size:32px;color:#6E685F"><span class="dot" style="width:46px;height:46px;background:#E2DCD2">{XMARK("#6E685F")}</span>{a}</div>
      <div style="flex:1;padding:26px 30px;display:flex;gap:16px;align-items:center;font-size:32px;font-weight:600;background:#F7FBF5"><span class="dot" style="width:46px;height:46px;background:var(--g)">{CHECK("#fff")}</span>{b}</div></div>'''
P['p7'] = f'''{brand()}
<h1 style="font-size:100px;margin-top:70px">Recepção 24h ou <span class="o">totem?</span></h1>
<div class="card" style="margin-top:52px;overflow:hidden">
  <div style="display:flex;font-size:30px;font-weight:600;letter-spacing:.08em"><div style="flex:1;padding:26px 30px;color:var(--mut)">RECEPÇÃO 24H</div><div style="flex:1;padding:26px 30px;background:var(--g);color:#fff">TOTEM</div></div>
  {cmp_row('Salário e encargos', 'Sem folha de pagamento')}
  {cmp_row('Hora extra e feriado', 'Funciona 24 horas')}
  {cmp_row('Alguém acordado', 'Check-in sozinho')}
  {cmp_row('Fila na chegada', 'Senha no celular', True)}
</div>
{cta('Comenta QUERO')}{mark()}'''

# ------------------------------------------------------------------ STORIES (1080x1920)
S = {}
cover = (HERE / 'capa-reel.png').as_uri()
S['s1'] = ('', f'''{brand()}
<div class="chip" style="margin-top:110px;height:76px;font-size:32px;background:var(--o);color:#000;padding:0 34px">Vídeo novo no perfil</div>
<div style="margin:50px auto 0;width:620px;height:1102px;border-radius:44px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.25);background:url({cover}) center/cover"></div>
<div style="margin-top:56px;text-align:center;font-size:52px;font-weight:600">Toca no perfil e assiste</div>''')

opts = ['Responder o WhatsApp', 'Chave e senha das portas', 'Hóspede de madrugada', 'Comissão das plataformas']
op = ''.join(f'<div class="card" style="padding:34px 40px;display:flex;gap:30px;align-items:center;margin-top:24px"><span style="width:84px;height:84px;border-radius:24px;background:var(--lg);color:var(--g);font-size:46px;font-weight:700;display:flex;align-items:center;justify-content:center">{i + 1}</span><span style="font-size:46px;font-weight:600">{t}</span></div>' for i, t in enumerate(opts))
S['s2'] = ('', f'''{brand()}
<h1 style="font-size:104px;margin-top:150px">O que mais te dá <span class="o">trabalho</span> na pousada?</h1>
<div style="margin-top:70px">{op}</div>
<div style="position:absolute;left:0;right:0;bottom:240px;text-align:center;font-size:44px;font-weight:600">Responda com o número por mensagem</div>''')

S['s3'] = ('dark', f'''{brand()}
<div style="margin-top:170px;font-size:44px;font-weight:600;letter-spacing:.12em;color:rgba(255,255,255,.65)">VOCÊ SABIA?</div>
<h1 style="font-size:96px;margin-top:30px">Numa reserva de R$&nbsp;560, a plataforma fica com</h1>
<div style="font-size:300px;font-weight:700;letter-spacing:-.05em;color:var(--o);line-height:1;margin-top:40px">R$ 84</div>
<div style="font-size:46px;margin-top:20px;color:rgba(255,255,255,.8)">com 15% de comissão. Em 10 reservas, R$&nbsp;840.</div>
<div style="position:absolute;left:76px;right:76px;bottom:240px;font-size:58px;font-weight:600">Reserva direta: <span class="o">o dinheiro fica com você.</span></div>''')

S['s4'] = ('', f'''{brand()}
<h1 style="font-size:120px;margin-top:220px">Sua pousada funciona <span class="o">sem você?</span></h1>
<div style="display:flex;gap:30px;margin-top:110px">
  <div class="card" style="flex:1;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px"><span class="dot" style="width:110px;height:110px;background:var(--g)">{CHECK("#fff").replace('<svg ', '<svg style="width:64px;height:64px" ')}</span><span style="font-size:64px;font-weight:700">SIM</span></div>
  <div class="card" style="flex:1;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px"><span class="dot" style="width:110px;height:110px;background:var(--o)">{XMARK("#000").replace('<svg ', '<svg style="width:64px;height:64px" ')}</span><span style="font-size:64px;font-weight:700">NÃO</span></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:240px;text-align:center;font-size:44px;font-weight:600">Responda por mensagem: sim ou não?</div>''')

S['s5'] = ('dark', f'''{brand()}
<div style="margin-top:200px;font-size:44px;font-weight:600;letter-spacing:.12em;color:rgba(255,255,255,.65)">BASTIDORES</div>
<h1 style="font-size:116px;margin-top:30px">Feito aqui, pra <span class="o">pousada daqui.</span></h1>
<div style="font-size:50px;line-height:1.3;margin-top:60px;color:rgba(255,255,255,.85)">O Pousadas Fácil é desenvolvido pela Exagon Digital, uma software house de Lages, na Serra Catarinense.</div>
<div style="position:absolute;left:76px;bottom:240px;display:flex;align-items:center;gap:18px;font-size:54px;font-weight:600">{EXAGON.replace("46px", "70px").replace("40px", "61px")}<span>Exagon Digital</span></div>''')

S['s6'] = ('', f'''{brand()}
<h1 style="font-size:110px;margin-top:200px">Quanto você pagou de <span class="o">comissão</span> em outubro?</h1>
<div class="card" style="margin-top:90px;padding:50px 56px">
  <div class="sm" style="font-size:36px">Manda o valor por mensagem</div>
  <div style="margin-top:22px;height:130px;border-radius:30px;background:#F2EEE7;display:flex;align-items:center;padding:0 40px;font-size:64px;font-weight:700;color:#B5AEA4">R$ ...</div>
  <div style="margin-top:30px;font-size:42px;font-weight:500">e a gente te mostra quanto ficaria no seu caixa com reserva direta.</div>
</div>''')

S['s7'] = ('dark', f'''{brand()}
<div class="chip" style="margin-top:200px;height:76px;font-size:32px;background:var(--o);color:#000;padding:0 34px">Lista de espera aberta</div>
<h1 style="font-size:124px;margin-top:50px">Quer o Pousadas Fácil na sua <span class="o">pousada?</span></h1>
<div style="font-size:50px;line-height:1.3;margin-top:50px;color:rgba(255,255,255,.85)">Reserva direta, senha nova pra cada hóspede, WhatsApp e totem 24h.</div>
<div style="position:absolute;left:76px;right:76px;bottom:240px;height:150px;border-radius:75px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 22px 0 56px">
  <span style="font-size:58px;font-weight:700;color:#151515">Manda QUERO no direct</span>
  <span style="width:110px;height:110px;border-radius:50%;background:var(--o);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" width="56" height="56"><path fill="none" stroke="#000" stroke-width="2.4" stroke-linejoin="round" d="M4 12l16-8-6 16-2-6z"/></svg></span></div>''')

def html(w, h, body, cls=''):
    if h == 1920: body = '<div style="height:120px"></div>' + body
    css = CSS.replace('FONTS', FONTS.as_uri()).replace('Wpx', f'{w}px').replace('Hpx', f'{h}px')
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}"><div class="wrap">{body}</div></body></html>'

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, body in P.items():
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}); f = HERE / f'{name}.html'; f.write_text(html(1080, 1350, body))
        pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'{name}.jpg'), type='jpeg', quality=92); pg.close()
    for name, (cls, body) in S.items():
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}); f = HERE / f'{name}.html'; f.write_text(html(1080, 1920, body, cls))
        pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'{name}.jpg'), type='jpeg', quality=92); pg.close()
    b.close()
print('ok')
