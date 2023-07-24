import psycopg2
from dotenv import dotenv_values
import hashGenerator
import markdown


config = dotenv_values(".env")
from datetime import datetime, timezone, timedelta



# print(config,flush=True)
HOST = config["POSTGRES_HOST"]
PORT = config["POSTGRES_PORT"]
USER = config["POSTGRES_USER"]
PASSWORD = config["POSTGRES_PASSWORD"]
DATABASE = config["POSTGRES_DB"]
# HOST = "localhost"

def login(address):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()
    cur.execute(f"SELECT id FROM users WHERE address = '{address}'")
    r = cur.fetchall()
    # print(r, flush=True)
    # with open("log.txt","a") as f:
    #     print(f,file=f)
    if len(r) == 0:
        print("here")
        cur.execute(f"INSERT INTO users (address) VALUES ('{address}')")
        con.commit()
        user_id = cur.lastrowid
    else:
        user_id = r[0][0]
    con.commit()
    con.close()
    access_token = updateToken(address)
    return user_id, access_token


def checkAccessToken(access_token):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    # INSERT INTO full_users_ids (user_id, vk_id,telegram_id,instagram_id) VALUES ((SELECT MAX(user_id) + 1 FROM full_users_ids), null, null, null)
    cur = con.cursor()
    dt = datetime.now()
    d1 = datetime.strftime(dt,"%Y-%m-%dT%H:%M:%SZ")
    print(f"SELECT * FROM users_token WHERE access_token = '{str(access_token)}' AND expire_date > CURRENT_TIMESTAMP", flush=True)
    cur.execute(f"SELECT * FROM users_token WHERE access_token = '{str(access_token)}' AND expire_date > '{(d1)}'")
    result = cur.fetchall()
    con.close()
    if len(result) == 0:
        return False, False, False
    return (result[0][0], result[0][1], result[0][2])
    #        user_id        token          date

def updateToken(address):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    # INSERT INTO full_users_ids (user_id, vk_id,telegram_id,instagram_id) VALUES ((SELECT MAX(user_id) + 1 FROM full_users_ids), null, null, null)
    t = datetime.now()
    t = t + timedelta(days=2)
    d1 = datetime.strftime(t,"%Y-%m-%dT%H:%M:%SZ")

    access_token = str(hashGenerator.simpleHash())

    cur = con.cursor()
    cur.execute(f"DELETE FROM users_token WHERE user_id = (SELECT id FROM users WHERE address = '{str(address)}')")
    con.commit()

    cur.execute(f"INSERT INTO users_token VALUES ((SELECT id FROM users where address = '{address}'), '{access_token}', '{d1}')")
    con.commit()
    con.close()
    return access_token

def addCutToDB(access_token, filename, paid):
    # INSERT INTO full_users_ids (user_id, vk_id,telegram_id,instagram_id) VALUES ((SELECT MAX(user_id) + 1 FROM full_users_ids), null, null, null)
    t = datetime.now()
    d1 = datetime.strftime(t,"%Y-%m-%dT%H:%M:%SZ")


    user_id, access_token, expire_date = checkAccessToken(access_token)

    print("User's id", user_id, flush=True)

    if user_id == False:
        return False

    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()
    cur.execute(f"INSERT INTO cuts(fileurl, authorid, publicdate, paid) VALUES ('{filename}', {int(user_id)}, CURRENT_TIMESTAMP, '{paid}')")
    con.commit()
    con.close()
    return True


def getCutUrl(cut_id, file_content=False, html_format=False):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()
    cur.execute(f"SELECT fileUrl FROM cuts WHERE id = {int(cut_id)}")
    result = (cur.fetchall())
    con.close()
    if len(result) == 0:
        return None
    else:
        if file_content:
            if html_format:
                return markdown.markdown(open('cuts/'+ result[0][0],'r').read())
            return open('cuts/'+ result[0][0],'r').read()
        else:
            return result[0][0]

def getPaper(paper_id,level):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()
    # cur.execute(f"SELECT cut_id, fileurl FROM cuts_to_paper JOIN cuts ON cuts_to_paper.cut_id = cuts.id WHERE paper_id = 1")
    cur.execute(f"SELECT cut_id from cuts_to_paper JOIN (SELECT id FROM cuts as c JOIN subscriptions as s ON s.author_id = c.authorid WHERE s.sub_level <= {int(level)} and c.paid = true) as level_s on level_s.id = cuts_to_paper.cut_id WHERE paper_id = {int(paper_id)}")
    cut_ids = (cur.fetchall())
    con.close()
    result = []
    for cut in cut_ids:
        # print(cut)
        result.append(getCutUrl(cut[0],file_content=True, html_format=True))
    return result
    

def getUsersPaper(user_id):
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = con.cursor()
    # cur.execute(f"SELECT cut_id, fileurl FROM cuts_to_paper JOIN cuts ON cuts_to_paper.cut_id = cuts.id WHERE paper_id = 1")
    cur.execute(f"SELECT id FROM papers WHERE user_id = {int(user_id)}")
    paper_ids = (cur.fetchall())
    con.close()
    result = []
    for id in paper_ids:
        result.append(id[0])
    return result
    

# print(login("0x3a29f07c909e7dc17ebf545f602ba3300a408391"))
# print(getPaper(1, 2))
