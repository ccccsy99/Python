# -*- coding: utf-8 -*-

"""
@version: ??
@author: congcong
@time: 2016/4/27 13:13
"""

import pymongo
import codecs
import time


# 连接mongo数据库
def conn_DB(host_name, port):
    client_conn = pymongo.MongoClient(host_name, port)
    # db = client_conn.MDF3_6_Resume
    db = client_conn.MDF3_6_330W
    return db


def main():
    non_count = 0
    update_count = 0
    excep_count = 0

    log = r'./errorLog_cert%s.txt' % time.strftime("%y%m%d%H%M")  # 异常数据存入到文档中

    db = conn_DB('192.168.6.62', 27017)
    # 遍历查找resume_info中的每条数据
    # for item in db.resume_info.find().limit(8):  # need modify
    cursor_info = db.resume_info.find({}, {"id": 1})

    if cursor_info.count() == 0:
        print "resume_info is empty!"
        exit(1)
    for item in cursor_info:
        try:
            # 查找resume_cert中是否存在{"id", item['id']}数据对
            # find_cursor = db.resume_cert.find({"id": item['id']}, {"cert": 1, "cert_time": 1})
            find_cursor = db.resume_education.find({"id": item['id']},
                                                   {"edu_start_time": 1, "edu_end_time": 1, "school_name": 1,
                                                    "edu_major": 1, "education": 1})
            print find_cursor.count()
            if find_cursor.count() == 0:
                # print "zibiao collection does not contain id %s" % (item['id'])
                non_count += 1
                continue

            item_lists = []  # 存放属性数据，列表类型
            item_string = ""  # 存放属性数据，string类型

            for fc in find_cursor:
                if fc:
                    str1 = fc['work_begin_time'] + '\t' + fc['work_end_time'] + '\t' + fc['work_in_company'] + '\t' + \
                           fc['work_department'] + '\t' + fc['work_position'] + '\t' + fc['work_abstract'] + '\t' + fc[
                               'work_grade'] + '\t' + fc['work_xiashu_num'] + '\t' + fc['company_industry'] + '\t' + fc[
                               'report_person'] + '\t' + fc['leave_reason'] + '\t' + fc['reference']  # resume_workexp
                    item_lists.append(str1)
                else:
                    print "fc is null,pass"
                    # 将list类型的数据转换成string类型,问题应该出现在这里
            for i in range(0, len(item_lists)):
                item_string += item_lists[i]
            print item_string
            # "person_certificate"  #"c_edu_exp"  "c_work_exp" "c_pro_exp"  "c_train_exp"    "person_note" "person_profession_skill"  "person_language_skill"  "campus_practice"
            db.resume_info.update({"id": item['id']}, {"$set": {"c_edu_exp": item_string}})  # need modify
            update_count += 1

            # # 一条记录更新之后，需要清空字符串及列表中的数据
            # for i in range(0, len(item_lists)):
            #     del item_lists[i]
            # item_string = ""

            if update_count % 100 == 0:
                print ("%d records have been updated") % (update_count)

                # except Exception, e:
                #     # print "oops,error!"
                #     #print "oops,error!when id is %s" % (item['id'])
                #     excep_count += 1
                #     with codecs.open(log, 'a+') as f:
                #         f.write(str(e))
                #         f.write('\n')

    print "non_count:" + str(non_count)
    print "update_count:" + str(update_count)
    print "excep_count:" + str(excep_count)


if __name__ == '__main__':
    main()
