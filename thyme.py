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
        #print str(upper-lower) + ' minutes'
        return upper - lower
    else:
        upper_mins = upper%100
        lower_mins = lower%100
        upper_hrs = upper - upper_mins
        lower_hrs = lower  - lower_mins

        mins = upper_mins + (60-lower_mins)
        hrs = ((upper_hrs-lower_hrs)/100) - 1
        #print '{} hours and {} minutes'.format(str(hrs), str(mins))

        return hrs*60 + mins

print time_diff(1545, 1930)

#Template from main.py

#Cmd-line args
#e.g. for tour expenses go "python main.py 3/7 3/20"
start_date = [int(i) for i in sys.argv[1].split("/")]
end_date = [int(i) for i in sys.argv[2].split("/")]
#print start_date + "-" + end_date

#Regexes for params
p_date = re.compile('\d{1,2}/\d{1,2}$')
p_timemark = re.compile('^\d+(\.\d+)*(?=\s)')

p_music = re.compile('music')
p_listen = re.compile('listen|watch|teach|lesson') #consume
p_rehearsal = re.compile('rehearsal|jam') #public making music but not for audience
p_performance = re.compile('performance|show') #public playing for an audience
p_write = re.compile('write|create') #private composing, writing
p_practice = re.compile('practice') #private practice
p_studio = re.compile('studio')

p_social = re.compile('social')
p_errands = re.compile('errand')
p_wash = re.compile('shower|brush|wash')
p_travel = re.compile('travel')
p_work = re.compile('work')
p_idle = re.compile('idle|watch|isle')
p_sleep = re.compile('sleep|nap')
p_eat = re.compile('eat|dinner|breakfast|lunch')

#Counting vars
num_days = 0
num_months = 1
time_x = 1100 #first entry
time_y = time_x

music_amt = 0
listen_amt = 0
rehearsal_amt = 0
performance_amt = 0
write_amt = 0
practice_amt = 0
studio_amt = 0

social_amt = 0
errands_amt = 0
wash_amt = 0
travel_amt = 0
work_amt = 0
idle_amt = 0
sleep_amt = 0
eat_amt = 0
other_amt = 0

#Parse lines
data = open('log_thyme.txt', 'r')
begin_counting = False

for line in data:
    #it's a dateline
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

    #it's a content line
    else:
        if begin_counting == True:
            match = re.search(p_timemark, line) #equiv to match = p_timemark.search(line)
            if match != None:
                time_new = float(match.group()) #default group(0)
                time_x = time_y
                time_y = time_new

                amt = time_diff(time_x, time_y)

                if re.search(p_music, line):
                    music_amt += amt
                    if re.search(p_listen, line):
                        listen_amt += amt
                        continue
                    elif re.search(p_rehearsal, line):
                        rehearsal_amt += amt
                        continue
                    elif re.search(p_performance, line):
                        performance_amt += amt
                        continue
                    elif re.search(p_write, line):
                        write_amt += amt
                        continue
                    elif re.search(p_practice, line):
                        practice_amt += amt
                        continue
                    elif re.search(p_studio, line):
                        studio_amt += amt
                        continue
                    else:
                        print line
                    continue
                elif re.search(p_social, line):
                    social_amt += amt
                    continue
                elif re.search(p_errands, line):
                    errands_amt += amt
                    continue
                elif re.search(p_wash, line):
                    wash_amt += amt
                    continue
                elif re.search(p_travel, line):
                    travel_amt += amt
                    continue
                elif re.search(p_work, line):
                    work_amt += amt
                    continue
                elif re.search(p_idle, line):
                    idle_amt += amt
                    continue
                elif re.search(p_sleep, line):
                    sleep_amt += amt
                    continue
                elif re.search(p_eat, line):
                    eat_amt += amt
                    continue
                else:
                    other_amt += amt
                    #print line
                    continue

for amt in [music_amt, social_amt, errands_amt]:
    print ''

num_months = num_days/30.5