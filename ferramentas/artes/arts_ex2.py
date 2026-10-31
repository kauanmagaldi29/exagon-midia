"""Post + story Exagon: 'Seu sistema dá problema? A gente ajusta ele pra você.'"""
import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / 'arts_ex.py').read_text().splitlines()
exec('\n'.join(src[:36]))                      # CSS, mark(), brand(), cta(), ARROW ...
exec('\n'.join(src[81:85]))                    # html()

X = '<svg viewBox="0 0 24 24" style="width:30px;height:30px"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11" fill="none" stroke="#8C8C8C" stroke-width="2.8" stroke-linecap="round"/></svg>'
V = '<svg viewBox="0 0 24 24" style="width:32px;height:32px"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rows = [('Trava ou fica lento', 'Rápido de novo'), ('Erro que ninguém resolve', 'Erro corrigido'), ('Quem fez sumiu', 'A gente assume'), ('Não conversa com nada', 'Integrado')]
def table(fs=32):
    r = ''.join(f'''<div style="display:flex;border-top:2px solid #262626">
      <div style="flex:1;padding:24px 26px;display:flex;gap:16px;align-items:center;font-size:{fs}px;color:#9A9A9A"><span style="width:46px;height:46px;border-radius:50%;background:#242424;display:flex;align-items:center;justify-content:center;flex:none">{X}</span>{a}</div>
      <div style="flex:1;padding:24px 26px;display:flex;gap:16px;align-items:center;font-size:{fs}px;font-weight:600;background:#1D1D1D"><span style="width:46px;height:46px;border-radius:50%;background:#FF4F1F;display:flex;align-items:center;justify-content:center;flex:none">{V}</span>{b}</div></div>''' for a, b in rows)
    return f'''<div class="card" style="overflow:hidden;padding:0">
      <div style="display:flex;font-size:26px;font-weight:600;letter-spacing:.12em"><div style="flex:1;padding:22px 26px;color:#8C8C8C">SEU SISTEMA HOJE</div><div style="flex:1;padding:22px 26px;background:#1D1D1D;color:#FF4F1F">DEPOIS DO AJUSTE</div></div>{r}</div>'''

def window(h=200):
    return f'''<div class="card" style="overflow:hidden;padding:0">
      <div style="height:62px;background:#1F1F1F;display:flex;align-items:center;gap:12px;padding:0 26px"><i style="width:16px;height:16px;border-radius:50%;background:#3A3A3A"></i><i style="width:16px;height:16px;border-radius:50%;background:#3A3A3A"></i><i style="width:16px;height:16px;border-radius:50%;background:#3A3A3A"></i><span style="margin-left:16px;font-size:24px;color:#777">seusistema.com.br</span></div>
      <div style="padding:34px 34px;display:flex;align-items:center;gap:24px"><span style="width:84px;height:84px;border-radius:24px;background:rgba(255,79,31,.14);display:flex;align-items:center;justify-content:center;flex:none"><svg viewBox="0 0 24 24" style="width:50px;height:50px"><path d="M12 4 21.5 20h-19z M12 10v4.5 M12 17.5v.3" fill="none" stroke="#FF4F1F" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <div><div style="font-size:40px;font-weight:600">Erro ao salvar o pedido</div><div class="sm">Tente novamente mais tarde</div></div></div></div>'''

post = f'''{brand()}
<h1 style="font-size:112px;margin-top:64px">Seu sistema dá <span class="o">problema?</span></h1>
<div style="font-size:56px;font-weight:600;margin-top:26px;letter-spacing:-.02em">A gente ajusta ele pra você.</div>
<div style="margin-top:46px">{table(31)}</div>
<div style="margin-top:34px;font-size:38px;font-weight:500;color:#BDBDBD">Sem jogar tudo fora e <span class="o">sem começar do zero.</span></div>
{cta('Comenta AJUSTE')}'''

story = f'''{brand()}
<h1 style="font-size:138px;margin-top:150px">Seu sistema dá <span class="o">problema?</span></h1>
<div style="font-size:70px;font-weight:600;margin-top:34px;letter-spacing:-.02em">A gente ajusta ele pra você.</div>
<div style="margin-top:70px">{window()}</div>
<div style="margin-top:34px;font-size:44px;line-height:1.35;color:#CFCFCF">Corrigimos erros, deixamos rápido de novo, assumimos sistemas sem suporte e integramos com o que você já usa.</div>
<div style="position:absolute;left:76px;right:76px;bottom:240px;height:150px;border-radius:75px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 22px 0 56px">
  <span style="font-size:56px;font-weight:700;color:#111">Manda AJUSTE no direct</span>
  <span style="width:110px;height:110px;border-radius:50%;background:#FF4F1F;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" width="56" height="56"><path fill="none" stroke="#000" stroke-width="2.4" stroke-linejoin="round" d="M4 12l16-8-6 16-2-6z"/></svg></span></div>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (W, H, body) in {'ex4': (1080, 1350, post), 'es4': (1080, 1920, story)}.items():
        pg = b.new_page(viewport={'width': W, 'height': H}); f = HERE / f'{name}.html'; f.write_text(html(W, H, body, ''))
        pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f'{name}.jpg'), type='jpeg', quality=92); pg.close()
    b.close()
print('ok')
