import psycopg2
from dotenv import dotenv_values

config = dotenv_values(".env")
from datetime import datetime, timezone, timedelta



# print(config,flush=True)
HOST = config["POSTGRES_HOST"]
PORT = config["POSTGRES_PORT"]
USER = config["POSTGRES_USER"]
PASSWORD = config["POSTGRES_PASSWORD"]
DATABASE = config["POSTGRES_DB"]
HOST = "localhost"
def checkAccessToken(access_token):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    # INSERT INTO full_users_ids (user_id, vk_id,telegram_id,instagram_id) VALUES ((SELECT MAX(user_id) + 1 FROM full_users_ids), null, null, null)
    cur = con.cursor()
    dt = datetime.now()
    d1 = datetime.strftime(dt,"%Y-%m-%dT%H:%M:%SZ")
    cur.execute(f"SELECT * FROM users_token WHERE access_token = '{str(access_token)}' AND expire_date > '{(d1)}'")
    result = cur.fetchall()
    con.close()
    if len(result) == 0:
        return False, False
    return (result[0][0], result[0][1])

def updateToken(address,access_token):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    # INSERT INTO full_users_ids (user_id, vk_id,telegram_id,instagram_id) VALUES ((SELECT MAX(user_id) + 1 FROM full_users_ids), null, null, null)
    t = datetime.now()
    t = t + timedelta(days=2)
    d1 = datetime.strftime(t,"%Y-%m-%dT%H:%M:%SZ")

    cur = con.cursor()
    cur.execute(f"DELETE FROM users_token WHERE user_id = (SELECT id FROM users JOIN users_token ON users.address = '{str(address)}')")
    cur.execute(f"INSERT INTO users_token VALUES ((SELECT id FROM users where address = '{address}'), '{access_token}', '{d1}')")
    con.commit()
    con.close()


# print(checkAccessToken("dasiudhnbhwbf87gewf78wevf879g"))
# print(updateToken("alkg7sd9f0vhdf7g6sjdkajsdl","hawgfyr8veb7wrveer87vhe8rf8"))
# print(checkAccessToken("dasiudhnbhwbf87gewf78wevf879g"))
