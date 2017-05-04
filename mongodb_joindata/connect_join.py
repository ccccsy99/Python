# -*- coding: utf-8 -*-

"""
@version: ??
@author: congcong
@time: 2016/5/5 14:58
"""

# import timeit  # 使用timeit模块来计时,timeit.timeit('x=sum(range(10))')
# import cProfile  # 使用profile找出瓶颈，给出关于执行时间都花在哪里的更为详细的信息，cProfile.run('main()')
import pymongo
import time
import codecs


def conn_DB(host_name, port):
    client_conn = pymongo.MongoClient(host_name, port)
    #db = client_conn.MDF3_6_Resume
    db = client_conn.MDF3_6_330W
    return db


def main():
    non_count = 0
    update_count = 0
    excep_count = 0
    sum = 0

    log = r'./errorLog_edu%s.txt' % time.strftime("%y%m%d%H%M")

    db = conn_DB('192.168.6.62', 27017)
    # 遍历查找resume_info中的每条数据
    cursor_info = db.resume_info.find({}, {"id": 1, "resume_id": 1})
    # cursor_zibiao = db.resume_cert.find({}, {"id": 1, "resume_id": 1}).limit(10)
    if cursor_info.count() == 0:
        print "resume_info is empty!"
        exit(1)
    for item in cursor_info.batch_size(30):#pymongo.errors.CursorNotFound: Cursor not found, cursor id: 3747045288255998531
        try:
            # 查找resume_cert中是否存在{"id", item['id']}数据对
            find_cursor = db.resume_cert.find({"id": item['id']}, {"id": 1, "resume_id": 1})#need modify

            if find_cursor.count() == 0:
                non_count += 1
                continue

            # print find_cursor.count()
            str_item = item['resume_id']
            #print item['id']
            # print str_item
            db.resume_cert.update({"id": item['id']}, {"$set": {"resume_id": str_item}}, multi=True)#need modify
            update_count += 1
            sum += find_cursor.count()

            if update_count % 100 == 0:
                print ("%d records have been updated") % (update_count)
        except Exception, e:
            # print "oops,error!when id is %s" % (item['id'])
            excep_count += 1
            with codecs.open(log, 'a+') as f:
                f.write(str(e))
                f.write('\n')
    print "non_count:" + str(non_count)
    print "update_count:" + str(update_count)
    print "excep_count:" + str(excep_count)
    print "update sum:zibiao records are " + str(sum)


if __name__ == '__main__':
    main()
