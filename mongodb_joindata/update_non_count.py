# -*- coding: utf-8 -*-

"""
@version: ??
@author: congcong
@time: 2016/5/5 14:00
"""

# import timeit  # 使用timeit模块来计时,timeit.timeit('x=sum(range(10))')
# import cProfile  # 使用profile找出瓶颈，给出关于执行时间都花在哪里的更为详细的信息，cProfile.run('main()')
import pymongo


def conn_DB(host_name, port):
    client_conn = pymongo.MongoClient(host_name, port)
    db = client_conn.MDF3_6_Resume
    # db = client_conn.MDF3_6_330W
    return db


def main():
    non_count = 0
    update_count = 0

    db = conn_DB('192.168.6.62', 27017)
    # 遍历查找resume_info中的每条数据
    cursor_info = db.resume_info.find({}, {"id": 1, "c_edu_exp": 1}).limit(200)
    # cursor_zibiao = db.resume_cert.find({}, {"id": 1, "resume_id": 1}).limit(10)
    if cursor_info.count() == 0:
        print "resume_info is empty!"
        exit(1)
    for item in cursor_info:
        # find_cursor = db.resume_cert.find({"id": item['id']}, {"id": 1, "resume_id": 1})
        find_cursor = db.resume_education.find({"id": item["id"]},
                                               {"edu_start_time": 1, "edu_end_time": 1, "school_name": 1,
                                                "edu_major": 1, "education": 1})
        if find_cursor.count() == 0:
            non_count += 1
            db.resume_info.update({"id": item['id']}, {"$set": {"c_edu_exp": ""}})
            update_count += 1
    print "non_count:" + str(non_count)
    print "update_count:" + str(update_count)


if __name__ == '__main__':
    main()
