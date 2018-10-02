from apscheduler.schedulers.blocking import BlockingScheduler
from .main_functions import main_index, main_binance


sched_job = BlockingScheduler()


@sched_job.scheduled_job('interval', minutes=1, id='index')
def main_index_sched():
    main_index()


@sched_job.scheduled_job('interval', minutes=1, id='binance')
def main_binance_sched():
    main_binance()
