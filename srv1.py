import datetime, os, webuntis.objects
from dotenv import load_dotenv

load_dotenv()
SRV = os.getenv('SRV')
USR = os.getenv('USR')
PWD = os.getenv('PWD')
SHO = os.getenv('SHO')
USRA = os.getenv('USRA')

time = datetime.datetime.now()
chtime = (time.strftime("%H%M"))
chdate = (time.strftime("%Y-%m-%d"))
start = datetime.datetime.now()
end = start + datetime.timedelta(days=5)

def gib_raum_info(raum):
    s = webuntis.Session(
        server=SRV,
        username=USR,
        password=PWD,
        school=SHO,
        useragent=USRA
    )
    s.login()
    if isinstance(s, str):
        # KEINE DATEN JUNGE
        print("KEINE DATEN VON RAUM ", raum)
    else:
        rooms = s.rooms().filter(name=raum)

        tt = s.timetable(room=rooms[0], start=start, end=end)
        tt = sorted(tt, key=lambda x: x.start)

        time_format_end = "%H%M"
        time_format_start = "%Y-%m-%d " + time_format_end

        for po in tt:
            s = po.start.strftime(time_format_start)
            e = po.end.strftime(time_format_end)
            k = " ".join([k.name for k in po.klassen])
            t = " ".join([t.full_name for t in po.teachers])
            r = " ".join([r.name for r in po.rooms])
            sub = " ".join([r.name for r in po.subjects])
            c = "(" + po.code + ")" if po.code is not None else ""

            if chtime < e:
                print(s + "-" + e, k, sub, t, r, c)

def main():
    gib_raum_info("2.311")

if __name__ == "__main__":
    main()