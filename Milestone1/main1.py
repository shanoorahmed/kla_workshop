import yaml
from yaml.loader import SafeLoader

from datetime import datetime, date
import time

with open('Milestone1A.yaml') as f:
    workflow = yaml.load(f, Loader=SafeLoader)


file1 = open("log1.txt","w")

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
    if execution == "Concurrent":
        print("NO")

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