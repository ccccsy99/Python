# -*- coding: utf-8 -*-

"""
@version: ??
@author: congcong
@time: 2016/5/4 14:56
"""
list=[123456]
s = "20jsaou0twnq"
print s,list

for i in range(0,len(list)):
    del list[i]
print list
print "list"+str(list)

# s = ""
# print s+'zhi    kong'+str(list)

s=""
if not s.strip():
    print "wehat"