import datetime, os, webuntis.objects, logging, socket
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

HOST = '127.0.0.1'
PORT = 2450

time = datetime.datetime.now()
chtime = (time.strftime("%H%M"))
chdate = (time.strftime("%Y-%m-%d"))
start = datetime.datetime.now()
end = start + datetime.timedelta(days=5)

def raum_info(raum):
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
        time_format_start = time_format_end
        time_format_date = "%Y-%m-%d"

        for po in tt:
            d = po.start.strftime(time_format_date)
            s = po.start.strftime(time_format_start)
            e = po.end.strftime(time_format_end)
            k = " ".join([k.name for k in po.klassen])
            try:
                t = " ".join([t.full_name for t in po.teachers])
            except IndexError:
                logging.error(f"Fehler bei einem Eintrag einer Lehrkraft von Raum {raum}")
            r = " ".join([r.name for r in po.rooms])
            sub = " ".join([r.long_name for r in po.subjects])
            c = "(" + po.code + ")" if po.code is not None else ""

            if chtime < e:
                print(d, s + "-" + e, k, sub, t, r, c)
        logging.info(f"Daten von Raum {raum} erhalten ...")

def send():
    print("bla")

def main():
    srv = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
    srv.bind((HOST, PORT))
    srv.listen(5)
    c, addr = srv.accept()
    logging.info("Server gestartet!")
    logging.info(f"Socket gestartet mit {HOST} & {PORT}!")

    c.send('ping'.encode())

    raum_info("2.304")
    raum_info("2.306")
    raum_info("2.311")

    #get battery stat
    print(c.recv(1024).decode())
    c.close()

    logging.info("Server gestoppt!")


if __name__ == "__main__":
    main()