from sutime import SUTime
import re
from datetime import datetime,timedelta
import string 

sutime = SUTime(mark_time_ranges=True, include_range=True)
alphabets = list(string.ascii_uppercase)

def getFigure(time:str)->str:
    "to extract the integer in the text "
    return ''.join([x for x in list(time) if x not in alphabets])



def formatText(text:str)->str:
    """this is to clean up the mail
    
    Keyword arguments:
    text -- the email
    Return: the email in its clean usable format
    """
    
    url = re.compile(r'https?://\S+|www\.\S+|meet\.google\.com\S+')
    text = url.sub(r'',text)
    text = re.sub('@[^\s]+','',text)
    text = re.sub('\n|\r', " ",text)
    return text.strip().lower()


def getValuables(value:dict)->dict:
    """This function fetches the value in the parsed email from the 
    SUTime library
    
    Keyword arguments:
    value -- a json object containing details of the time or date extracted by SUTime

    Return: dict format of the valued date or time 
    """
    
    tag = {}
    if value['type'] == "DURATION":
        try:

            tag.update({'TIME': value['value']['begin']})
        except:
            d = getFigure(value['value'])
            if value['value'].startswith('PT'):
                t = datetime.now() + timedelta(minutes=int(d))
                tag.update({'TIME': datetime.isoformat(t).split('T')[1]})
            if value['value'].endswith('W'):
                t = datetime.now() + timedelta(days=int(d)*7)
                tag.update({'DATE': datetime.isoformat(t).split('T')[0]})
            else:
                t = datetime.now() + timedelta(days=int(d)*30)
                tag.update({'DATE': datetime.isoformat(t).split('T')[0]})
            
    if value['type'] == 'DATE':
        tag.update({'DATE': value['value']})
    if value['type'] == 'TIME':
        tag.update({'TIME': value['value'].split('T')[1]})
    return tag 


def compareDate(dates:list)->str:
    """compares dates and picks the earliest date
    
    Keyword arguments:
    dates -- list of available dates
    Return: the earliest date in the list
    """
    first_time = 2000000000000000000    #because the smallest is the goal
    final_date = ''
    today =  datetime.now().timestamp()

    try:
        for date in dates:
            if len(date) >8:
                timeStamp = datetime.strptime(date, "%Y-%m-%d").timestamp()
            if len(date) == 8:
                n_weeks = int(getFigure(date.split('-')[1]))
                year = datetime.now().year 
                ndate = datetime.isoformat(datetime(year, 1,1) + timedelta(days=n_weeks*7)).split('T')[0]
                timeStamp = datetime.strptime(ndate, "%Y-%m-%d").timestamp()
                date = ndate
            if len(date)< 8:
                date = date + '-01'
                timeStamp = datetime.strptime(date, "%Y-%m-%d").timestamp()

            if timeStamp < today:
                # add 7 days ,to get the next week
                date = datetime.strptime(date, '%Y-%m-%d') +timedelta(days=7)
                if timeStamp < first_time:
                  first_time = timeStamp
                  final_date = datetime.isoformat(date).split('T')[0]
                
    except:
        final_date = ''
    return final_date



def combineDateTime(vals:list)->str:
    """this combines all the valuables expected 
    
    Keyword arguments:)
    vals -- list of all the valuables in the email
    Return: the mvp
    """
    
    mvp = ''
    dates = []
    for ref in vals:
        if "DATE" in ref.keys():
            dates.append(ref["DATE"])
        if "TIME" in ref.keys():
            if len(ref['TIME']) >= len(mvp):
                mvp = ref['TIME']
    date = compareDate(dates)
    return date + ' T ' + mvp


def getDateTime(parse:list)-> str:
    tags = []
    for n,tag in enumerate(parse):
        tags.append(getValuables(tag))
        
    return combineDateTime(tags)


if __name__ == "__main__":

    email = input('What is the mail:  ')
    today = datetime.isoformat(datetime.now()).split('T')[0]
    email_sutime =sutime.parse(formatText(email), reference_date=today)

    print(f'The first date is: {getDateTime(email_sutime)}')