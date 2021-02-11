'''
Please note: This module is still in a developing stage. For the Completed Sentiment 
Analysis Model, please refer to the ASBA.py module
'''

import aspect_based_sentiment_analysis as absa
import pandas as pd
import numpy as np

def read(i):
    df = pd.read_csv('data/combined/reviews.csv')
    df = df.drop('Unnamed: 0', 1)
    df = df.sample(frac=0.5, random_state=i+10)
    return(df)


def infer_seat(nlp, x, aspect):
    text = (x)

    seat, space, legroom = nlp(text, aspects=aspect)
    if seat.sentiment == absa.Sentiment.positive:
        seat_score = 1
    elif seat.sentiment == absa.Sentiment.negative:
        seat_score = -1
    else:
        seat_score = 0
    
    if space.sentiment == absa.Sentiment.positive:
        space_score = 1
    elif space.sentiment == absa.Sentiment.negative:
        space_score = -1
    else:
        space_score = 0

    if legroom.sentiment == absa.Sentiment.positive:
        legroom_score = 1
    elif legroom.sentiment == absa.Sentiment.negative:
        legroom_score = -1
    else:
        legroom_score = 0
    
    return np.mean([seat_score, space_score, legroom_score])


def infer_staff(nlp, x, aspect):
    text = (x)

    staff, crew, attendants = nlp(text, aspects=aspect)

    if staff.sentiment == absa.Sentiment.positive:
        staff_score = 1
    elif staff.sentiment == absa.Sentiment.negative:
        staff_score = -1
    else:
        staff_score = 0
    
    if crew.sentiment == absa.Sentiment.positive:
        crew_score = 1
    elif crew.sentiment == absa.Sentiment.negative:
        crew_score = -1
    else:
        crew_score = 0
    
    if attendants.sentiment == absa.Sentiment.positive:
        attendants_score = 1
    elif attendants.sentiment == absa.Sentiment.negative:
        attendants_score = -1
    else:
        attendants_score = 0

    return np.mean([crew_score, staff_score, attendants_score])


def infer_food(nlp, x, aspect):
    text = (x)

    food, meal = nlp(text, aspects=aspect)
    if food.sentiment == absa.Sentiment.positive:
        food_score = 1
    elif food.sentiment == absa.Sentiment.negative:
        food_score = -1
    else:
        food_score = 0
    
    if meal.sentiment == absa.Sentiment.positive:
        meal_score = 1
    elif meal.sentiment == absa.Sentiment.negative:
        meal_score = -1
    else:
        meal_score = 0
    
    return np.mean([food_score, meal_score])


def infer_baggage(nlp, x, aspect):
    text = (x)
    print('here')

    baggage, check_in = nlp(text, aspects=aspect)
    if baggage.sentiment == absa.Sentiment.positive:
        baggage_score = 1
    elif baggage.sentiment == absa.Sentiment.negative:
        baggage_score = -1
    else:
        baggage_score = 0
    
    if check_in.sentiment == absa.Sentiment.positive:
        check_in_score = 1
    elif check_in.sentiment == absa.Sentiment.negative:
        check_in_score = -1
    else:
        check_in_score = 0
    
    return np.mean([baggage_score, check_in_score])


def infer_time(nlp, x, aspect):
    text = (x)

    time, cancelled, speed = nlp(text, aspects=aspect)
    if time.sentiment == absa.Sentiment.positive:
        time_score = 1
    elif time.sentiment == absa.Sentiment.negative:
        time_score = -1
    else:
        time_score = 0
    
    if cancelled.sentiment == absa.Sentiment.positive:
        cancelled_score = 1
    elif cancelled.sentiment == absa.Sentiment.negative:
        cancelled_score = -1
    else:
        cancelled_score = 0
    
    if speed.sentiment == absa.Sentiment.positive:
        speed_score = 1
    elif speed.sentiment == absa.Sentiment.negative:
        speed_score = -1
    else:
        speed_score = 0
    
    return np.mean([time_score, cancelled_score, speed_score])


def infer_value(nlp, x, aspect):
    text = (x)

    price, value = nlp(text, aspects=aspect)
    if price.sentiment == absa.Sentiment.positive:
        price_score = 1
    elif price.sentiment == absa.Sentiment.negative:
        price_score = -1
    else:
        price_score = 0
    
    if value.sentiment == absa.Sentiment.positive:
        value_score = 1
    elif value.sentiment == absa.Sentiment.negative:
        value_score = -1
    else:
        value_score = 0
    
    return np.mean([price_score, value_score])


def run(df,i):
    nlp = absa.load()

    df['Seat Sentiment'] = df['Comment'].apply(lambda x: infer_seat(nlp,x,['seat','space','legroom']))
    df['Staff Sentiment'] = df['Comment'].apply(lambda x: infer_staff(nlp,x,['staff','crew','attendants']))
    df['Food Sentiment'] = df['Comment'].apply(lambda x: infer_food(nlp,x,['food','meal']))
    df['Baggage Sentiment'] = df['Comment'].apply(lambda x: infer_baggage(nlp,x,['baggage','check in']))
    df['Time Sentiment'] = df['Comment'].apply(lambda x: infer_time(nlp,x,['time','cancelled','speed']))
    df['Value for Money Sentiment'] = df['Comment'].apply(lambda x: infer_value(nlp,x,['price','value']))

    df = df.drop(['Comment','Date','Class'], 1)
    df.to_csv('data/results/sentiments'+str(i+1)+'.csv')

if __name__ == '__main__':
    for i in range(1):
        df = read(i)
        run(df,i)