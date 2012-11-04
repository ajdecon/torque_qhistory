# torque_accounting.py
#   Functions for working with Torque accounting files

def parse_line(line):
    event = line.split(';')
    job_name = event[2]
    event_type = event[1]
    event_time = event[0]
    
    properties={}
    prop_strings = event.split(" ")
    for p in prop_strings:
        prop=p.split("=")
        if len(prop)=2:
            properties[prop[0]] = prop[1]

    return (job_name, event_type, event_time, properties)

def parse_records(text):
    jobs = {}

    lines=text.split("\n")

    for line in lines:
        job_name, event_type, event_time, properties = parse_line(line)
        if not job_name in jobs:
            jobs[job_name] = {}
            jobs[job_name]['events'] = {}
        jobs[job_name]['events'][event_type]=event_time
        
        for p in properties:
            jobs[job_name][p]=properties[p]

    return jobs
