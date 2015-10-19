import shutil
import MySQLdb

self.mysqlconn = MySQLdb.connect(host='192.168.0.2', user='root',
                                        passwd='root', db='stock')

cursor = self.mysqlconn.cursor()
try:
    cursor.execute("INSERT INTO unbacked_redis_data(unbacked_redis_stock) VALUES ('%s')" % line)
except Exception, e:
    print e
isexists = os.path.exists("/home/zjdx/unbacked_redis_files")
if not isexists:
    os.makedirs("/home/zjdx/unbacked_redis_files")
    print "/home/zjdx/unbacked_redis_files" + u' 创建成功'
shutil.move("/home/zjdx/"+line, "/home/zjdx/unbacked_redis_files")

self.mysqlconn.commit()
self.mysqlconn.close()