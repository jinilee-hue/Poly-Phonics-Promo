import asyncio, base64, io, glob, sys
from playwright.async_api import async_playwright
from PIL import Image
CH=glob.glob('/Users/jini/Library/Caches/ms-playwright/chromium-1243/chrome-mac*/*.app/Contents/MacOS/*')[0]
SIZE=216; FRAMES=24
OUT='/Users/jini/Documents/Jini/2026/Phonics/Poly-Phonics-Promo/assets/img/concept-c/logo-die.webp'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CH, args=['--use-angle=metal','--enable-gpu-rasterization','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':SIZE,'height':SIZE})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto(f'http://127.0.0.1:5292/index.html?size={SIZE}&frames={FRAMES}',wait_until='networkidle')
        await pg.wait_for_function('window.ready===true', timeout=15000)
        frames=[]
        for i in range(FRAMES):
            d=await pg.evaluate(f'window.frame({i})')
            frames.append(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGBA'))
        print('errs',errs)
        await b.close()
    sheet=Image.new('RGBA',(SIZE*FRAMES,SIZE),(0,0,0,0))
    for i,f in enumerate(frames): sheet.paste(f,(i*SIZE,0))
    sheet.save(OUT,'WEBP',quality=92,method=6, lossless=False)
    frames[0].save('die_rest.png')
    prev=Image.new('RGBA',(SIZE*8,SIZE),(27,100,232,255))
    for k,i in enumerate(range(0,FRAMES,3)): prev.alpha_composite(frames[i],(k*SIZE,0))
    prev.convert('RGB').save('die_frames.png')
    import os; print(OUT, sheet.size, os.path.getsize(OUT)//1024,'KB')
asyncio.run(main())
