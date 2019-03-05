import argparse
import csv
import time
from pathlib import Path
from datetime import datetime


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("inPath", help="path Rto event log here (csv)")
parser.add_argument("--caseInd", help="index of the case column in the csv file (index starts from 0)", type=int)
parser.add_argument("--timeInd", help="index of the timestamp in the csv file (index starts from 0)", type=int)
parser.add_argument("--outPath", help="output file name (in case not provided, saved in the same folder with appended name with \'timestamp_sorted\' strong)")
parser.add_argument("--delim", help="delimiter used (if not standard: \',\')")
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

case_id = None
timestamp_id = None
if not args.caseInd:
    print ("The case ID and timestamp ID are not inputted")
    print ("Choose *case ID* and *timestamp ID* number from next lines:")
    for i in range(len(header)):
        print (str(i) + "  " + header[i])


    case_id = int(input("Case ID is: "))
    timestamp_id = int(input("Timestamp ID is: "))

else:
    case_id = args.caseInd
    timestamp_id = args.timeInd

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

def string_to_timeval(str_time):
    try:
        t = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    except:
        # 2012/04/03 08:55:38.000

        t = datetime.strptime(str_time[:-4], "%Y/%m/%d %H:%M:%S")

    return time.mktime(t.timetuple())


log = sorted(log, key=lambda trace: string_to_timeval(trace[0][timestamp_id]))

if args.outPath:
    out_log_path = args.outPath
else:
    out_log_path = event_log_in.parents[0] / (event_log_in.name[:-4] + "_timestamp_sorted.csv")


# write the result
with open(out_log_path, 'w') as csvfile:
    if args.delimOut:
        spamwriter = csv.writer(csvfile, delimiter=args.delimOut, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    else:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(header)

    for trace in log:
        for event in trace:
            spamwriter.writerow(event)

print ("File outputed to: " + str(out_log_path))
print ("-> Good luck with your further research")


