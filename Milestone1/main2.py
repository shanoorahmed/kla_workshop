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
    if execution == "Sequential":
        for act in activities:
            now = datetime.now()
            file1.write(f"{now};{work}.{act} Entry\n")
            if activities[act]['Type'] == "Flow":
                newwork = work + '.' + act
                flow(newwork,activities[act]['Execution'],activities[act]['Activities'])
            elif activities[act]['Type'] == "Task":
                newwork = work + '.' + act
                task(newwork,activities[act]['Function'],activities[act]['Inputs'])
            now = datetime.now()
            file1.write(f"{now};{work}.{act} Exit\n")
    elif execution == "Concurrent":
        for act in activities:
            now = datetime.now()
            file1.write(f"{now};{work}.{act} Entry\n")
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
        for thread in threads:
            thread[0].join()
            now = datetime.now()   
            file1.write(f"{now};{thread[1]} Exit\n")

def task(work,function,inputs):
    if function == 'TimeFunction':
        fun_input = inputs['FunctionInput']
        exc_time = inputs['ExecutionTime']
        now = datetime.now()
        file1.write(f"{now};{work} Executing {function} ({fun_input}, {exc_time})\n")
        time.sleep(int(exc_time))

for work in workflow:
    now = datetime.now()
    file1.write(f"{now};{work} Entry\n")
    if workflow[work]['Type'] == "Flow":
        flow(work,workflow[work]['Execution'],workflow[work]['Activities'])
    elif workflow[work]['Type'] == "Task":
        task(work,workflow[work]['Function'],workflow[work]['Inputs'])
    now = datetime.now()
    file1.write(f"{now};{work} Exit")