from sched_functions import sched_job
import subprocess
import settings


def modules_manipulations(opirations : {job_id: enabling(true|false)}):
    for i in opirations:
        if opirations[i]:
            sched_job.resume_job(job_id=i)
        else:
            sched_job.pause_job(job_id=i)


def django_control(enabling : (true|false)):  # Disabling heroku server if django app active
    if enabling:
        subprocess.run(['heroku', 'ps:scale', 'clock=0', '-a', settings.HEROKU_APP_NAME])
    else:
        subprocess.run(['heroku', 'ps:scale', 'clock=1', '-a', settings.HEROKU_APP_NAME])
