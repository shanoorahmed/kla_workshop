import yaml
from yaml.loader import SafeLoader

from datetime import datetime
import time
import threading

with open('Milestone1B.yaml') as f:
    workflow = yaml.load(f, Loader=SafeLoader)

file1 = open("log2.txt","w")
threads = []

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
                task(newwork,activities[act]['Function'],activities[act]['Inputs'])
    elif execution == "Concurrent":
        for act in activities:
            if activities[act]['Type'] == "Flow":
                newwork = work + '.' + act
                thread = threading.Thread(target=flow,args=[newwork,activities[act]['Execution'],activities[act]['Activities']])
                thread.start()
                threads.append([thread,newwork])
            elif activities[act]['Type'] == "Task":
                newwork = work + '.' + act
                thread = threading.Thread(target=task,args=[newwork,activities[act]['Function'],activities[act]['Inputs']])
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

def task(work,function,inputs):
    if function == 'TimeFunction':
        fun_input = inputs['FunctionInput']
        exc_time = inputs['ExecutionTime']
        now = datetime.now()
        file1.write(f"{now};{work} Entry\n")
        file1.write(f"{now};{work} Executing {function} ({fun_input}, {exc_time})\n")
        time.sleep(int(exc_time))
        now = datetime.now()
        file1.write(f"{now};{work} Exit\n")

for work in workflow:
    if workflow[work]['Type'] == "Flow":
        flow(work,workflow[work]['Execution'],workflow[work]['Activities'])
    elif workflow[work]['Type'] == "Task":
        task(work,workflow[work]['Function'],workflow[work]['Inputs'])