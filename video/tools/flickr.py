# uso: flickr.py plano.json -> baixa fotos CC (uso comercial + adaptação) e grava assets/credits.json
import sys,json,os,re,urllib.request,urllib.parse
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) CanalNuvem/0.1"}
LIC={4:"CC BY 2.0",5:"CC BY-SA 2.0",7:"No known copyright restrictions",9:"CC0",10:"Public Domain Mark"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
def search(text):
    s=get("https://www.flickr.com/search/?"+urllib.parse.urlencode({"text":text,"license":"4,5,7,9,10"})).decode()
    dec=json.JSONDecoder(); out=[]; key='{"data":{"_flickrModelRegistry":"photo-lite-models"'
    for m in re.finditer(re.escape(key),s):
        try: o,_=dec.raw_decode(s,m.start())
        except Exception: continue
        d=o["data"]; out.append(d)
    return out
plan=json.load(open(sys.argv[1])); os.makedirs("assets/img",exist_ok=True)
cred=json.load(open("assets/credits.json")) if os.path.exists("assets/credits.json") else {}
for key,spec in plan.items():
    have=[k for k in cred if k.rsplit("_",1)[0]==key]
    n=spec.get("n",1); got=len(have); seen={cred[k]["page"] for k in cred}
    for term in (spec["q"] if isinstance(spec["q"],list) else [spec["q"]]):
        if got>=n: break
        for d in search(term):
            if got>=n: break
            if d.get("license") not in LIC: continue
            sizes=d["sizes"]["data"]; best=None
            for sz in ["k","h","l","b","c","z"]:
                if sz in sizes: best=sizes[sz]["data"]; break
            if not best or best["width"]<spec.get("minw",1000): continue
            if spec.get("land",True) and best["width"]<best["height"]: continue
            title=d.get("title","")
            if spec.get("must") and not re.search(spec["must"],title,re.I): continue
            pid=re.search(r"/(\d+)_",best["url"]).group(1)
            page=f'https://www.flickr.com/photos/{d.get("pathAlias") or d.get("ownerNsid")}/{pid}/'
            if page in seen: continue
            seen.add(page)
            name=f"{key}_{got}.jpg"; open("assets/img/"+name,"wb").write(get("https:"+best["url"]))
            cred[f"{key}_{got}"]=dict(file="img/"+name,title=title,page=page,license=LIC[d["license"]],author=d.get("realname") or d.get("username"),w=best["width"],h=best["height"])
            print(key,got,title,LIC[d["license"]],best["width"],best["height"],flush=True); got+=1
    if got<n: print("FALTOU",key,got,"/",n,flush=True)
    json.dump(cred,open("assets/credits.json","w"),ensure_ascii=False,indent=1)
