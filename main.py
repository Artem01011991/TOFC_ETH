from sched_functions import sched_job
from controling_opirations import modules_manipulations
import settings
import configparser
import logging
import sys


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
    (settings.SCHEDULER_IDS['index'], conf['Bot section'].getboolen('index activation mode'),),) if not v}  # modules which shoud be disabled

if disabled_modules:   # for modules with value 'False'
    modules_manipulations(disabled_modules)

try:
    sched_job.start()
except:
    for i in settings.CONFIG_MODULES_OPTION_NAME:
        conf[i] = 'false'

    with open(settings.CONFIG_FILE_NAME, 'w') as ini_file:
        conf.write(ini_file)
        ini_file.close()

    modules_manipulations({settings.SCHEDULER_IDS['binance']: False, settings.SCHEDULER_IDS['index']: False})
