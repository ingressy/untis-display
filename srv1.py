import datetime, os, webuntis.objects, logging
from dotenv import load_dotenv

logging.basicConfig(
    filename="srv.log",
    encoding="utf-8",
    level=logging.INFO,
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

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
        logging.ERROR(f"Keine Daten von Raum ",{raum})
    elif isinstance(s, str):
        logging.ERROR(f"Fehlerhafte Daten von Raum", {raum})
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
                try:
                    print(s + "-" + e, k, sub, t, r, c)
                except IndexError:
                    logging.error(f"Fehler im Belegungsplan von Raum {raum}")
        logging.info(f"Daten von Raum {raum} erhalten ...")

def main():
    gib_raum_info("2.304")
    gib_raum_info("2.306")
    gib_raum_info("2.311")


if __name__ == "__main__":
    main()