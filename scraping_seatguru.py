########################################################################################
# SEAT GURU
########################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


def scrape():
    homepage_url = "https://www.seatguru.com/browseairlines/browseairlines.php"
    homepage=requests.get(homepage_url)
    soup = BeautifulSoup(homepage.content, 'html.parser')

    airline_links = soup.find_all(class_ = "browseAirlines")[0].find_all("a")

    homepage_url = "https://www.seatguru.com"

    airlines_colnames = ["Name","Overview"]

    airlines_dataframe = pd.DataFrame(index = np.arange(1,176),columns = airlines_colnames)
    airlines_dataframe = airlines_dataframe.fillna(0)

    flights_colnames = ['Name','Airline','Seats','ReviewIDs']
    # 'Seats' is a list like ['138 Economy', '41 Business']
    # 'ReviewIDs' is a list of all the review IDs for the plane (List of integers)
    flights_dataframe = pd.DataFrame(columns = flights_colnames)
    flights_df_name = []
    flights_df_airline = []
    flights_df_seats = []
    flights_df_reviewIDs = []
    review_id_counter = 0
    reviews_colnames = ['ID','Comment','Date','Class']
    reviews_dataframe = pd.DataFrame(columns = reviews_colnames)
    reviews_df_id = []
    reviews_df_comment = []
    reviews_df_date = []
    reviews_df_class = []

    for i,airline_link in enumerate(airline_links):
        airline_page = requests.get(homepage_url + airline_link['href'])
        airline_soup = BeautifulSoup(airline_page.content, 'html.parser')
        airlines_dataframe.iloc[i,0] = airline_link.getText()
        airlines_dataframe.iloc[i,1] = airline_soup.find_all(class_ = "overview")[0].find('p').getText()
        aircrafts = airline_soup.find_all(class_ = "aircraft_seats")
        for aircraft in aircrafts:
            flights_df_name.append(aircraft.find('a').getText())
            flights_df_airline.append(airline_link.getText())
            seats = []
            aircraft_review_ids = []
            seats_list = aircraft.find_all(class_ = "seat_class")
            for seat in seats_list:
                seats.append(seat.getText())
            flights_df_seats.append(seats)
            aircraft_link = aircraft.find('a')
            aircraft_page = requests.get(homepage_url + aircraft_link['href'])
            aircraft_soup = BeautifulSoup(aircraft_page.content, 'html.parser')
            comment_box = aircraft_soup.find_all(class_ = "comment-box")
            if comment_box:
                comments = comment_box[0].find_all(class_ = "comment")
                comments_metadata = aircraft_soup.find_all(class_ = "comment-box")[0].find_all(class_ = "submitted")
                for j,comment in enumerate(comments):
                    review_id_counter += 1
                    reviews_df_comment.append(comment.getText().strip())
                    reviews_df_id.append(review_id_counter)
                    aircraft_review_ids.append(review_id_counter)
                    text = comments_metadata[j].find(class_ = 'date').getText()
                    date = re.search(r'\d{4}/\d{2}/\d{2}', text).group()
                    reviews_df_date.append(date)
                    if (len(text.strip().split("for Seat",1)))>1:
                        seat_no = text.strip().split("for Seat",1)[1].strip().upper()
                        seat_phrase = "Seat "+seat_no[:-1] + " " + seat_no[-1:]
                        table = aircraft_soup.find_all('table',class_ = "standard")[0]
                        flag = False
                        for row in table.find_all("tr"): 
                            cells = row.find_all("td")
                            if cells:
                                if seat_phrase in cells[5].getText():
                                    seat_class = cells[5].getText().split("Class",1)[0]
                                    if ('Economy' in seat_class):
                                        reviews_df_class.append('Economy')
                                        flag = True
                                        break
                                    elif ('Premium' in seat_class):
                                        reviews_df_class.append('Premium')
                                        flag = True
                                        break
                                    elif ('Business' in seat_class):
                                        reviews_df_class.append('Business')
                                        flag = True
                                        break
                                    else:
                                        # Change this to NA!!
                                        reviews_df_class.append(0)
                                        flag = True
                                        break
                        if (flag == False):
                            reviews_df_class.append(0)
                    else:
                        # Change this to NA!!
                        reviews_df_class.append(0)
                flights_df_reviewIDs.append(aircraft_review_ids)
            else:
                reviews_df_comment.append(0)
                flights_df_reviewIDs.append(0)
                reviews_df_id.append(0)
                reviews_df_date.append(0)
                reviews_df_class.append(0)

    #airlines_dataframe.to_csv("airlines.csv")

    flights_dataframe['Name'] = flights_df_name
    flights_dataframe['Airline'] = flights_df_airline
    flights_dataframe['Seats'] = flights_df_seats
    flights_dataframe['ReviewIDs'] = flights_df_reviewIDs
    #flights_dataframe.to_csv('flights.csv')

    reviews_dataframe['ID'] = reviews_df_id
    reviews_dataframe['Comment'] = reviews_df_comment
    reviews_dataframe['Date'] = reviews_df_date
    reviews_dataframe['Class'] = reviews_df_class

    reviews_dataframe = reviews_dataframe[reviews_dataframe.ID != 0]

    #reviews_dataframe.to_csv('reviews.csv')

if __name__ == '__main__':
    scrape()