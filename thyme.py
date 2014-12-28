# THYME
# music: rehearsal create practice jam write listen performance watch play show studio teach
# social, errands, idle, sleep, eat, travel, shower, brush
# work, exc
# music and social will specify who
# performances should be *.27 and siphon the rest to social

import re
import sys

def time_diff(t0, t1):
    diff = abs(t1 - t0)

    # e.g. 0900, 0945
    if diff < 60:
        # print str(diff) + ' minutes'
        return t1 - t0
    else:
        t1_mins = t1 % 100
        t0_mins = t0 % 100
        t1_hrs = t1 - t1_mins
        t0_hrs = t0  - t0_mins
        mins = t1_mins + (60-t0_mins)
        hrs = abs(((t1_hrs-t0_hrs)/100) - 1)

        if t0 > t1:
            hrs = 24 - hrs

        # print '{} hours and {} minutes'.format(str(hrs), str(mins))

        return hrs*60 + mins


assert time_diff(900, 930) == 30
assert time_diff(2230, 145) == time_diff(1030, 1345)


#Template from main.py

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
t0 = None
t1 = None

amts = {
    'social': 0,
    'errands': 0,
    'wash': 0,
    'travel': 0,
    'work': 0,
    'idle': 0,
    'sleep': 0,
    'eat': 0,
    'prgm': 0,
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

#Params for parsing
data = open('log_thyme.txt', 'r')
begin_counting = False
last_category = 'sleep'
current_category = 'sleep'
start_date = []
end_date = []
sleep_times = []
x_amt = 0

#reverse order of dates
data_reversed = ['init']
date_chunk = ['init']
for line in data:
    if re.search(p_date, line):
        # list manip
        date_chunk.extend(data_reversed)
        data_reversed = date_chunk
        date_chunk = [line]

        # setting start and end dates
        if len(end_date) < 1:
            end_date = [int(i) for i in line.strip().split("/")]
        start_date = [int(i) for i in line.strip().split("/")]
    else:
        date_chunk.append(line)

print ''.join(data_reversed)

#Cmd-line args
if len(sys.argv) > 2:
    start_date = [int(i) for i in sys.argv[1].split("/")]
    end_date = [int(i) for i in sys.argv[2].split("/")]
print str(start_date) + "-" + str(end_date)

for line in data_reversed: #note we go FORWARDS in time
    #it's a dateline
    if re.search(p_date, line):
        date = [int(i) for i in re.search(p_date, line).group().split("/")]
        #begin_counting = in_date_range(date, start_date, end_date)
        if begin_counting == False:
            # if (date[0] == end_date[0] and date[1] <= end_date[1]) or (date[0] < end_date[0]):
            if (date[0] > start_date[0]) or (date[0] == start_date[0] and date[1] >= start_date[1]): 
                begin_counting = True
                print "hooray! " + line
        else:
            num_days += 1
            # if (date[0] == start_date[0] and date[1] <= start_date[1]) or (date[0] < start_date[0]):
            if (date[0] > end_date[0]) or (date[0] == end_date[0] and date[1] >= end_date[1]):
                begin_counting = False
                print "we're done " + line + " "
                break

    #it's a content line
    else:
        if begin_counting == True:
            match = re.search(p_timemark, line) #equiv to match = p_timemark.search(line)
            if match != None:
                time_new = float(match.group()) #default group(0)
                #initialize
                if t0 == None and t1 == None:
                    t1 = time_new
                    continue

                #update
                t0 = t1
                t1 = time_new
                amt = time_diff(t0, t1)
                # print 't0: {}, t1:{}, amt:{}'.format(str(t0), str(t1), str(amt))

                last_category = current_category
                current_category = line

                if re.search(p_music, last_category):
                    #amts['music'] += amt
                    if re.search(p_listen, last_category):
                        music_amts['listen'] += amt
                        continue
                    elif re.search(p_rehearsal, last_category):
                        music_amts['rehearsal'] += amt
                        continue
                    elif re.search(p_performance, last_category):
                        music_amts['performance'] += amt
                        num_performances += 1
                        continue
                    elif re.search(p_write, last_category):
                        music_amts['write'] += amt
                        continue
                    elif re.search(p_practice, last_category):
                        music_amts['practice'] += amt
                        continue
                    elif re.search(p_studio, last_category):
                        music_amts['studio'] += amt
                        continue
                    else:
                        music_amts['other'] += amt
                        print last_category
                    continue
                elif re.search(p_social, last_category):
                    amts['social'] += amt
                    if 'x' in last_category:
                        x_amt += 1
                    continue
                elif re.search(p_errands, last_category):
                    amts['errands'] += amt
                    continue
                elif re.search(p_wash, last_category):
                    amts['wash'] += amt
                    continue
                elif re.search(p_travel, last_category):
                    amts['travel'] += amt
                    continue
                elif re.search(p_work, last_category):
                    # amts['work'] += amt
                    amts['eat'] += 1
                    amt -= 1
                    amts['prgm'] += amt * 0.7
                    amts['idle'] += amt * 0.3
                    continue
                elif re.search(p_idle, last_category):
                    amts['idle'] += amt
                    continue
                elif re.search(p_sleep, last_category):
                    amts['sleep'] += amt
                    if 'nap' not in last_category:
                        sleep_times.append(time_diff(1200, t0)) #offset from 12pm
                    continue
                elif re.search(p_eat, last_category):
                    amts['eat'] += amt
                    continue
                else:
                    amts['other'] += amt
                    #print line
                    continue

amts = dict(amts.items() + {'music': sum(music_amts.values())}.items())
total_mins = sum(amts.values())
total_music = amts['music']

print str(num_days) + ' days total'
print str(num_days*24) + ' vs ' + str(total_mins/60)

for amt in amts:
    print str(amt) + ': ' + str(amts[amt]/60) + ' hours (' + str(round((amts[amt]/60)/num_days, 2)) + ' hrs/day, ' + str(round(100*(amts[amt]/60)/(total_mins/60), 2)) + '% of total)'

print ''

for amt in music_amts:
    print 'music_' + str(amt) + ': ' + str(music_amts[amt]/60) + ' hours (' + str(round((music_amts[amt]/60)/num_days, 2)) + ' hrs/day, ' + str(round(100*(music_amts[amt]/60)/(total_music/60), 2)) + '% of all music)'

print str(num_performances) + ' performances'
print str(x_amt) + ' x\'s'
avg_sleep_offset = (sum(sleep_times) / len(sleep_times)) / 60
avg_sleep_time = [int(avg_sleep_offset-12), int(((avg_sleep_offset-12)%1)*60)]
# print sleep_times
print 'avg sleep time of day: ' + ':'.join(str(i) for i in avg_sleep_time)

num_months = num_days/30.5