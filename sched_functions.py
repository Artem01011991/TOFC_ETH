from apscheduler.schedulers.blocking import BlockingScheduler
from main_functions import main_index, main_binance
import configparser
import settings


conf = configparser.ConfigParser()
conf.read(settings.CONFIG_FILE_NAME)  # app configurations


sched_job = BlockingScheduler()


if conf['Bot section'].getboolean(settings.CONFIG_MODULES_OPTION_NAME['Index activation mode']):
    @sched_job.scheduled_job('interval', minutes=1, id='index')
    def main_index_sched():
        main_index()


if conf['Bot section'].getboolean(settings.CONFIG_MODULES_OPTION_NAME['Binance activation mode']):
    @sched_job.scheduled_job('interval', minutes=1, id='binance')
    def main_binance_sched():
        main_binance()
