import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
OV = r'''(() => {
  ['cap','capbg','aChart'].forEach(id => document.getElementById(id).style.display = 'none');
  const d = document.createElement('div');
  d.innerHTML = `<div style="position:absolute;left:84px;right:84px;top:1150px;font-family:Outfit;color:#151515;display:flex;flex-direction:column;gap:28px">
    <span style="font-size:28px;font-weight:600;letter-spacing:.14em;color:#8A857D">PARA DONOS DE POUSADA E HOSTEL</span>
    <h1 style="margin:0;font-size:136px;line-height:.95;letter-spacing:-.045em;font-weight:700">Sua pousada<br><span style="color:#FF4F1F">não evolui?</span></h1>
    <span style="margin-top:26px;align-self:flex-start;display:inline-flex;align-items:center;gap:26px;height:112px;padding:0 18px 0 46px;border-radius:56px;background:#151515;color:#fff;font-size:42px;font-weight:600">Assista
      <span style="width:76px;height:76px;border-radius:50%;background:#FF4F1F;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" width="34" height="34" style="transform:translateX(2px)"><path d="M8 5.5v13l10.5-6.5Z" fill="#000"/></svg></span></span>
  </div>
  <div style="position:absolute;right:84px;top:1790px;display:flex;align-items:center;gap:14px">
    <svg viewBox="0 0 120 104" style="width:58px;height:50px"><defs><mask id="xc"><rect width="120" height="104" fill="#fff"/><rect x="74" y="18" width="50" height="68" fill="#000"/></mask></defs><path mask="url(#xc)" fill-rule="evenodd" d="M120 51.96L90 103.92L30 103.92L0 51.96L30 0L90 0Z M99.21 51.96L79.6 85.92L40.4 85.92L20.79 51.96L40.4 18L79.6 18Z" fill="#FF4F1F"/><rect x="30" y="42.96" width="66" height="18" fill="#FF4F1F"/></svg>
    <span style="font-size:46px;font-weight:600;letter-spacing:-.02em">Exagon</span></div>`;
  document.body.appendChild(d);
})();'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + str(HERE / 'index.html')); pg.wait_for_function('window.READY === true')
    pg.evaluate('window.renderAt(2.3)'); pg.evaluate(OV); pg.wait_for_timeout(300)
    pg.screenshot(path='capa.png'); b.close()
