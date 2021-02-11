import pandas as pd


def my_split(x):
    if pd.notnull(x):
        return x.split()[0]
    else:
        return '0'

def format_date(x):
    if pd.notnull(x):
        month, year = x.split()
        month_name_int_map = {
            'January' : '01',
            'February' : '02',
            'March' : '03',
            'April' : '04',
            'May' : '05',
            'June' : '06',
            'July' : '07',
            'August' : '08',
            'September' : '09',
            'October' : '10',
            'November' : '11',
            'December' : '12'
        }
        return year+'/'+month_name_int_map[month]+'/'+"1"
    else:
        return x


def seatguru_airlines_format(x,flights_df):
    for ind, i in enumerate(flights_df['ReviewIDs']):
        if i == 0:
            continue
        else:
            for j in i:
                if j == x:
                    return flights_df.loc[ind,'Airline']
    return '0'


def seatguru_aircraft_format(x,flights_df):
    for ind, i in enumerate(flights_df['ReviewIDs']):
        if i == 0:
            continue
        else:
            for j in i:
                if j == x:
                    return flights_df.loc[ind,'Aircraft']
    return '0'


def skytrax_airlines_format(x):
    if pd.notnull(x):
        tokens = x.split('-')
        result = []
        for token in tokens:
            result.append(token.capitalize())
        return " ".join(result)
    else:
        return '0'


def skytrax_rate_format(x):
    if pd.notnull(x):
        return x
    else:
        return -1


def skytrax_traveller_type_format(x):
    if pd.notnull(x):
        return x
    else:
        return "0"


def skytrax_origin_format(x):
    if pd.notnull(x):
        if "-" in x:
            return x.split("-")[0].strip().split(" ")[0].strip()
        elif "to" in x:
            return x.split("to")[0].strip().split(" ")[0].strip()
        else:
            return "0"
    else:
        return "0"


def skytrax_destination_format(x):
    if pd.notnull(x):
        if "-" in x:
            return x.split("-")[1].strip().split(" ")[0].strip()
        elif "to" in x:
            return x.split("to")[1].strip().split(" ")[0].strip()
        else:
            return "0"
    else:
        return "0"


def merge_reviews():
    skytrax = pd.read_csv("data/skytrax/skytrax_all.csv")
    skytrax = skytrax.drop('Unnamed: 0', 1)
    #print(skytrax.head())
    #print(skytrax.columns)
    #print(skytrax.iloc[0])
    #print(len(skytrax))

    
    seatguru = pd.read_csv("data/seatguru/reviews.csv")
    seatguru = seatguru.drop('Unnamed: 0', 1)
    #print(seatguru.tail())

    seatguru_flights = pd.read_csv("data/seatguru/flights.csv")
    seatguru_flights = seatguru_flights.drop('Unnamed: 0', 1)
    #print(seatguru_flights.tail())

    seatguru['Airlines'] = seatguru['ID'].apply(lambda x: seatguru_airlines_format(x,seatguru_flights))
    seatguru['Aircraft'] = seatguru['ID'].apply(lambda x: seatguru_aircraft_format(x,seatguru_flights))
    seatguru.loc[:,'SeatRating'] = -1
    seatguru.loc[:,'StaffRating'] = -1
    seatguru.loc[:,'FoodBevRating'] = -1
    seatguru.loc[:,'GroundServiceRating'] = -1
    seatguru.loc[:,'EntertainmentRating'] = -1
    seatguru.loc[:,'ValueRating'] = -1
    seatguru.loc[:,'WiFiRating'] = -1
    seatguru.loc[:,'Recommended'] = -1
    seatguru.loc[:,'Origin'] = "0"
    seatguru.loc[:,'Destination'] = "0"
    seatguru.loc[:,'TravellerType'] = "0"

    #print(seatguru.tail())

    skytrax_review_id = [i for i in range(len(seatguru)+1,len(seatguru)+1+len(skytrax))]
    colnames = ["ID","Comment","Date","Class"]
    new_skytrax = pd.DataFrame(columns = colnames)
    new_skytrax['Comment'] = skytrax['content']
    new_skytrax['ID'] = skytrax_review_id
    new_skytrax['Class'] = skytrax['Seat Type'].apply(my_split)
    new_skytrax['Date'] = skytrax['Date Flown'].apply(format_date)
    new_skytrax['Aircraft'] = skytrax['Aircraft']
    new_skytrax['Airlines'] = skytrax['airline'].apply(skytrax_airlines_format)
    new_skytrax['SeatRating'] = skytrax['Seat Comfort'].apply(skytrax_rate_format)
    new_skytrax['StaffRating'] = skytrax['Cabin Staff Service'].apply(skytrax_rate_format)
    new_skytrax['FoodBevRating'] = skytrax['Food & Beverages'].apply(skytrax_rate_format)
    new_skytrax['GroundServiceRating'] = skytrax['Ground Service'].apply(skytrax_rate_format)
    new_skytrax['EntertainmentRating'] = skytrax['Inflight Entertainment'].apply(skytrax_rate_format)
    new_skytrax['ValueRating'] = skytrax['Value For Money'].apply(skytrax_rate_format)
    new_skytrax['WiFiRating'] = skytrax['Wifi & Connectivity'].apply(skytrax_rate_format)
    new_skytrax['Recommended'] = skytrax['Recommended'].apply(skytrax_rate_format)
    new_skytrax['TravellerType'] = skytrax['Type Of Traveller'].apply(skytrax_traveller_type_format)
    new_skytrax['Origin'] = skytrax['Route'].apply(skytrax_origin_format)
    new_skytrax['Destination'] = skytrax['Route'].apply(skytrax_destination_format)
    
    df = pd.concat([seatguru, new_skytrax], ignore_index = True)
    
    print(df.iloc[17340])
    
    df.to_csv('data/combined/reviews_all.csv')


if __name__ == '__main__':
    merge_reviews()