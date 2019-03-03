# Event-Log-Preprocessing-Tools

This repo is intended for simple data preprocessing tools for event logs. 

These are standalone python scripts that have self explanatory name and could be run separately from the command line. 

Written in python 3. 

Examle:

```shell
python3 sort_by_timestamp_first_event_in_the_case.py path/to/log caseIdNumber timestampIdNumber
```

You can always run --help function to check the parameters' list.

```shell
python3 sort_by_timestamp_first_event_in_the_case.py --help
```

Out:
```shell
usage: sort_by_timestamp_first_event_in_the_case.py [-h] [--outPath OUTPATH]
                                                    [--delim DELIM]
                                                    [--delimOut DELIMOUT]
                                                    inPath caseInd timeInd

positional arguments:
  inPath               path to event log here (csv)
  caseInd              index of the case column in the csv file (index starts
                       from 0)
  timeInd              index of the timestamp in the csv file (index starts
                       from 0)

optional arguments:
  -h, --help           show this help message and exit
  --outPath OUTPATH    output file name (in case not provided, saved in the
                       same folder with appended name with 'timestamp_sorted'
                       strong)
  --delim DELIM        delimiter used (if not standard: ',')
  --delimOut DELIMOUT  delimiter used to output (if not standard: ',')
```
  
