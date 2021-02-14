import connect, psycopg2 #importing connect.py file and drivers to allow python to talk to the database
print("import done - establishing connection") # confirming the we imported and established the connection
conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, \       
     password=connect.dbpass, host=connect.dbhost, port=connect.dbport) #creating connection through database server, passing varaibels from connect.py
with conn:              #with the connection between database and server, does not allow direct execute the query
    cur = conn.cursor() #query is happen within the cursor, so we need get the cursor
    cur.execute("select * from member;") #execute the query
    select_result = cur.fetchall() #get result of the query,get back all the results


