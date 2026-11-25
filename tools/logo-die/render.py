import asyncio, base64, io, glob, sys
from playwright.async_api import async_playwright
from PIL import Image
CH=glob.glob('/Users/jini/Library/Caches/ms-playwright/chromium-1243/chrome-mac*/*.app/Contents/MacOS/*')[0]
SIZE=480; FRAMES=24          # render big, then Lanczos down: smooth outline (user 2026-11-25 '테두리 깨지지 않게')
OUT2X=120; OUT1X=60          # frame size for 2x and 1x screens (logo shows at 60 CSS px)
OUT='/Users/jini/Documents/Jini/2026/Phonics/Poly-Phonics-Promo/assets/img/concept-c/logo-die.webp'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CH, args=['--use-angle=metal','--enable-gpu-rasterization','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':SIZE,'height':SIZE})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto(f'http://127.0.0.1:5292/index.html?size={SIZE}&frames={FRAMES}&ink=%23FFC400',wait_until='networkidle')
        await pg.wait_for_function('window.ready===true', timeout=15000)
        frames=[]
        for i in range(FRAMES):
            d=await pg.evaluate(f'window.frame({i})')
            frames.append(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGBA'))
        print('errs',errs)
        await b.close()
    def premul_resize(im, n):           # resize in premultiplied alpha so the edge doesn't pick up a dark/white fringe
        import numpy as np
        a=np.asarray(im).astype(np.float32)/255; a[...,:3]*=a[...,3:4]
        ch=[Image.fromarray((a[...,k]*255).astype('uint8')).resize((n,n),Image.LANCZOS) for k in range(4)]
        b=np.stack([np.asarray(c).astype(np.float32)/255 for c in ch],-1)
        al=np.clip(b[...,3:4],1e-6,1); b[...,:3]=np.where(b[...,3:4]>0,b[...,:3]/al,0)
        return Image.fromarray((np.clip(b,0,1)*255+.5).astype('uint8'),'RGBA')
    for n,out in [(OUT2X,OUT),(OUT1X,OUT.replace('.webp','@1x.webp'))]:
        sheet=Image.new('RGBA',(n*FRAMES,n),(0,0,0,0))
        for i,f in enumerate(frames): sheet.paste(premul_resize(f,n),(i*n,0))
        sheet.save(out,'WEBP',lossless=True,method=6)
    frames[0].save('die_rest.png')
    prev=Image.new('RGBA',(SIZE*8,SIZE),(27,100,232,255))
    for k,i in enumerate(range(0,FRAMES,3)): prev.alpha_composite(frames[i],(k*SIZE,0))
    prev.convert('RGB').save('die_frames.png')
    import os; print(OUT, sheet.size, os.path.getsize(OUT)//1024,'KB')
asyncio.run(main())
