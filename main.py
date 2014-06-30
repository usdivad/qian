import re
import sys

#Initial prompt
# putty = raw_input("Enter 'all', 'range', or 'month':\n")
# start_date = []
# end_date = []

#Cmd-line args
#e.g. for tour expenses go "python main.py 3/7 3/20"
start_date = [int(i) for i in sys.argv[1].split("/")]
end_date = [int(i) for i in sys.argv[2].split("/")]
#print start_date + "-" + end_date

#Imported data
data = open("log.txt", "r")

#Regexes for params
p_date = re.compile("\d{1,2}/\d{1,2}$")
p_expenditure = re.compile("^\d+(\.\d+)*(?=\s)")
p_alcohol = re.compile("beer|wine|whiskey|vodka|gin|rum|tequila|car bomb|cocktail|coca|shot|margarita|drink|anchor")
p_food = re.compile("breakfast|brunch|lunch|dinner|fruit|food|peanut|ribs|egg|cheese|juice|apple|banana|orange|snack|gyro|pizza|avocado|cream|water|burger|Takoyaki|cafe|smoothie|taco|watermelon|turkey|enchilada|gyro|chicken|lamb|beef|Chinese|Indian|fries")
p_rent = re.compile("rent|hotel|motel|deposit")
p_travel = re.compile("taxi|cab|metrocard|sub|transit")
p_entertainment = re.compile("concert|show|ticket")

#Counting vars
expenditure = 0
alcohol = 0
food = 0
rent = 0
other = 0
travel = 0
entertainment = 0
num_days = 0
num_months = 1

#Parse lines
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
                elif re.search(p_alcohol, line):
                    alcohol += amt
                elif re.search(p_rent, line):
                    rent += amt
                elif re.search(p_travel, line):
                    travel += amt
                elif re.search(p_entertainment, line):
                    entertainment += amt
                else:
                    other += amt
                    #print line

num_months = num_days/30.5

print "total: " + str(expenditure)
print "food: " + str(food)
print "alcohol: " + str(alcohol)
print "rent: " + str(rent)
print "travel: " + str(travel)
print "entertainment: " + str(entertainment)
print "other: " + str(other)
print "avg monthly (" + str(num_days) + " days over 30.5 days/month is " + str(num_months) + " months): " + str(expenditure/num_months)



#def in_date_range(date, start, end):
