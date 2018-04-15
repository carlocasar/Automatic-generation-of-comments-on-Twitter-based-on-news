import sqlite3
import json
import newspaper
from newspaper import Article
from datetime import datetime


timeframe = '2017-10'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply
(parent_id TEXT PRIMARY KEY, comment_id TEXT, parent TEXT,
comment TEXT, subreddit TEXT, unix INT, score INT)""")

def format_data(data):
    data = data.replace("\n"," newlinechar ").replace("\r"," newlinechar ").replace('"',"'")
    return data

def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 100:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        return False

def acceptable(data):
    if len(data.split(' ')) > 400 or len(data) < 1 :
        return False
    elif len(data) > 1500:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True

def sql_insert_replace_comment(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET comment_id = "{}", comment = "{}", subreddit = "{}", unix = {}, score = {} WHERE parent_id ="{}";""".format(commentid, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 update',str(e))

def sql_insert_parent(parentid,body,subreddit,time):
    try:
        sql = """INSERT INTO parent_reply (parent_id, parent, subreddit, unix) VALUES ("{}","{}","{}",{});""".format(parentid, body, subreddit, int(time))
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))


def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return True
        else: return False
    except Exception as e:
        return False



if __name__ == "__main__":
    create_table()
    row_counter = 1
    paired_rows = 1
    control = False
    """
    with open("C:/Users/Carlo/Desktop/chatData/json_source_urls.json", buffering = 1000,encoding="utf8") as g:
        for row in g:
            try:
                row = json.loads(row)
                parent_id = row['id']
                if(parent_id == '6i5msi'): control = True
                if (control):
                    subreddit = row['subreddit']
                    created_utc = row ['created_utc']
                    article = Article(row['url'])
                    article.download()
                    article.parse()
                    parent_data = format_data(article.text)
                    if(len(parent_data) > 500):
                        sql_insert_parent(parent_id, parent_data, subreddit, created_utc)
                        row_counter += 1

            except Exception as e:
                pass
            if row_counter  % 100000 == 0:
                print("total rows read: {}".format(row_counter))


    """

    sql = "SELECT parent_id FROM parent_reply"
    c.execute(sql)
    tuple_ids = c.fetchall()
    list_ids = list(sum(tuple_ids, ()))
    print("numero de noticias: {}".format(row_counter))
    print(list_ids[1])
    rows_read = 0


    with open("C:/Users/Carlo/Desktop/chatData/new_comments_noscore.json", buffering = 1000,encoding="utf8") as f:
        for row in f:
            rows_read += 1
            row = json.loads(row)
            parent_id_full = row['parent_id']
            parent_id = parent_id_full[3:]
            if rows_read  % 100000 == 0:
                print("total rows read: {}".format(rows_read))
            if parent_id in list_ids:
                body = format_data(row['body'])
                created_utc = row['created_utc']
                score = int(row['score'])
                subreddit = row['subreddit']
                comment_id = row['id']

                try:
                    if acceptable(body):
                        existing_comment_score = find_existing_score(parent_id)
                        if existing_comment_score:
                            if score > existing_comment_score:
                                sql_insert_replace_comment(comment_id,parent_id,body,subreddit,created_utc,score)

                        else:
                            sql_insert_replace_comment(comment_id,parent_id,body,subreddit,created_utc,score)
                            paired_rows += 1
                    if paired_rows  % 1000 == 0:
                        print("total rows paired: {}".format(paired_rows))

                except Exception as e:
                    print(e)
                    pass
