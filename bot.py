"""ДҲФ кафедраси — Telegram эслатма боти (мустақил файл, жадвал ичида).
   python bot.py digest | remind 9:00 | test"""
import os,sys,time,json,urllib.request,urllib.parse,datetime as dt
try:
    from zoneinfo import ZoneInfo
    TZ=ZoneInfo("Asia/Tashkent")
except Exception:
    TZ=dt.timezone(dt.timedelta(hours=5))
START=dt.date(2026,9,8); END=dt.date(2026,12,25)
HOL={dt.date(2026,10,1),dt.date(2026,12,8)}
KUN=["душанба","сешанба","чоршанба","пайшанба","жума","шанба","якшанба"]
SUBFULL={"КОНС":"Конституциявий ҳуқуқ","ДҲН":"Давлат ва ҳуқуқ назарияси"}
DHN7_UZ=["Davlat va huquq nazariyasining predmeti va metodlari. Davlat va huquqning kelib chiqishi.","Davlat tushunchasi, belgilari, mohiyati va tiplari. Davlat funksiyalari.","Davlat shakllari: davlatning boshqaruv shakli, tuzilish shakli va siyosiy rejim. Davlat mexanizmi va davlat apparati.","Ijtimoiy munosabatlar va huquq. Huquqiy ong va huquqiy madaniyat. Huquq normalari. Huquq shakllari (manbalari).","Huquq ijodkorligi. Huquq tizimi va huquqiy tizim. Huquqiy munosabatlar. Huquqni amalga oshirish.","Huquq normalarini sharhlash. Huquqiy xulq-atvor. Huquqbuzarlik va yuridik javobgarlik.","Huquqiy tartibga solish mexanizmi. Qonuniylik va huquqiy tartibot. Davlat va huquqning rivojlanish istiqbollari va yo‘llari."]
DHN7_RU=["Предмет и методы теории государства и права. Происхождение государства и права.","Понятие, признаки, сущность и типы государства. Функции государства.","Формы государства: форма правления, форма государственного устройства и политический режим. Механизм государства и государственный аппарат.","Общественные отношения и право. Правосознание и правовая культура. Нормы права. Формы (источники) права.","Правотворчество. Система права и правовая система. Правовые отношения. Реализация права.","Толкование норм права. Правовое поведение. Правонарушение и юридическая ответственность.","Механизм правового регулирования. Законность и правопорядок. Перспективы и пути развития государства и права."]
DHN15_UZ=["Davlat va huquq nazariyasining predmeti va metodlari","Davlat va huquqning kelib chiqishi","Davlat tushunchasi, belgilari, mohiyati va tiplari. Davlat funksiyalari","Davlat shakllari: davlatning boshqaruv shakli, tuzilish shakli va siyosiy rejim","Davlat mexanizmi va davlat apparati","Ijtimoiy munosabatlar va huquq. Huquqiy ong va huquqiy madaniyat","Huquq normalari","Huquq shakllari (manbalari)","Huquq ijodkorligi","Huquq tizimi va huquqiy tizim","Huquqiy munosabatlar. Huquqni amalga oshirish","Huquq normalarini sharhlash","Huquqiy xulq-atvor. Huquqbuzarlik va yuridik javobgarlik","Huquqiy tartibga solish mexanizmi. Qonuniylik va huquqiy tartibot","Davlat va huquqning rivojlanish istiqbollari va yo‘llari"]
DHN15_RU=["Предмет и методы теории государства и права","Происхождение государства и права","Понятие, признаки, сущность и типы государства. Функции государства","Формы государства: форма правления, форма государственного устройства и политический режим","Механизм государства и государственный аппарат","Общественные отношения и право. Правосознание и правовая культура","Нормы права","Формы (источники) права","Правотворчество","Система права и правовая система","Правовые отношения. Реализация права","Толкование норм права","Правовое поведение. Правонарушение и юридическая ответственность","Механизм правового регулирования. Законность и правопорядок","Перспективы и пути развития государства и права"]
KONS15_UZ=["Konstitutsiyaviy huquq faniga kirish. Konstitutsiyaning asosiy prinsiplari","O‘zbekiston Respublikasida fuqarolik masalalari. Shaxsiy huquq va erkinliklar","Inson va fuqarolarning siyosiy, iqtisodiy, ijtimoiy, madaniy va ekologik huquqlari. Fuqarolarning burchlari","Jamiyatning iqtisodiy negizlari. Fuqarolik jamiyati institutlari","Oila, bolalar va yoshlar masalalari. Ommaviy axborot vositalarining konstitutsiyaviy asoslari","O‘zbekiston Respublikasining ma’muriy-hududiy va davlat tuzilishi","O‘zbekiston Respublikasining Oliy Majlisi","O‘zbekiston Respublikasida Prezidentlik instituti","O‘zbekiston Respublikasi Vazirlar Mahkamasi","Mahalliy davlat hokimiyati va fuqarolarning o‘zini o‘zi boshqarish organlari","O‘zbekiston Respublikasida saylov tizimi","Sud hokimiyatining konstitutsiyaviy-huquqiy asoslari","O‘zbekiston Respublikasida advokaturaning konstitutsiyaviy-huquqiy asoslari","Prokuraturaning konstitutsiyaviy-huquqiy asoslari","Moliya, pul va bank tizimi hamda mudofaa va xavfsizlik masalalari. Konstitutsiyaga o‘zgartirish kiritish tartibi"]
KONS15_RU=["Введение в конституционное право. Основные принципы Конституции","Вопросы гражданства в Республике Узбекистан. Личные права и свободы","Политические, экономические, социальные, культурные и экологические права человека и гражданина. Обязанности граждан","Экономические основы общества. Институты гражданского общества","Вопросы семьи, детей и молодёжи. Конституционные основы средств массовой информации","Административно-территориальное и государственное устройство Республики Узбекистан","Олий Мажлис Республики Узбекистан","Институт президентства в Республике Узбекистан","Кабинет Министров Республики Узбекистан","Местные органы государственной власти и органы самоуправления граждан","Избирательная система в Республике Узбекистан","Конституционно-правовые основы судебной власти","Конституционно-правовые основы адвокатуры в Республике Узбекистан","Конституционно-правовые основы прокуратуры","Вопросы финансов, денежной и банковской системы, обороны и безопасности. Порядок внесения изменений в Конституцию"]
CFG=[{"pot": "1К","sub": "ДҲН","pn": "Киберҳуқуқ","lect": "У.Шоназаров","lroom": "А-306","sems": [["У.Шоназаров","306","БК-26"]],"slots": [[0,"9:00"],[2,"10:30"]],"ru": False},{"pot": "1К","sub": "КОНС","pn": "Киберҳуқуқ","lect": "Н.Азизов","lroom": "А-306","sems": [["Н.Азизов","306","БК-26"]],"slots": [[1,"10:30"],[3,"10:30"]],"ru": False},{"pot": "1КРУС","sub": "ДҲН","pn": "Киберҳуқуқ (рус гуруҳи)","lect": "А.Джасимова","lroom": "А-305","sems": [["А.Джасимова","305","БКР-26"]],"slots": [[2,"9:00"],[3,"9:00"]],"ru": True},{"pot": "1КРУС","sub": "КОНС","pn": "Киберҳуқуқ (рус гуруҳи)","lect": "А.Джасимова","lroom": "А-305","sems": [["А.Джасимова","305","БКР-26"]],"slots": [[1,"12:00"],[3,"10:30"]],"ru": True},{"pot": "1П","sub": "ДҲН","pn": "Прокурорлик фаолияти","lect": "У.Шоназаров","lroom": "Б-103","sems": [["У.Шоназаров","103","БП1-26"],["Ш.Зуфарова","307","БП2-26"]],"slots": [[1,"9:00"],[3,"9:00"]],"ru": False},{"pot": "1П","sub": "КОНС","pn": "Прокурорлик фаолияти","lect": "Н.Азизов","lroom": "Б-103","sems": [["Д.Ибрагимов","103","БП1-26"],["Ш.Зуфарова","307","БП2-26"]],"slots": [[2,"10:30"],[4,"10:30"]],"ru": False},{"pot": "1ПРУС","sub": "ДҲН","pn": "Прокурорлик фаолияти (рус гуруҳи)","lect": "Т.Кенжаев","lroom": "А-404","sems": [["Т.Кенжаев","404","БПР-26"]],"slots": [[2,"9:00"],[4,"9:00"]],"ru": True},{"pot": "1ПРУС","sub": "КОНС","pn": "Прокурорлик фаолияти (рус гуруҳи)","lect": "Т.Кенжаев","lroom": "А-404","sems": [["Т.Кенжаев","404","БПР-26"]],"slots": [[0,"10:30"],[2,"10:30"]],"ru": True},{"pot": "1ТА","sub": "ДҲН","pn": "Тергов фаолияти «А» поток","lect": "У.Шоназаров","lroom": "А-101","sems": [["Н.Азизов","207","БТА1-26"],["Ш.Зуфарова","208","БТА2-26"],["А.Джасимова","210","БТА3-26"]],"slots": [[0,"10:30"]],"ru": False},{"pot": "1ТА","sub": "КОНС","pn": "Тергов фаолияти «А» поток","lect": "Д.Ибрагимов","lroom": "А-101","sems": [["А.Джасимова","207","БТА1-26"],["Э.Хожиев","208","БТА2-26"],["Ш.Зуфарова","210","БТА3-26"]],"slots": [[0,"9:00"],[2,"12:00"]],"ru": False},{"pot": "1ТБ","sub": "ДҲН","pn": "Тергов фаолияти «Б» поток","lect": "У.Шоназаров","lroom": "А-201","sems": [["У.Шоназаров","201","БТБ1-26"],["Ш.Зуфарова","202","БТБ2-26"],["А.Джасимова","205","БТБ3-26"]],"slots": [[0,"12:00"]],"ru": False},{"pot": "1ТБ","sub": "КОНС","pn": "Тергов фаолияти «Б» поток","lect": "Д.Ибрагимов","lroom": "А-201","sems": [["О.Нематиллаев","201","БТБ1-26"],["Э.Хожиев","202","БТБ2-26"],["Ш.Зуфарова","205","БТБ3-26"]],"slots": [[1,"10:30"],[3,"10:30"]],"ru": False},{"pot": "1ТД","sub": "ДҲН","pn": "Тергов фаолияти «Д» поток","lect": "У.Шоназаров","lroom": "Б-201","sems": [["У.Шоназаров","201","БТД1-26"],["Ш.Зуфарова","206","БТД2-26"]],"slots": [[3,"12:00"]],"ru": False},{"pot": "1ТД","sub": "КОНС","pn": "Тергов фаолияти «Д» поток","lect": "Д.Ибрагимов","lroom": "Б-201","sems": [["Д.Ибрагимов","201","БТД1-26"],["Ш.Зуфарова","206","БТД2-26"]],"slots": [[2,"9:00"],[4,"9:00"]],"ru": False},{"pot": "1ТРУС","sub": "ДҲН","pn": "Тергов фаолияти (рус гуруҳи)","lect": "Т.Кенжаев","lroom": "А-309","sems": [["Т.Кенжаев","309","БТР-26"]],"slots": [[1,"9:00"]],"ru": True},{"pot": "1ТРУС","sub": "КОНС","pn": "Тергов фаолияти (рус гуруҳи)","lect": "Т.Кенжаев","lroom": "А-309","sems": [["Т.Кенжаев","309","БТР-26"]],"slots": [[0,"9:00"],[3,"9:00"]],"ru": True}]
def dates(wds,n):
    out=[];d=START
    while len(out)<n and d<END+dt.timedelta(days=400):
        if d.weekday() in wds and d not in HOL: out.append(d)
        d+=dt.timedelta(days=1)
    return out

def plan(c):
    ru=c["ru"]; single=len(c["slots"])==1
    if c["sub"]=="ДҲН":
        if c["pot"].startswith("1Т"):
            T=DHN7_RU if ru else DHN7_UZ; lec=[1]*7; sem=[1]*6+[2]
        elif c["pot"].startswith("1П"):
            T=(DHN15_RU if ru else DHN15_UZ)[:7]; lec=[2,2,2,2,2,3,2]; sem=list(lec)
        else:
            T=DHN15_RU if ru else DHN15_UZ; lec=[1]*15; sem=[1]*15
    else:
        if c["pot"].startswith("1П"):
            T=(KONS15_RU if ru else KONS15_UZ)[:10]; lec=[2,2,2,2,1,1,2,1,1,1]; sem=list(lec)
        else:
            T=KONS15_RU if ru else KONS15_UZ; lec=[1]*15; sem=[1]*15
    nl=sum(lec); ns=sum(sem); order=[]
    if single:
        seq=[]
        for i in range(len(T)): seq+=[(i,"L")]*lec[i]+[(i,"S")]*sem[i]
        ds=dates({c["slots"][0][0]},len(seq))
        order=[(i,k,ds[j]) for j,(i,k) in enumerate(seq)]
    else:
        ds=dates({c["slots"][0][0],c["slots"][1][0]},nl+ns); j=0
        for i in range(len(T)):
            for _ in range(lec[i]): order.append((i,"L",ds[j])); j+=1
            for _ in range(sem[i]): order.append((i,"S",ds[j])); j+=1
    return T,order,ns*2

def build():
    out=[]
    for c in CFG:
        T,order,sh=plan(c)
        lim=4 if sh==16 else 8; k=0; on1=None
        for i,kind,d in order:
            if kind=="S":
                k+=1
                if k==lim: on1=d
        ond={on1:"1-оралиқ назорат", order[-1][2]:"2-оралиқ назорат"}
        st={w:t for w,t in c["slots"]}
        for i,kind,d in order:
            t=st.get(d.weekday()) or c["slots"][0][1]
            r=dict(d=d,t=t,code=c["sub"]+c["pot"],pot=c["pn"],tno=i+1,top=T[i],
                   ty=("Маъруза" if kind=="L" else "Семинар"))
            if kind=="L": r["who"]=[("Бутун поток",c["lect"],c["lroom"])]
            else:
                r["who"]=[(g,a,b) for a,b,g in c["sems"]]
                if d in ond: r["on"]=ond[d]
            out.append(r)
    out.sort(key=lambda r:(r["d"],r["t"],r["code"]))
    return out

LESSONS=build()
SLOTS=sorted({l["t"] for l in LESSONS},key=lambda x:(int(x.split(":")[0]),int(x.split(":")[1])))
TOKEN=os.environ.get("TELEGRAM_TOKEN","").strip()
CHAT=os.environ.get("TELEGRAM_CHAT_ID","").strip()

STATE=".state/sent.txt"
LOGF=".state/log.txt"
OBUNA=".state/obuna.txt"
ADMINF=".state/admin.txt"
TUZ=".state/tuzatish.json"
POTOKLAR=sorted({c["pot"] for c in CFG})
FANLAR=sorted({c["sub"] for c in CFG})

def logga(s):
    t=dt.datetime.now(TZ).strftime("%d.%m %H:%M:%S")
    line="%s | %s"%(t,s)
    print(line)
    try:
        os.makedirs(".state",exist_ok=True)
        old=[]
        try: old=[x for x in open(LOGF,encoding="utf-8").read().split("\n") if x.strip()]
        except Exception: pass
        old.append(line)
        open(LOGF,"w",encoding="utf-8").write("\n".join(old[-250:])+"\n")
    except Exception as e: print("лог хатоси:",e)

def royxat_oq(f):
    try: return [x.strip() for x in open(f,encoding="utf-8").read().split("\n") if x.strip()]
    except Exception: return []
def royxat_yoz(f,l):
    os.makedirs(".state",exist_ok=True)
    open(f,"w",encoding="utf-8").write("\n".join(l)+("\n" if l else ""))

def already(key):
    try: return key in open(STATE,encoding="utf-8").read().split("\n")
    except Exception: return False
def mark(key):
    old=royxat_oq(STATE); old.append(key); royxat_yoz(STATE,old[-300:])

# ---------- обуна ----------
def obunalar(): return royxat_oq(OBUNA)
def obuna_qosh(cid):
    cid=str(cid); l=obunalar()
    if cid in l: return False
    l.append(cid); royxat_yoz(OBUNA,l); logga("янги обуна: %s (жами %d)"%(cid,len(l))); return True
def obuna_ol(cid):
    cid=str(cid); l=obunalar()
    if cid not in l: return False
    royxat_yoz(OBUNA,[x for x in l if x!=cid]); logga("обуна бекор: %s"%cid); return True
def obunami(cid): return str(cid) in obunalar()

# ---------- админ ----------
def adminlar(): return royxat_oq(ADMINF)
def adminmi(cid): return str(cid) in adminlar()
def admin_qosh(cid):
    l=adminlar()
    if str(cid) in l: return False
    l.append(str(cid)); royxat_yoz(ADMINF,l); logga("янги админ: %s"%cid); return True

# ---------- тузатишлар ----------
def tuzatishlar():
    try: return json.load(open(TUZ,encoding="utf-8"))
    except Exception: return []
def tuz_yoz(l):
    os.makedirs(".state",exist_ok=True)
    json.dump(l,open(TUZ,"w",encoding="utf-8"),ensure_ascii=False,indent=1)

BASE=LESSONS
_C={"k":None,"v":None}

def pot_mos(code,pot):
    if pot=="*": return True
    c=code.upper(); p=pot.upper()
    if c==p: return True
    if p in [f.upper() for f in FANLAR]: return c.startswith(p)
    return c.endswith(p)

def qolla(base):
    out=[]
    for l in base:
        n=dict(l); n["who"]=[list(w) for w in l["who"]]; out.append(n)
    for t in tuzatishlar():
        tur=t.get("tur"); sana=t.get("sana","*"); pot=t.get("pot","*"); vaqt=t.get("vaqt","*")
        def mos(l):
            if sana!="*" and str(l["d"])!=sana: return False
            if not pot_mos(l["code"],pot): return False
            if vaqt!="*" and l["t"]!=vaqt: return False
            return True
        if tur=="bekor":
            out=[l for l in out if not mos(l)]
        elif tur=="domla":
            e=t.get("eski",""); y=t.get("yangi","")
            for l in out:
                if mos(l):
                    for w in l["who"]:
                        if e=="*" or e.lower() in w[1].lower(): w[1]=y
        elif tur=="xona":
            for l in out:
                if mos(l):
                    for w in l["who"]: w[2]=t.get("yangi","")
        elif tur=="vaqt":
            for l in out:
                if mos(l): l["t"]=t.get("yangi",l["t"])
        elif tur=="mavzu":
            for l in out:
                if mos(l): l["top"]=t.get("yangi",l["top"])
    return out

def LES():
    try: k=open(TUZ,encoding="utf-8").read()
    except Exception: k=""
    if _C["k"]!=k: _C["k"]=k; _C["v"]=qolla(BASE)
    return _C["v"]

def SLOTLAR():
    return sorted({l["t"] for l in LES()},key=lambda x:(int(x.split(":")[0]),int(x.split(":")[1])))

# ---------- юбориш ----------
def barcha_manzil():
    ids=[c.strip() for c in CHAT.replace(";",",").split(",") if c.strip()]
    for c in obunalar():
        if c not in ids: ids.append(c)
    return ids

def bitta(cid,text,plain=False):
    import urllib.error,re as _re
    p={"chat_id":cid,"text":(_re.sub(r"<[^>]+>","",text) if plain else text),
       "disable_web_page_preview":"true"}
    if not plain: p["parse_mode"]="HTML"
    body=urllib.parse.urlencode(p).encode()
    for i in range(3):
        try:
            req=urllib.request.Request("https://api.telegram.org/bot%s/sendMessage"%TOKEN,data=body)
            with urllib.request.urlopen(req,timeout=30) as r: return True
        except urllib.error.HTTPError as e:
            d=""
            try: d=e.read().decode("utf-8","replace")[:200]
            except Exception: pass
            logga("ХАТО %s (%d): %s %s"%(cid,i+1,e.code,d))
            if e.code==400 and not plain: return bitta(cid,text,plain=True)
            if e.code==429: time.sleep(20); continue
            if e.code in (401,403,404):
                if e.code==403: obuna_ol(cid)
                return False
            time.sleep(3)
        except Exception as e:
            logga("ХАТО %s (%d): %s"%(cid,i+1,e)); time.sleep(3)
    if not plain: return bitta(cid,text,plain=True)
    return False

def send(text):
    if not TOKEN or not CHAT:
        print("!! TELEGRAM_TOKEN ёки TELEGRAM_CHAT_ID берилмаган"); sys.exit(1)
    ids=barcha_manzil(); ok=0
    for cid in ids:
        if bitta(cid,text): ok+=1
        time.sleep(0.06)
    logga("хабар: %d/%d манзилга етди"%(ok,len(ids)))
    return ok>0

def block(l):
    s=["<b>%s</b> · %s · <i>%s</i>"%(l["code"],l["ty"],l["pot"]),
       "   📖 <b>%d-мавзу.</b> %s"%(l["tno"],l["top"])]
    if l.get("on"): s.append("   ❗️ <b>%s</b>"%l["on"])
    s+=["   👤 %s — %s, <b>%s</b>-хона"%(g,a,b) for g,a,b in l["who"]]
    return "\n".join(s)

def digest():
    day=dt.datetime.now(TZ).date()+dt.timedelta(days=1)
    key="digest-%s"%day
    if already(key): return
    ls=[l for l in LES() if l["d"]==day]
    if not ls: logga("эртага дарс йўқ"); mark(key); return
    p=["📅 <b>Эртага — %s, %s</b>\nДавлат-ҳуқуқий фанлар кафедраси машғулотлари\n"
       %(day.strftime("%d.%m.%Y"),KUN[day.weekday()])]
    for t in SLOTLAR():
        cur=[l for l in ls if l["t"]==t]
        if not cur: continue
        p.append("🕘 <b>%s</b>"%t); p+=[block(l) for l in cur]; p.append("")
    p.append("<i>Ҳаммага сермаҳсул иш куни тилаймиз!</i>")
    if send("\n".join(p).strip()): mark(key)
    else: logga("дайджест юборилмади, қайта уриниб кўрилади")

def remind(slot):
    now=dt.datetime.now(TZ); today=now.date()
    key="remind-%s-%s"%(today,slot)
    if already(key): return
    ls=[l for l in LES() if l["d"]==today and l["t"]==slot]
    if not ls: logga("бугун %s да дарс йўқ"%slot); mark(key); return
    hh,mm=(int(x) for x in slot.split(":"))
    start=now.replace(hour=hh,minute=mm,second=0,microsecond=0)
    qoldi=int(round((start-now).total_seconds()/60.0))
    if qoldi<1: logga("%s: дарс бошланиб бўлган"%slot); mark(key); return
    logga("эслатма: %s (%d дақиқа қолди, %d дарс)"%(slot,qoldi,len(ls)))
    ok=True
    for l in ls:
        if not send("⏰ <b>%d дақиқадан сўнг — %s</b>\n\n%s"%(qoldi,slot,block(l))): ok=False
        time.sleep(1)
    if ok: mark(key)
    else: logga("эслатма ЮБОРИЛМАДИ: %s — қайта уринилади"%slot)

def test():
    n=dt.datetime.now(TZ)
    send("✅ <b>Синов хабари</b>\nВақт: %s\nМашғулотлар: %d\nОбуначилар: %d\nТузатишлар: %d"
         %(n.strftime("%d.%m.%Y %H:%M"),len(LES()),len(obunalar()),len(tuzatishlar())))

def diag():
    import urllib.error
    def call(name,q=""):
        u="https://api.telegram.org/bot%s/%s%s"%(TOKEN,name,q)
        try: print(name,"->",urllib.request.urlopen(u,timeout=20).read().decode("utf-8","replace")[:600])
        except urllib.error.HTTPError as e: print(name,"-> ХАТО",e.code,e.read().decode("utf-8","replace")[:600])
        except Exception as e: print(name,"-> ХАТО",type(e).__name__,e)
    print("CHAT:",repr(CHAT),"| обуна:",obunalar(),"| админ:",adminlar())
    call("getMe")
    for cid in barcha_manzil(): call("getChat","?chat_id="+urllib.parse.quote(cid))
    send("🔎 Диагностика хабари")

# ---------- интерфейс ----------
YOQ="🔔 Эслатмани ёқиш"
OCH="🔕 Эслатмани ўчириш"

def kb(cid):
    uch=[{"text":OCH}] if obunami(cid) else [{"text":YOQ}]
    return {"keyboard":[[{"text":"📅 Бугун"},{"text":"📅 Эртага"}],
                        [{"text":"🗓 Шу ҳафта"}],uch],"resize_keyboard":True}

def hello(cid):
    h=("👋 <b>ДҲФ кафедраси — дарс жадвали боти</b>\n"
       "Пастдаги тугмалардан фойдаланинг ёки /bugun, /ertaga, /hafta ёзинг.\n")
    if obunami(cid):
        h+="🔔 Автоматик эслатма: <b>ЁҚИЛГАН</b> (дарсдан 10 дақиқа олдин ва 18:00 да).\n"
    else:
        h+="🔕 Автоматик эслатма ўчиқ. Ёқиш учун «%s» тугмасини босинг.\n"%YOQ
    if adminmi(cid): h+="🛠 Сиз админсиз — буйруқлар рўйхати: /yordam\n"
    return h

YORDAM=("🛠 <b>Админ буйруқлари</b>\n\n"
 "<b>Домлани алмаштириш</b>\n"
 "<code>/domla сана поток эски > янги</code>\n"
 "масалан: <code>/domla 10.09 1П Шоназаров > Азизов</code>\n"
 "доимий қилиш учун сана ўрнига <code>*</code>: <code>/domla * 1П Шоназаров > Азизов</code>\n\n"
 "<b>Дарс вақтини кўчириш</b>\n"
 "<code>/vaqt сана поток эскивақт > янгивақт</code>\n"
 "масалан: <code>/vaqt 10.09 1П 9:00 > 12:00</code>\n\n"
 "<b>Хонани ўзгартириш</b>\n"
 "<code>/xona сана поток вақт хона</code>\n"
 "масалан: <code>/xona 10.09 1П 9:00 А-205</code>\n\n"
 "<b>Мавзуни ўзгартириш</b>\n"
 "<code>/mavzu сана поток вақт янги мавзу матни</code>\n\n"
 "<b>Дарсни бекор қилиш</b>\n"
 "<code>/bekor сана</code> ёки <code>/bekor сана поток</code>\n"
 "масалан: <code>/bekor 10.09</code> — ўша куннинг ҳамма дарси\n\n"
 "<b>Тузатишлар рўйхати:</b> <code>/royxat</code>\n"
 "<b>Тузатишни ўчириш:</b> <code>/ochir 2</code>\n\n"
 "Сана: <code>10.09</code>, <code>10.09.2026</code>, <code>bugun</code>, <code>ertaga</code> ёки <code>*</code>\n"
 "Потоклар: 1К, 1КРУС, 1П, 1ПРУС, 1ТА, 1ТБ, 1ТД, 1ТРУС ёки <code>*</code>\n"
 "Фақат бир фан учун: <code>ДҲН1П</code> ёки <code>КОНС1П</code>; бутун фан: <code>ДҲН</code>")

def sana_ol(s):
    s=s.strip().lower()
    if s in ("*","hamma","ҳамма","doim","доим"): return "*"
    n=dt.datetime.now(TZ).date()
    if s in ("bugun","бугун"): return str(n)
    if s in ("ertaga","эртага"): return str(n+dt.timedelta(days=1))
    p=s.replace("/",".").replace("-",".").split(".")
    try:
        d=int(p[0]); m=int(p[1]); y=int(p[2]) if len(p)>2 else n.year
        if y<100: y+=2000
        return str(dt.date(y,m,d))
    except Exception: return None

def pot_ol(s):
    s=s.strip().upper()
    if s in ("*","HAMMA","ҲАММА"): return "*"
    for f in FANLAR:
        if f.upper()==s: return f
    for p in POTOKLAR:
        if p.upper()==s: return p
    for l in BASE:
        if l["code"].upper()==s: return l["code"]
    return None

def vaqt_ol(s):
    import re as _re
    s=s.strip()
    if s=="*": return "*"
    m=_re.match(r"^(\d{1,2})[:.](\d{2})$",s)
    return "%d:%02d"%(int(m.group(1)),int(m.group(2))) if m else None

def _snap():
    return set((str(l["d"]),l["t"],l["pot"],l["code"],l["top"],
                tuple(tuple(w) for w in l["who"])) for l in LES())

def tuz_qosh(rec):
    old=_snap()
    l=tuzatishlar(); l.append(rec); tuz_yoz(l)
    new=_snap()
    ozgardi=len(old-new)
    if ozgardi==0:
        l=tuzatishlar(); l.pop(); tuz_yoz(l)
        return None
    logga("тузатиш: %s (%d дарс)"%(rec,ozgardi))
    return ozgardi

def royxat_matn():
    l=tuzatishlar()
    if not l: return "📋 Ҳозирча ҳеч қандай тузатиш йўқ."
    p=["📋 <b>Тузатишлар</b>"]
    for i,t in enumerate(l,1):
        s="%d) <b>%s</b> · сана: %s · поток: %s"%(i,t.get("tur"),t.get("sana"),t.get("pot"))
        if t.get("vaqt","*")!="*": s+=" · вақт: %s"%t["vaqt"]
        if t.get("eski"): s+=" · %s → %s"%(t["eski"],t.get("yangi",""))
        elif t.get("yangi"): s+=" → %s"%t["yangi"]
        p.append(s)
    p.append("\nЎчириш: <code>/ochir рақам</code>")
    return "\n".join(p)

def admin_buyruq(cid,txt):
    """админ буйруғи бўлса — жавоб матнини қайтаради, акс ҳолда None"""
    t=txt.strip()
    if not t.startswith("/"): return None
    bosh=t.split()[0].lower().lstrip("/")
    if bosh not in ("domla","vaqt","xona","mavzu","bekor","royxat","ochir","yordam","admin"):
        return None
    if bosh=="admin":
        if not adminlar():
            admin_qosh(cid); saqla()
            return "🛠 Сиз админ сифатида қайд этилдингиз.\n\n"+YORDAM
        return YORDAM if adminmi(cid) else "⛔️ Админ аллақачон белгиланган."
    if not adminmi(cid):
        return "⛔️ Бу буйруқ фақат админ учун."
    if bosh=="yordam": return YORDAM
    if bosh=="royxat": return royxat_matn()
    qolgan=t[len(t.split()[0]):].strip()
    if bosh=="ochir":
        l=tuzatishlar()
        try: n=int(qolgan)
        except Exception: return "❌ Рақам киритинг: <code>/ochir 1</code>"
        if not 1<=n<=len(l): return "❌ Бундай рақам йўқ. /royxat"
        x=l.pop(n-1); tuz_yoz(l); saqla(); logga("тузатиш ўчирилди: %s"%x)
        return "🗑 %d-тузатиш ўчирилди."%n
    if bosh=="bekor":
        a=qolgan.split()
        if not a: return "❌ Намуна: <code>/bekor 10.09</code> ёки <code>/bekor 10.09 1П</code>"
        s=sana_ol(a[0])
        if not s: return "❌ Сана нотўғри: %s"%a[0]
        p=pot_ol(a[1]) if len(a)>1 else "*"
        if p is None: return "❌ Поток нотўғри: %s"%a[1]
        n=tuz_qosh({"tur":"bekor","sana":s,"pot":p})
        if not n: return "⚠️ Мос дарс топилмади (сана/поток текширинг)."
        saqla(); return "🚫 <b>%d та дарс бекор қилинди</b> (%s, %s)."%(n,s,p)
    if bosh in ("domla","vaqt"):
        if ">" not in qolgan:
            return ("❌ «>» белгиси керак.\nНамуна: <code>/domla 10.09 1П Шоназаров > Азизов</code>"
                    if bosh=="domla" else
                    "❌ «>» белгиси керак.\nНамуна: <code>/vaqt 10.09 1П 9:00 > 12:00</code>")
        chap,ong=qolgan.split(">",1); ong=ong.strip(); a=chap.split()
        if len(a)<3 or not ong: return "❌ Тўлиқ эмас. /yordam"
        s=sana_ol(a[0]); p=pot_ol(a[1])
        if not s: return "❌ Сана нотўғри: %s"%a[0]
        if p is None: return "❌ Поток нотўғри: %s"%a[1]
        eski=" ".join(a[2:])
        if bosh=="domla":
            n=tuz_qosh({"tur":"domla","sana":s,"pot":p,"eski":eski,"yangi":ong})
            if not n: return "⚠️ «%s» домла бу дарсларда топилмади."%eski
            saqla(); return "👤 <b>%d та дарсда</b> %s → <b>%s</b> (%s, %s)"%(n,eski,ong,s,p)
        v1=vaqt_ol(eski); v2=vaqt_ol(ong)
        if not v1 or not v2: return "❌ Вақт формати: 9:00, 10:30, 12:00"
        n=tuz_qosh({"tur":"vaqt","sana":s,"pot":p,"vaqt":v1,"yangi":v2})
        if not n: return "⚠️ %s да мос дарс топилмади."%v1
        saqla(); return "🕘 <b>%d та дарс</b> %s → <b>%s</b> га кўчирилди (%s, %s)"%(n,v1,v2,s,p)
    a=qolgan.split()
    if len(a)<4: return "❌ Тўлиқ эмас. /yordam"
    s=sana_ol(a[0]); p=pot_ol(a[1]); v=vaqt_ol(a[2]); qiymat=" ".join(a[3:])
    if not s: return "❌ Сана нотўғри: %s"%a[0]
    if p is None: return "❌ Поток нотўғри: %s"%a[1]
    if not v: return "❌ Вақт нотўғри: %s"%a[2]
    if bosh=="xona":
        n=tuz_qosh({"tur":"xona","sana":s,"pot":p,"vaqt":v,"yangi":qiymat})
        if not n: return "⚠️ Мос дарс топилмади."
        saqla(); return "🚪 <b>%d та дарс</b> хонаси <b>%s</b> қилинди (%s, %s, %s)"%(n,qiymat,s,p,v)
    n=tuz_qosh({"tur":"mavzu","sana":s,"pot":p,"vaqt":v,"yangi":qiymat})
    if not n: return "⚠️ Мос дарс топилмади."
    saqla(); return "📖 <b>%d та дарс</b> мавзуси янгиланди (%s, %s, %s)"%(n,s,p,v)

def api(name,params,timeout=70):
    d=urllib.parse.urlencode(params).encode()
    rq=urllib.request.Request("https://api.telegram.org/bot%s/%s"%(TOKEN,name),data=d)
    try:
        with urllib.request.urlopen(rq,timeout=timeout) as r: return json.loads(r.read().decode())
    except Exception as e:
        print("api %s: %s"%(name,e)); return {}

def chunks(s,n=3500):
    out=[];cur=""
    for para in s.split("\n"):
        if len(cur)+len(para)+1>n: out.append(cur); cur=para
        else: cur=cur+"\n"+para if cur else para
    if cur: out.append(cur)
    return out

def reply(cid,text):
    for part in chunks(text):
        api("sendMessage",{"chat_id":cid,"text":part,"parse_mode":"HTML",
            "disable_web_page_preview":"true","reply_markup":json.dumps(kb(cid))})
        time.sleep(0.3)

def day_text(day,title):
    ls=[l for l in LES() if l["d"]==day]
    h="📅 <b>%s — %s, %s</b>"%(title,day.strftime("%d.%m.%Y"),KUN[day.weekday()])
    if not ls: return h+"\n\nБу куни дарс йўқ."
    p=[h,""]
    for t in SLOTLAR():
        cur=[l for l in ls if l["t"]==t]
        if not cur: continue
        p.append("🕘 <b>%s</b>"%t); p+=[block(l) for l in cur]; p.append("")
    return "\n".join(p).strip()

def week_text(today):
    mon=today-dt.timedelta(days=today.weekday())
    return "\n\n".join(day_text(mon+dt.timedelta(days=i),
                       KUN[(mon+dt.timedelta(days=i)).weekday()].capitalize()) for i in range(5))

def saqla():
    if not os.environ.get("GITHUB_ACTIONS"): return
    os.system('git config user.name "dhf-bot"; '
              'git config user.email "41898282+github-actions[bot]@users.noreply.github.com"; '
              'git add .state; git commit -m "holat" >/dev/null 2>&1; '
              'git pull --rebase --autostash >/dev/null 2>&1; git push >/dev/null 2>&1')

def vazifa():
    now=dt.datetime.now(TZ); today=now.date()
    if now.hour==18 and not already("digest-%s"%(today+dt.timedelta(days=1))):
        digest(); saqla()
    if today.weekday()<5:
        for slot in SLOTLAR():
            hh,mm=(int(x) for x in slot.split(":"))
            start=now.replace(hour=hh,minute=mm,second=0,microsecond=0)
            d=(start-now).total_seconds()
            if 0<d<=630 and not already("remind-%s-%s"%(today,slot)):
                remind(slot); saqla()

def xabarni_qayta_ishla(cid,txt):
    cid=str(cid); low=txt.lower(); today=dt.datetime.now(TZ).date()
    j=admin_buyruq(cid,txt)
    if j is not None: reply(cid,j); return
    if YOQ.lower() in low or low.startswith("/obuna") or low.startswith("/yoq"):
        yangi=obuna_qosh(cid); saqla()
        reply(cid,("🔔 <b>Эслатма ёқилди.</b>\nЭнди ҳар дарсдан <b>10 дақиқа олдин</b> ва кечқурун "
                   "<b>18:00</b> да эртанги жадвал шу ерга келиб туради.\n"
                   "Ўчириш учун «%s» тугмасини босинг."%OCH) if yangi else
                  "🔔 Эслатма аллақачон ёқилган.")
        return
    if OCH.lower() in low or low.startswith("/toxtat") or low.startswith("/stop"):
        obuna_ol(cid); saqla()
        reply(cid,"🔕 <b>Эслатма ўчирилди.</b>\nҚайта ёқиш учун «%s» тугмасини босинг."%YOQ); return
    if "эртага" in low or low.startswith("/ertaga"):
        reply(cid,day_text(today+dt.timedelta(days=1),"Эртага")); return
    if "ҳафта" in low or low.startswith("/hafta"):
        reply(cid,week_text(today)); return
    if "бугун" in low or low.startswith("/bugun"):
        reply(cid,day_text(today,"Бугун")); return
    reply(cid,hello(cid)+"\n"+day_text(today,"Бугун")+"\n\n"
          +day_text(today+dt.timedelta(days=1),"Эртага"))

def loop(daqiqa=330):
    if not TOKEN: print("!! TELEGRAM_TOKEN йўқ"); sys.exit(1)
    end=time.time()+daqiqa*60; off=0
    r=api("getUpdates",{"timeout":0,"offset":-1},timeout=30)
    if r.get("result"): off=r["result"][-1]["update_id"]+1
    logga("цикл бошланди (%d дақиқа, обуна: %d, тузатиш: %d)"
          %(daqiqa,len(obunalar()),len(tuzatishlar()))); saqla()
    while time.time()<end:
        try: vazifa()
        except Exception as e: logga("вазифа хатоси: %s"%e)
        r=api("getUpdates",{"timeout":30,"offset":off})
        for u in r.get("result",[]):
            off=u["update_id"]+1
            m=u.get("message") or u.get("edited_message") or {}
            cid=(m.get("chat") or {}).get("id"); txt=m.get("text") or ""
            if cid is None or not txt: continue
            try: xabarni_qayta_ishla(cid,txt)
            except Exception as e: logga("жавоб хатоси: %s"%e)
    try: vazifa()
    except Exception as e: logga("вазифа хатоси: %s"%e)
    logga("цикл тугади")

if __name__=="__main__":
    c=sys.argv[1] if len(sys.argv)>1 else "test"
    if c=="digest": digest()
    elif c=="remind": remind(sys.argv[2])
    elif c=="diag": diag()
    elif c=="javob": loop(int(sys.argv[2]) if len(sys.argv)>2 else 25)
    elif c=="loop": loop(int(sys.argv[2]) if len(sys.argv)>2 else 330)
    else: test()
