import re
import sys

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
p_alcohol = re.compile("beer|wine|whiskey|vodka|gin|rum|tequila|car bomb|cocktail|coca|shot")
p_food = re.compile("breakfast|lunch|dinner|fruit")
p_rent = re.compile("rent|hotel|motel")
p_travel = re.compile("taxi|cab")
p_entertainment = re.compile("concert|show|ticket")

#Counting vars
expenditure = 0
alcohol = 0
food = 0
rent = 0
other = 0
travel = 0
entertainment = 0

#Parse lines
begin_counting = False
for line in data:
    if re.search(p_date, line):
        date = [int(i) for i in re.search(p_date, line).group().split("/")]
        #begin_counting = in_date_range(date, start_date, end_date)
        if begin_counting == False:
            if (date[0] == end_date[0] and date[1] <= end_date[1]) or (date[0] < end_date[0]):
                begin_counting = True
                print "huzzah! " + line
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

print "total: " + str(expenditure)
print "food: " + str(food)
print "alcohol: " + str(alcohol)
print "rent: " + str(rent)
print "travel: " + str(travel)
print "entertainment: " + str(entertainment)
print "other: " + str(other)



#def in_date_range(date, start, end):
