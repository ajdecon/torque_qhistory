# torque_accounting.py
#   Functions for working with Torque accounting files
from datetime import datetime

def parse_line(line):
    event = line.split(';')
    job_name = event[2]
    event_type = event[1]
    event_time = event[0]
    
    properties={}
    prop_strings = event[3].split(" ")
    for p in prop_strings:
        prop=p.split("=")
        if len(prop)==2:
            properties[prop[0]] = prop[1]

    return (job_name, event_type, event_time, properties)

def parse_records(text):
    jobs = {}

    lines=text.split("\n")

    for line in lines:
        if len(line)==0:
            continue
        job_name, event_type, event_time, properties = parse_line(line)
        if not job_name in jobs:
            jobs[job_name] = {}
            jobs[job_name]['events'] = {}
        jobs[job_name]['events'][event_type]=event_time
        
        for p in properties:
            jobs[job_name][p]=properties[p]

    return jobs


def calculate_durations(jobs):
    for j in jobs:
        try:
            stime = datetime.strptime(jobs[j]['events']['S'],"%m/%d/%Y %H:%M:%S")
            qtime = datetime.strptime(jobs[j]['events']['Q'],"%m/%d/%Y %H:%M:%S")
            jobs[j]['wait_time']=str(stime-qtime)
        except KeyError:
            pass

        try:
            stime = datetime.strptime(jobs[j]['events']['S'],"%m/%d/%Y %H:%M:%S")
            etime = datetime.strptime(jobs[j]['events']['E'],"%m/%d/%Y %H:%M:%S")
            jobs[j]['run_time']=str(etime-stime)
        except KeyError:
            pass
    return jobs

def parse_files(filenames):
    texts=[]
    for fname in filenames:
        f = open(fname,'r')
        texts.append(f.read())
        f.close
    return calculate_durations(parse_records("\n".join(texts)))


