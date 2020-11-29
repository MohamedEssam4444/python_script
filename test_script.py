#!/usr/bin/env python3
import os
import sys
import re
from itertools import chain
from collections import defaultdict
import operator
import csv
import ast
logfile=sys.argv[1]
error_dict=dict()
users_dict_err = dict()
users_dict_info = dict()
with open (logfile) as f: # will iterate over the logfile and use regular expressions to parse it and find the word "error" or the word "info" , if it found "error" in the log then the user made an error if "info" then there is no error form that urser
    for line in f:
        pattern1=r": ([A-Z.]*)" #pattern to know if its' error or info
        pattern2=r": [A-Z.]* ([A-Za-z+' ]*)" #pattern to get info and error type to be put in error_dict and users_dict
        pattern3=r"\((\w.*)\)" #pattern to get users who made error or info to be put in users_dict
        result1=re.search(pattern1,line)
        result2=re.search(pattern2,line)
        result3=re.search(pattern3,line)
        #print(result1[1])
        if result1[1] is None:
            print("ur pattern gets nothing my friend")
            continue
        elif "ERROR" in result1[1]:
            error_dict[result2[1]]=error_dict.get(result2[1],0)+1 #gets each error and how many times it was repeated
            print(error_dict)
            users_dict_err[result3[1]]=users_dict_err.get(result3[1],0)+1#
            users_dict_info[result3[1]]=users_dict_info.get(result3[1],0)
            # print(users_dict_info)
        elif "INFO" in result1[1]:
            users_dict_info[result3[1]]=users_dict_info.get(result3[1],0)+1
            users_dict_err[result3[1]]=users_dict_err.get(result3[1],0)


users_dict = defaultdict(list)

for k, v in chain(users_dict_info.items(),users_dict_err.items()):
    users_dict[k].append(v)

for k, v in users_dict.items():
    newtuple=(k,v)
    # print(k, v)
y=sorted(users_dict.items(), key = operator.itemgetter(0))
error=sorted(error_dict.items(), key = operator.itemgetter(1), reverse=True)
print(error)
sorted_user_str=[y]
sorted_user_str=str(sorted_user_str).replace('[','').replace(']','')
print(sorted_user_str)
per_user=list(eval(sorted_user_str))
print(per_user)
with open ('error_message.csv','w')as err_msg_csv: # generate error_message.csv file
    csv_out=csv.writer(err_msg_csv)
    csv_out.writerow(['Error','Count'])
    for row in error:
        csv_out.writerow(row)
keys=['Username','INFO','ERROR']
with open ('user_statistics.csv','w')as users_msg_csv: # generate user_statistics.csv file
    csv_out=csv.writer(users_msg_csv)
    csv_out.writerow(keys)
    for row in per_user:
        csv_out.writerow(row)
