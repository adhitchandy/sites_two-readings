import json,os
from PIL import Image, ExifTags
M="""01 _DSC1216 012_13.03.2026
02 DEZ09320 003_04.03.2026
03 _DSC1257 028_01.10.2026
04 AUG03037 007_08.03.2026
05 _DSC9931 004_05.03.2026
06 MAE04857 010_11.03.2026
07 _DSC1160 026_30.09.2026
08 AUG04053 017_18.03.2026
09 _DSC0463 002_03.03.2026
10 MAI00197 023_30.09.2026
11 _DSC2813 022_30.09.2026
12 FEB03494 016_17.03.2026
13 _DSC2075 024_30.09.2026
14 OKT05836 025_30.09.2026
15 _DSC1167 029_01.10.2026
16 AUG04676 030_01.10.2026
17 _DSC8836 011_12.03.2026
18 MAE03851 005_06.03.2026
19 _DSC1900 008_09.03.2026
20 DEZ09793 013_14.03.2026
21 _DSC2112 021_30.09.2026
22 JAN01381 006_07.03.2026
23 _DSC2752 020_27.03.2026
24 MAI08583 015_16.03.2026
25 _DSC0335 027_01.10.2026
26 MAE04945 019_21.03.2026
27 _DSC1897 018_19.03.2026
28 AUG02170 009_10.03.2026
29 _DSC2762 014_15.03.2026
30 FEB01586 031_01.10.2026"""
def ex(p):
    try:
        im=Image.open(p); e=im.getexif(); d={}
        for k,v in e.items(): d[ExifTags.TAGS.get(k,k)]=v
        for k,v in e.get_ifd(0x8769).items(): d[ExifTags.TAGS.get(k,k)]=v
        o={}
        for k in ['Make','Model','LensModel','FocalLength','FNumber','ExposureTime','ISOSpeedRatings','DateTimeOriginal','Software']:
            if k in d:
                v=d[k]
                try: v=float(v) if not isinstance(v,(str,int)) else v
                except Exception: v=str(v)
                o[k]=v.strip('\x00 ') if isinstance(v,str) else v
        return o
    except Exception as x: return {'err':str(x)}
def hist(p):
    im=Image.open(p).convert('RGB'); im.thumbnail((500,500))
    out=[]
    for ch in list(im.split())+[im.convert('L')]:
        h=ch.histogram(); b=[sum(h[i*4:(i+1)*4]) for i in range(64)]
        s=sorted(b)[-3] or 1
        out.append(''.join(chr(48+min(42,round(42*x/s))) for x in b))
    return out
R={}
for line in M.split('\n'):
    n,b,a=line.split()
    R[n]={'file':b,'exA':ex(f'photos/edited/adhit/{b}.jpg'),'exL':ex(f'photos/edited/allison/{a}.jpg'),
          'hA':hist(f'tools/pairs/{n}-adhit.jpg'),'hL':hist(f'tools/pairs/{n}-allison.jpg')}
json.dump(R,open('tools/meta.json','w'))
for n,v in R.items(): print(n,v['file'],v['exA'],'|',v['exL'])
