# alinha o texto do roteiro com o tempo de cada palavra (Whisper) -> words.json
import sys,json,re,subprocess,difflib,numpy as np,unicodedata
from faster_whisper import WhisperModel
narr=json.load(open(sys.argv[1])); outp=sys.argv[2]
def load(f):
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-f","s16le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
def norm(w): return re.sub(r"[^a-z0-9]","",unicodedata.normalize("NFKD",w.lower()).encode("ascii","ignore").decode())
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
out=[];offset=0.0
for ci,(title,paras) in enumerate(narr):
    f=f"voz/cap{ci}.mp3"; a=load(f); dur=len(a)/16000
    segs,_=m.transcribe(a,language="pt",word_timestamps=True)
    hw=[(w.word.strip(),w.start,w.end) for s in segs for w in s.words]
    toks=[(pi,t) for pi,p in enumerate(paras) for t in p.split()]
    A=[norm(t) for _,t in toks]; Bn=[norm(w) for w,_,_ in hw]
    sm=difflib.SequenceMatcher(None,A,Bn,autojunk=False)
    times=[None]*len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): times[blk.a+k]=(hw[blk.b+k][1],hw[blk.b+k][2])
    # interpola faltantes
    known=[i for i,t in enumerate(times) if t]
    for i in range(len(times)):
        if times[i] is None:
            prev=max([k for k in known if k<i],default=None); nxt=min([k for k in known if k>i],default=None)
            s=times[prev][1] if prev is not None else 0.0; e=times[nxt][0] if nxt is not None else dur
            lo=prev if prev is not None else -1; hi=nxt if nxt is not None else len(times)
            frac=(i-lo)/(hi-lo); st=s+(e-s)*frac*0.98
            times[i]=(st,st+max(0.05,(e-s)/(hi-lo)))
    miss=len(toks)-len(known)
    print(title,len(toks),"sem match:",miss,file=sys.stderr)
    for (pi,t),(s,e) in zip(toks,times):
        out.append(dict(w=t,s=round(s+offset,3),e=round(e+offset,3),cap=ci,p=pi))
    offset+=dur
json.dump(dict(words=out,caps=[dict(i=i,title=t) for i,(t,_) in enumerate(narr)]),open(outp,"w"),ensure_ascii=False)
