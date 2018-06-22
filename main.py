import subprocess
import logging
import sys
import time
import settings
from main_functions import main


log = logging.getLogger()
log.setLevel(logging.DEBUG)
chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
chanel.setFormatter(formatter)
log.addHandler(chanel)


if settings.DEBUG:
    subprocess.run(['heroku', 'ps:scale', 'clock=0', '-a', settings.HEROKU_APP_NAME])
    main()
    subprocess.run(['heroku', 'ps:scale', 'clock=1', '-a', settings.HEROKU_APP_NAME])
else:
    while True:
        try:
            main()
            time.sleep(60)
        except:
            time.sleep(60)
