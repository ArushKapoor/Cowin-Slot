import schedule
import time
from cowin_alert import cowin


def do_nothing():
    print("Arush")


# schedule.every(1).minutes.do(cowin)
schedule.every(5).seconds.do(cowin)

while 1:
    schedule.run_pending()
    time.sleep(1)
