import subprocess
import logging
import sys
import time
from settings import DEBUG
from mail_functions import main


log = logging.getLogger()
log.setLevel(logging.DEBUG)
chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
chanel.setFormatter(formatter)
log.addHandler(chanel)


if DEBUG:
    subprocess.run(['heroku', 'ps:scale', 'clock=0', '-a', 'immense-eyrie-59509'])
    main()
    subprocess.run(['heroku', 'ps:scale', 'clock=1', '-a', 'immense-eyrie-59509'])
else:
    while True:
        try:
            main()
            time.sleep(60)
        except:
            time.sleep(60)
