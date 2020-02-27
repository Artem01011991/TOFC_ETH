import logging
import subprocess
import sys

from tofc_eth.conf import settings
from tofc_eth.schedulers.handlers import sched_job

log = logging.getLogger()
log.setLevel(logging.DEBUG)
chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
chanel.setFormatter(formatter)
log.addHandler(chanel)


if settings.DEBUG:
    from tofc_eth.main_functions import main_index, main_binance

    subprocess.run(["heroku", "ps:scale", "clock=0", "-a", settings.HEROKU_APP_NAME])
    log.info("*******INDEX********")
    main_index()
    log.info("*******BINANCE********")
    main_binance()
    subprocess.run(["heroku", "ps:scale", "clock=1", "-a", settings.HEROKU_APP_NAME])
else:
    sched_job.start()
