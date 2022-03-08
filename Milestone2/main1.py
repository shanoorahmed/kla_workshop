import yaml
from yaml.loader import SafeLoader

import csv

from datetime import datetime
import time
import threading

with open('Milestone2A.yaml') as f:
    workflow = yaml.load(f, Loader=SafeLoader)

file1 = open("log1.txt","w")
threads = []
dic = {}

def flow(work, execution, activities):
    now = datetime.now()
    file1.write(f"{now};{work} Entry\n")
    if execution == "Sequential":
        for act in activities:
            if activities[act]['Type'] == "Flow":
                newwork = work + '.' + act
                flow(newwork,activities[act]['Execution'],activities[act]['Activities'])
            elif activities[act]['Type'] == "Task":
                newwork = work + '.' + act
                if activities[act]['Function'] == 'TimeFunction':
                    if 'Condition' in activities[act].keys():
                        taskTime(newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Condition'])
                    else:
                        taskTime(newwork,activities[act]['Function'],activities[act]['Inputs'])
                elif activities[act]['Function'] == 'DataLoad':
                    if 'Condition' in activities[act].keys():
                        taskData(newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Outputs'],activities[act]['Condition'])
                    else:
                        taskData(newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Outputs'])
    elif execution == "Concurrent":
        for act in activities:
            if activities[act]['Type'] == "Flow":
                newwork = work + '.' + act
                thread = threading.Thread(target=flow,args=[newwork,activities[act]['Execution'],activities[act]['Activities']])
                thread.start()
                threads.append([thread,newwork])
            elif activities[act]['Type'] == "Task":
                newwork = work + '.' + act
                if activities[act]['Function'] == 'TimeFunction':
                    if 'Condition' in activities[act].keys():
                        thread = threading.Thread(target=taskTime,args=[newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Condition']])
                    else:
                        thread = threading.Thread(target=taskTime,args=[newwork,activities[act]['Function'],activities[act]['Inputs']])
                elif activities[act]['Function'] == 'DataLoad':
                    if 'Condition' in activities[act].keys():
                        thread = threading.Thread(target=taskData,args=[newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Outputs'],activities[act]['Condition']])
                    else:
                        thread = threading.Thread(target=taskData,args=[newwork,activities[act]['Function'],activities[act]['Inputs'],activities[act]['Outputs']])
                thread.start()
                threads.append([thread,newwork])
        flag = 1
        while flag == 1:
            flag = 0
            for thread in threads:
                if thread[0].is_alive():
                    flag = 1
    now = datetime.now()
    file1.write(f"{now};{work} Exit\n")

def taskTime(work,function,inputs,cond=False):
    now = datetime.now()
    file1.write(f"{now};{work} Entry\n")
    if not cond:
        fun_input = inputs['FunctionInput']
        exc_time = inputs['ExecutionTime']
        file1.write(f"{now};{work} Executing {function} ({fun_input}, {exc_time})\n")
        time.sleep(int(exc_time))
    else:
        fun_input = inputs['FunctionInput']
        exc_time = inputs['ExecutionTime']
        file1.write(f"{now};{work} Executing {function} ({fun_input}, {exc_time})\n")
        time.sleep(int(exc_time))
    now = datetime.now()
    file1.write(f"{now};{work} Exit\n")

def taskData(work,function,inputs,outputs,cond=False):  
    now = datetime.now()
    file1.write(f"{now};{work} Entry\n")
    if not cond:
        file_name = inputs['Filename']
        file = open(file_name)
        reader = csv.reader(file)
        lines = int(len(list(reader))) - 1
        s = '$(' + file_name + '.NoOfDefects' + ')'
        dic[s] = lines
        file1.write(f"{now};{work} Executing {function} ({file_name})\n")
    else:
        sp = cond.split(" ") 
        s = 
        file_name = inputs['Filename']
        file1.write(f"{now};{work} Executing {function} ({file_name})\n")
    now = datetime.now()
    file1.write(f"{now};{work} Exit\n")

for work in workflow:
    flow(work,workflow[work]['Execution'],workflow[work]['Activities'])        