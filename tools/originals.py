import json,os,re,io,sys,rawpy
from PIL import Image, ImageOps
M=re.findall(r'(\d\d) ([A-Z_]+\d+) (\d{3}_[\d.]+\d)',open('tools/meta.py').read()); assert len(M)==30
RAW='photos/raw/'; OUT='site/img'
H=json.load(open('tools/hist.json'))
def hist(im):
    im=im.copy(); im.thumbnail((500,500)); out=[]
    for ch in list(im.split())+[im.convert('L')]:
        h=ch.histogram(); b=[sum(h[i*4:(i+1)*4]) for i in range(64)]; s=sorted(b)[-3] or 1
        out.append(''.join(chr(48+min(42,round(42*x/s))) for x in b))
    return out
for n,b,a in M[int(sys.argv[1]):int(sys.argv[2])]:
    f=[x for x in os.listdir(RAW) if x.startswith(b+'.')][0]; r=rawpy.imread(RAW+f); im=None
    if f.endswith('.NEF'):
        t=r.extract_thumb()
        if t.format==rawpy.ThumbFormat.JPEG:
            im=Image.open(io.BytesIO(t.data)); o=im.getexif().get(0x0112,1); im=ImageOps.exif_transpose(im).convert('RGB')
            if o==1 and r.sizes.flip in (5,6): im=im.rotate(90 if r.sizes.flip==5 else -90,expand=True)
    if im is None: im=Image.fromarray(r.postprocess(use_camera_wb=True,no_auto_bright=False,output_bps=8))
    # same way up as the edits
    ref=Image.open(f'{OUT}/{n}-adhit.jpg').size
    if (im.width>im.height)!=(ref[0]>ref[1]): im=im.rotate(90,expand=True)
    xl=im.copy(); xl.thumbnail((3200,3200),Image.LANCZOS); xl.save(f'{OUT}/xl/{n}-original.jpg',quality=86,progressive=True,optimize=True)
    lg=xl.copy(); lg.thumbnail((1800,1800),Image.LANCZOS); lg.save(f'{OUT}/{n}-original.jpg',quality=82,progressive=True,optimize=True)
    sm=lg.copy(); sm.thumbnail((960,960),Image.LANCZOS); sm.save(f'{OUT}/s/{n}-original.webp',quality=76,method=5)
    H[f'{n}-original']=hist(lg); print(n,f,im.size,flush=True)
json.dump(H,open('tools/hist.json','w'))
