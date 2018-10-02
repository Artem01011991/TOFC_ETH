from .sched_functions import sched_job


def modules_manipulations(opirations):
    '''
    Pause and resume modules if needed.
    :param opirations: {job_id: enabling(true|false)}
    :return:
    '''
    for i in opirations:
        if opirations[i]:
            sched_job.resume_job(job_id=i)
        else:
            sched_job.pause_job(job_id=i)
