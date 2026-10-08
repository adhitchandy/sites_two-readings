import json,os,shutil,zipfile,re,sys
from PIL import Image, ImageOps
M=re.findall(r'(\d\d) ([A-Z_]+\d+) (\d{3}_[\d.]+\d)',open('tools/meta.py').read())
assert len(M)==30
NM={v:k for k,v in json.load(open('tools/newmap.json')).items()}
M=[(n,NM[n][:-4],x) for n,_,x in M]
OUT='site/img'; os.makedirs(OUT+'/s',exist_ok=True); os.makedirs(OUT+'/xl',exist_ok=True)
start=int(sys.argv[1]); end=int(sys.argv[2])
H=json.load(open('tools/hist.json')) if os.path.exists('tools/hist.json') else {}
def hist(im):
    im=im.copy(); im.thumbnail((500,500)); out=[]
    for ch in list(im.split())+[im.convert('L')]:
        h=ch.histogram(); b=[sum(h[i*4:(i+1)*4]) for i in range(64)]
        s=sorted(b)[-3] or 1
        out.append(''.join(chr(48+min(42,round(42*x/s))) for x in b))
    return out
for n,b,a in M[start:end]:
    for who,p in (('adhit',f'photos/edited/adhit/{b}.jpg'),('allison',f'photos/edited/allison/{a}.jpg')):
        im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
        xl=im.copy(); xl.thumbnail((3200,3200),Image.LANCZOS); xl.save(f'{OUT}/xl/{n}-{who}.jpg',quality=86,progressive=True,optimize=True)
        lg=xl.copy(); lg.thumbnail((1800,1800),Image.LANCZOS); lg.save(f'{OUT}/{n}-{who}.jpg',quality=82,progressive=True,optimize=True)
        sm=lg.copy(); sm.thumbnail((960,960),Image.LANCZOS); sm.save(f'{OUT}/s/{n}-{who}.webp',quality=76,method=5)
        H[f'{n}-{who}']=hist(lg)
    print(n,flush=True)
json.dump(H,open('tools/hist.json','w'))
