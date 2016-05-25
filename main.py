# -*- coding: utf-8 -*-

from flask import Flask, request, make_response
import json, os, psycopg2, urlparse

app = Flask(__name__)

##################################################################

def db_init():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    db_createTables(cur)
    
    return conn, cur
      
def db_createTables(cur):
  cur.execute('''\
    CREATE TABLE IF NOT EXISTS Product (
      pid SERIAL,
      name varchar,
      price float
    );
    INSERT INTO Product (name,price) Values ('Pomme',5)
    INSERT INTO Product (name,price) Values ('Orange',6)
    INSERT INTO Product (name,price) Values ('Poire',5)
    ''')


def db_select(cur, sql, params = None):
  if params:
    cur.execute(sql, params)
  else:
    cur.execute(sql)
  
  rows = cur.fetchall()
  cleanRows = []
  if rows != None:
    columns = map(lambda d: d[0], cur.description)
    for row in rows:
      cleanRow = dict()
      for (i,colName) in enumerate(columns):
        cleanRow[colName] = row[i]
      cleanRows.append(cleanRow)
  
  return cleanRows

##################################################################

@app.route('/ini')
def ini():
  conn, cur = db_init()
  db_createTables(cur)
  conn.close()
  return "Fait"

@app.route('/products/<productId>')
def desc_produit(productId):
  conn, cur = db_init()
  result = db_select(cur, 'SELECT * FROM Product Where pid ='+ productId )
  conn.close()
  
  resp = make_response(json.dumps(result))
  resp.mimetype = 'application/json'
  return resp

@app.route('/products', methods = ["POST"])
def products_add():
  conn, cur = db_init()
  result = db_select(cur, 'SELECT pid, name FROM Product')
  conn.close()
  
  resp = make_response(json.dumps(result))
  resp.mimetype = 'application/json'
  return resp

@app.route('/products')
def products_fetchall():
  conn, cur = db_init()
  result = db_select(cur, 'SELECT pid, name FROM Product')
  conn.close()
  
  resp = make_response(json.dumps(result))
  resp.mimetype = 'application/json'
  return resp

if __name__ == "__main__":
  app.run()

