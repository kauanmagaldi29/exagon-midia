"""usage: rv.py meta | rv.py preview t1 t2 ... | rv.py scene NAME F0 F1"""
import sys, os, json, time, subprocess, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
FPS = 30
def open_page(p):
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    logs = []; pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('ERR ' + str(e)))
    pg.goto('file://' + str(HERE / 'index.html'))
    try: pg.wait_for_function('window.READY === true', timeout=60000)
    except Exception: print('\n'.join(logs)); raise
    for l in logs: print('console:', l)
    return b, pg
mode = sys.argv[1]
with sync_playwright() as p:
    b, pg = open_page(p)
    if mode == 'meta':
        m = pg.evaluate('({d: window.DURATION, sfx: window.SFX})'); (HERE / 'meta.json').write_text(json.dumps(m)); print(m['d'], len(m['sfx']))
    elif mode == 'preview':
        out = HERE / 'prev'; out.mkdir(exist_ok=True)
        for ts in sys.argv[2:]:
            pg.evaluate(f'window.renderAt({float(ts)})'); pg.screenshot(path=str(out / f't_{ts}.jpg'), type='jpeg', quality=90)
    elif mode == 'scene':
        name, f0, f1 = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        (HERE / 'scenes').mkdir(exist_ok=True)
        tmp = HERE / 'scenes' / f'{name}.part.mp4'; fin = HERE / 'scenes' / f'{name}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), str(tmp)], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(f0, f1):
            pg.evaluate(f'window.renderAt({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); rc = ff.wait()
        if rc == 0: tmp.rename(fin)
        print(name, f1 - f0, 'frames', round(time.time() - t0, 1), 's rc', rc)
    b.close()
