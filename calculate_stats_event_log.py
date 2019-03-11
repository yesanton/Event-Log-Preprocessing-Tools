import argparse
import csv
import time
from pathlib import Path
from datetime import datetime


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(description="This script is able to calculate all the basic stats of the inputtted CSV log")

parser.add_argument("inPath", help="path to event log here (csv)")
parser.add_argument("--delim", help="delimiter used (if not standard: \',\')")

parser.add_argument("--mode", help="mode can be \'short\' or \'full\'")

parser.add_argument("--caseInd", help="index of the case column in the csv file (index starts from 0)", type=int)
parser.add_argument("--timeInd", help="index of the timestamp in the csv file (index starts from 0)", type=int)
parser.add_argument("--actInd", help="index of the activity column in the csv file (index starts from 0)", type=int)

parser.add_argument("--outPath", help="output file name (in case not provided, saved in the same folder with name appened name \"stats\")")
parser.add_argument("--delimOut", help="delimiter used to output (if not standard: \',\')")

args = parser.parse_args()
print(args.inPath)

event_log_in = Path(args.inPath)
opened_event_log = open(event_log_in, 'r')

if args.delim:
    csv_reader = csv.reader(opened_event_log, delimiter=args.delim, quotechar='|')
else:
    csv_reader = csv.reader(opened_event_log, delimiter=',', quotechar='|')

header = next(csv_reader, None)

### we calculate
# number of cases
num_of_cases = 0
cases_happened = set()
# num of distict activities
num_of_distinct_activities = 0
num_of_acitivies_total = 0
activities_per_case = 0
activities_happened = set()

# time range
first_date = None
last_date = None



case_id = None
timestamp_id = None
activ_id = None

if not args.caseInd:
    print ("The case ID, timestamp ID, activity ID are not inputted")
    print ("Choose *case ID*, *timestamp ID* and *activity ID* number from next lines:")
    for i in range(len(header)):
        print (str(i) + "  " + header[i])


    case_id = int(input("Case ID is: "))
    timestamp_id = int(input("Timestamp ID is: "))
    activ_id = int(input("Activity ID is: "))
else:
    case_id = args.caseInd
    timestamp_id = args.timeInd
    activ_id = args.activity

log = []
trace = []
current_case = None
for row in csv_reader:
    #print (row)
    if current_case != row[case_id]:
        # here we finished reading one trace
        if not trace == []:
            log.append(trace)
        trace = [row]
        current_case = row[case_id]
    else:
        trace.append(row)

    num_of_acitivies_total += 1

def string_to_timeval(str_time):
    try:
        t = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    except:
        # 2012/04/03 08:55:38.000

        t = datetime.strptime(str_time[:-4], "%Y/%m/%d %H:%M:%S")

    return time.mktime(t.timetuple())


log = sorted(log, key=lambda trace: string_to_timeval(trace[0][timestamp_id]))

print (timestamp_id)
first_date = log[0][0][timestamp_id]
last_date = log[-1][-1][timestamp_id]


for i in range(len(log)):
    for j in range(len(log[i])):
        activities_happened.add(log[i][j][activ_id])
    cases_happened.add(log[i][0][case_id])

num_of_cases = len(cases_happened)
num_of_distinct_activities = len(activities_happened)

result_lines = []
result_lines.append(['First date:', first_date, 'Last date:', last_date])
result_lines.append(['Number of activities total:', num_of_acitivies_total])
result_lines.append(['Number of activities per case:', num_of_acitivies_total / num_of_cases])

result_lines.append(['Number of ditinct activities:', num_of_distinct_activities])
result_lines.append(['Number of cases:', num_of_cases])
result_lines.append(['List of all activities:'])

if args.mode:
    if args.mode == "full":
        for i in activities_happened:
            result_lines.append([i])



# save stats in the csv
if args.outPath:
    out_log_path = args.outPath
else:
    out_log_path = event_log_in.parents[0] / (event_log_in.name[:-4] + "_stats.csv")


# write the result
with open(out_log_path, 'w') as csvfile:
    if args.delimOut:
        spamwriter = csv.writer(csvfile, delimiter=args.delimOut, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    else:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for result in result_lines:
        spamwriter.writerow(result)
        print (result)
print ("File outputed to: " + str(out_log_path))
print ("-> Good luck with your further research")


