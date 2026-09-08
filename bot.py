

if len(sys.argv)>1 and sys.argv[1]=="diag":
    import urllib.error
    def call(name,q=""):
        u="https://api.telegram.org/bot%s/%s%s"%(TOKEN,name,q)
        try:
            print(name,"->",urllib.request.urlopen(u,timeout=20).read().decode()[:400])
        except urllib.error.HTTPError as e:
            print(name,"-> ХАТО",e.code,e.read().decode()[:400])
        except Exception as e:
            print(name,"-> ХАТО",type(e).__name__)
    print("CHAT_ID узунлиги:",len(CHAT),"| биринчи белги:",CHAT[:1])
    call("getMe")
    call("getChat","?chat_id="+urllib.parse.quote(CHAT))
    b=urllib.parse.urlencode({"chat_id":CHAT,"text":"диагностика"}).encode()
    try:
        rq=urllib.request.Request("https://api.telegram.org/bot%s/sendMessage"%TOKEN,data=b)
        print("sendMessage ->",urllib.request.urlopen(rq,timeout=20).read().decode()[:400])
    except urllib.error.HTTPError as e:
        print("sendMessage -> ХАТО",e.code,e.read().decode()[:400])
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

def send(text):
    if not TOKEN or not CHAT:
        print("!! TELEGRAM_TOKEN ёки TELEGRAM_CHAT_ID берилмаган"); sys.exit(1)
    body=urllib.parse.urlencode({"chat_id":CHAT,"text":text,"parse_mode":"HTML",
        "disable_web_page_preview":"true"}).encode()
    req=urllib.request.Request("https://api.telegram.org/bot%s/sendMessage"%TOKEN,data=body)
    for i in range(3):
        try:
            with urllib.request.urlopen(req,timeout=30) as r: print("OK",r.status); return True
        except Exception as e:
            print("хато (%d): %s"%(i+1,e)); time.sleep(5)
    return False

def block(l):
    s=["<b>%s</b> · %s · <i>%s</i>"%(l["code"],l["ty"],l["pot"]),
       "   📖 <b>%d-мавзу.</b> %s"%(l["tno"],l["top"])]
    if l.get("on"): s.append("   ❗️ <b>%s</b>"%l["on"])
    s+=["   👤 %s — %s, <b>%s</b>-хона"%(g,a,b) for g,a,b in l["who"]]
    return "\n".join(s)

def digest():
    day=dt.datetime.now(TZ).date()+dt.timedelta(days=1)
    ls=[l for l in LESSONS if l["d"]==day]
    if not ls: print("эртага дарс йўқ"); return
    p=["📅 <b>Эртага — %s, %s</b>\nДавлат-ҳуқуқий фанлар кафедраси машғулотлари\n"
       %(day.strftime("%d.%m.%Y"),KUN[day.weekday()])]
    for t in SLOTS:
        cur=[l for l in ls if l["t"]==t]
        if not cur: continue
        p.append("🕘 <b>%s</b>"%t); p+=[block(l) for l in cur]; p.append("")
    p.append("<i>Ҳаммага сермаҳсул иш куни тилаймиз!</i>")
    send("\n".join(p).strip())

def remind(slot):
    now=dt.datetime.now(TZ); today=now.date()
    ls=[l for l in LESSONS if l["d"]==today and l["t"]==slot]
    if not ls: print("бугун %s да дарс йўқ"%slot); return
    hh,mm=(int(x) for x in slot.split(":"))
    tgt=now.replace(hour=hh,minute=mm,second=0,microsecond=0)-dt.timedelta(minutes=10)
    w=(tgt-now).total_seconds()
    if w>0: print("кутиш %ds"%w); time.sleep(min(w,1800))
    for l in ls:
        send("⏰ <b>10 дақиқадан сўнг — %s</b>\n\n%s"%(slot,block(l))); time.sleep(1)

def test():
    n=dt.datetime.now(TZ)
    send("✅ <b>Синов хабари</b>\nБот ишламоқда. Ҳозирги вақт: %s\nЖадвалдаги машғулотлар: %d"
         %(n.strftime("%d.%m.%Y %H:%M"),len(LESSONS)))

if __name__=="__main__":
    c=sys.argv[1] if len(sys.argv)>1 else "test"
    if c=="digest": digest()
    elif c=="remind": remind(sys.argv[2])
    else: test()
