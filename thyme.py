import re
import sys

def time_diff(x, y):
    diff = 0
    upper = 0
    lower = 0
    if x > y:
        upper = x
        lower = y
    else:
        upper = y
        lower = x

    if upper - lower < 60:
        return upper - lower
    else:
        upper_mins = upper%100
        lower_mins = lower%100
        upper_hrs = upper - upper_mins
        lower_hrs = lower  - lower_mins

        mins = upper_mins + (60-lower_mins)
        hrs = ((upper_hrs-lower_hrs)/100) - 1
        print '{} hours and {} minutes'.format(str(hrs), str(mins))

        return hrs*60 + mins

print time_diff(1745, 1930)

# #Cmd-line args
# #e.g. for tour expenses go "python main.py 3/7 3/20"
# start_date = [int(i) for i in sys.argv[1].split("/")]
# end_date = [int(i) for i in sys.argv[2].split("/")]
# #print start_date + "-" + end_date