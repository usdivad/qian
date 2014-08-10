# THYME
# music: rehearsal create practice jam write listen performance watch play show studio teach
# social, errands, idle, sleep, eat, travel, shower, brush
# work, exc
# music and social will specify who
# performances should be *.27 and siphon the rest to social

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
        print str(upper-lower) + ' minutes'
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

print time_diff(1545, 1930)

#Template from main.py

#Cmd-line args
#e.g. for tour expenses go "python main.py 3/7 3/20"
start_date = [int(i) for i in sys.argv[1].split("/")]
end_date = [int(i) for i in sys.argv[2].split("/")]
#print start_date + "-" + end_date

#Regexes for params
p_date = re.compile("\d{1,2}/\d{1,2}$")

#Counting vars
num_days = 0
num_months = 1

#Parse lines
data = open('log.txt', 'r')
begin_counting = False
for line in data:
    if re.search(p_date, line):
        num_days += 1
        date = [int(i) for i in re.search(p_date, line).group().split("/")]
        #begin_counting = in_date_range(date, start_date, end_date)
        if begin_counting == False:
            if (date[0] == end_date[0] and date[1] <= end_date[1]) or (date[0] < end_date[0]):
                begin_counting = True
                print "hooray! " + line
        else:
            if (date[0] == start_date[0] and date[1] <= start_date[1]) or (date[0] < start_date[0]):
                begin_counting = False
                print "we're done " + line + " "
                break
    else:
        if begin_counting == True:
            match = re.search(p_expenditure, line) #equiv to match = p_expenditure.search(line)
            if match != None:
                amt = float(match.group()) #default group(0)
                expenditure += amt
                if re.search(p_food, line):
                    food += amt
                    continue
                elif re.search(p_alcohol, line):
                    if not re.search(re.compile("drum|wine glasses"), line):
                        alcohol += amt
                        print line
                        continue
                elif re.search(p_rent, line):
                    rent += amt
                    continue
                elif re.search(p_travel, line):
                    travel += amt
                    continue
                elif re.search(p_entertainment, line):
                    entertainment += amt
                    continue
                elif re.search(p_home, line):
                    home += amt
                    continue
                else:
                    other += amt
                    continue
                    #print line
            else:
                ematch = re.search(p_earnings, line)
                if ematch != None:
                    amt = float(ematch.group().replace('+', ''))
                    earnings += amt
                    #print line

num_months = num_days/30.5