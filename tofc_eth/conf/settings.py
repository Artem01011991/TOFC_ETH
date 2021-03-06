import environs

# env vars assignment
env = environs.Env()
environs.Env.read_env()

# project root
root = environs.Path(__file__).parents[1]

# heroku
HEROKU_APP_NAME = env("HEROKU_APP_NAME")

# tradeX
USER_LOGIN = env("USER_LOGIN")
USER_PASS = env("USER_PASS")
USER_WMID = env("USER_WMID")

# db
DATABASE_URL = env("DATABASE_URL")

# binance
BINANCE_APIKEY = env("BINANCE_APIKEY")
BINANCE_SECRETKEY = env("BINANCE_SECRETKEY")
