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

print time_diff(0000, 900)

#Template from main.py

#Cmd-line args
#e.g. for tour expenses go "python main.py 3/7 3/20"
start_date = [int(i) for i in sys.argv[1].split("/")]
end_date = [int(i) for i in sys.argv[2].split("/")]
print str(start_date) + "-" + str(end_date)

#Regexes for params
p_date = re.compile('\d{1,2}/\d{1,2}$')
p_timemark = re.compile('^\d+(\.\d+)*(?=\s)')

p_music = re.compile('music')
p_listen = re.compile('listen|watch|teach|lesson') #consume
p_rehearsal = re.compile('rehears|jam|soundcheck|birthday') #public making music but not for audience
p_performance = re.compile('perform|show') #public playing for an audience
p_write = re.compile('write|create|compose|beat|programming|mix') #private composing, writing
p_practice = re.compile('practice|drum') #private practice
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

amts = {
    'social': 0,
    'errands': 0,
    'wash': 0,
    'travel': 0,
    'work': 0,
    'idle': 0,
    'sleep': 0,
    'eat': 0,
    'other': 0
}

music_amts = {
    'other': 0,
    'listen': 0,
    'rehearsal': 0,
    'performance': 0,
    'write': 0,
    'practice': 0,
    'studio': 0
}

num_performances = 0

#Parse lines
data = open('log_thyme.txt', 'r')
begin_counting = False

for line in data: #note we go backwards in time
    #it's a dateline
    if re.search(p_date, line):
        num_days += 1
        date = [int(i) for i in re.search(p_date, line).group().split("/")]
        #begin_counting = in_date_range(date, start_date, end_date)
        if begin_counting == False:
            if (date[0] == end_date[0] and date[1] <= end_date[1]) or (date[0] < end_date[0]):
            #if (date[0] > start_date[0]) or (date[0] == start_date[0] and date[1] >= start_date[1]): 
                begin_counting = True
                print "hooray! " + line
        else:
            if (date[0] == start_date[0] and date[1] <= start_date[1]) or (date[0] < start_date[0]):
            #if (date[0] > end_date[0]) or (date[0] == end_date[0] and date[1] >= end_date[1]):
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
                    #amts['music'] += amt
                    if re.search(p_listen, line):
                        music_amts['listen'] += amt
                        continue
                    elif re.search(p_rehearsal, line):
                        music_amts['rehearsal'] += amt
                        continue
                    elif re.search(p_performance, line):
                        music_amts['performance'] += amt
                        num_performances += 1
                        continue
                    elif re.search(p_write, line):
                        music_amts['write'] += amt
                        continue
                    elif re.search(p_practice, line):
                        music_amts['practice'] += amt
                        continue
                    elif re.search(p_studio, line):
                        music_amts['studio'] += amt
                        continue
                    else:
                        music_amts['other'] += amt
                        print line
                    continue
                elif re.search(p_social, line):
                    amts['social'] += amt
                    continue
                elif re.search(p_errands, line):
                    amts['errands'] += amt
                    continue
                elif re.search(p_wash, line):
                    amts['wash'] += amt
                    continue
                elif re.search(p_travel, line):
                    amts['travel'] += amt
                    continue
                elif re.search(p_work, line):
                    amts['work'] += amt
                    continue
                elif re.search(p_idle, line):
                    amts['idle'] += amt
                    continue
                elif re.search(p_sleep, line):
                    amts['sleep'] += amt
                    continue
                elif re.search(p_eat, line):
                    amts['eat'] += amt
                    continue
                else:
                    amts['other'] += amt
                    #print line
                    continue

amts = dict(amts.items() + {'music': sum(music_amts.values())}.items())
for amt in amts:
    print str(amt) + ': ' + str(amts[amt]/60) + ' hours'

print ''

for amt in music_amts:
    print 'music_' + str(amt) + ': ' + str(music_amts[amt]/60) + ' hours' + '(' 

print str(num_performances) + ' performances'

num_months = num_days/30.5