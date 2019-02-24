import configparser
import logging
import sys

import settings
from TOFC_ETH.controling_opirations import modules_manipulations
from TOFC_ETH.sched_functions import sched_job

log = logging.getLogger()
log.setLevel(logging.DEBUG)
chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
chanel.setFormatter(formatter)
log.addHandler(chanel)

conf = configparser.ConfigParser()
conf.read(settings.CONFIG_FILE_NAME)
disabled_modules = {k: v for k, v in (
    (settings.SCHEDULER_IDS['binance'], conf['Bot section'].getboolen('binance activation mode'),),
    # modules which shoud be disabled
    (settings.SCHEDULER_IDS['index'], conf['Bot section'].getboolen('index activation mode'),),) if not v}

if disabled_modules:   # for modules with value 'False'
    modules_manipulations(disabled_modules)

try:
    sched_job.start()
except Exception:
    for i in settings.CONFIG_MODULES_OPTION_NAME:
        conf[i] = 'false'

    with open(settings.CONFIG_FILE_NAME, 'w') as ini_file:
        conf.write(ini_file)
        ini_file.close()

    modules_manipulations({settings.SCHEDULER_IDS['binance']: False, settings.SCHEDULER_IDS['index']: False})
