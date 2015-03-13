# torque_accounting.py
#   Functions for working with Torque accounting files
from datetime import datetime
import sys

# strfdelta: formatted print for timedelta object
# with thanks to http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects
def strfdelta(tdelta, fmt):
    d = {'days': tdelta.days}
    d['hours'], rem = divmod(tdelta.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)
    # Force 2-digit values
    d['hours'] = "%02d" % d['hours']
    d['minutes'] = "%02d" % d['minutes']
    d['seconds'] = "%02d" % d['seconds']
    return fmt.format(**d)

def parse_line(line, debug):
    event = line.split(';')
    job_name = event[2]
    event_type = event[1]
    event_time = event[0]
    
    properties={}
    prop_strings = event[3].split(" ")
    for p in prop_strings:
        # DBG: Don't over-split complex node flags
        prop=p.split("=", 1)
        if debug==1:
         print "Parsing p " + p + " (len " + str(len(prop)) + ")"
        if len(prop)==2:
            properties[prop[0]] = prop[1]
            if debug==1:
             print "Parsing property " + prop[0]
            # DBG: Deal with : separated node fields, but only for node flags
            if "nodes" in prop[0]:
                thisprop=prop[0]
                flags=prop[1].split(":")
                if len(flags) > 1:
                    for f in flags:
                        subprop=f.split("=")
                        if len(subprop)==2:
                            properties[subprop[0]] = subprop[1]
                            if debug==1:
                             print "Found subprop " + subprop[0] + " = " + subprop[1] + " (for prop " + thisprop + ")"
                        elif len(subprop)==1:
                            propparts=thisprop.split(".")
                            # Differentiate between numeric values and node flags ("gpu")
                            try:
                                properties[propparts[1]] = str(int(subprop[0]))
                                if debug==1:
                                 print "Found subprop " + propparts[1] + " = " + subprop[0] + " (for prop " + thisprop + ")"
                            except ValueError:
                                properties[subprop[0]] = subprop[0]
                                if debug==1:
                                 print "Found subprop " + subprop[0] + " = " + subprop[0] + " (for prop " + thisprop + ")"

    return (job_name, event_type, event_time, properties)

def parse_records(text, debug):
    jobs = {}

    lines=text.split("\n")

    for line in lines:
        if debug==1:
            print line
        if len(line)==0:
            continue
        try:
            job_name, event_type, event_time, properties = parse_line(line, debug)
        except IndexError:
            sys.stderr.write("WARNING: line could not be parsed\n%s\n" % line)
            continue
        if not job_name in jobs:
            jobs[job_name] = {}
            jobs[job_name]['events'] = {}
        jobs[job_name]['events'][event_type]=event_time
        
        for p in properties:
            jobs[job_name][p]=properties[p]
            if debug==1:
                print "Adding j " + job_name + " p " + p + " = " + properties[p]

    return jobs


def calculate_durations(jobs):
    for j in jobs:
        try:
            stime = datetime.strptime(jobs[j]['events']['S'],"%m/%d/%Y %H:%M:%S")
            qtime = datetime.strptime(jobs[j]['events']['Q'],"%m/%d/%Y %H:%M:%S")
            jobs[j]['wait_time']=strfdelta(stime-qtime,"{days}:{hours}:{minutes}:{seconds}")
        except KeyError:
            pass

        try:
            stime = datetime.strptime(jobs[j]['events']['S'],"%m/%d/%Y %H:%M:%S")
            etime = datetime.strptime(jobs[j]['events']['E'],"%m/%d/%Y %H:%M:%S")
            jobs[j]['run_time']=strfdelta(etime-stime,"{days}:{hours}:{minutes}:{seconds}")
        except KeyError:
            pass
    return jobs

def parse_files(filenames, debug):
    texts=[]
    for fname in filenames:
        f = open(fname,'r')
        texts.append(f.read())
        f.close
    return calculate_durations(parse_records("\n".join(texts), debug))


