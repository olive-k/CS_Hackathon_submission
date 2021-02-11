""" This script writes the reviews of all the airlines on skytrax to a csv file """

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# This function extracts reviews (both content and attributes) from one page
def get_reviews(soup):
    """
    input: a review page in bs4 type
    output: a DataFrame of the review content and attributes as columns for the input page
    """
    # this function extracts text content
    def get_content_list():
        content = soup.find_all(class_="text_content")
        content_list = [i.get_text() for i in content]
        # get the comment in the right format
        content_list = [i.replace("✅ Trip Verified |","") for i in content_list]
        content_list = [i.replace("Not Verified |","") for i in content_list]
        return content_list

    # this function extracts other attributes such as seat type and other ratings
    def get_attr_df():
        reviews = soup.find_all(class_="body")
        reviews_list = []
        for review in reviews:
            review_dict = {}
            table = review.find(class_="review-stats").find(class_="review-ratings")
            stars_dict = {}
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                # get the ratings
                stars = list(cells[1].find_all(class_='star fill'))
                if len(stars)>0:
                    stars = len(stars)

                for i in list(cells[0]):
                    stars_dict[i] = stars
                    if type(stars_dict[i]) is int:
                        review_dict[i] = stars_dict[i]
                    else:
                        for j in list(cells[1]):
                            review_dict[i] = j

                review_dict.update({"id": review["id"]})
            reviews_list.append(review_dict)
            reviews_df = pd.DataFrame(reviews_list).set_index('id')
        return reviews_df

    df = get_attr_df()
    df['content']=get_content_list()
    return df

# this function iterates through all the pages of all the airlines if the number of review pages for one airline is more than 10
def airline_reviews(airlines):
    """
    input: a list of airline names
    output: a DataFrame of all the airline reviews we are interested in
    """
    airlines_list = []
    headers = {'Accept-Language': 'en-US,en;q=0.8'}
    for airline in airlines:
        front_page = requests.get("https://www.airlinequality.com/airline-reviews/{}/".format(airline), headers=headers)
        soup_airline = BeautifulSoup(front_page.content, 'html.parser')
        try:
            nb_pages = soup_airline.find_all('a', href=re.compile('^/airline-reviews/{}/page/'.format(airline)))[-2]
            nb_pages = str(nb_pages)
            if nb_pages[-7].isnumeric():
                nb_pages = int(nb_pages[-7:-4])
            else:
                nb_pages = int(nb_pages[-6:-4])

                review_list = []
                for page in range(0,nb_pages):

                    airline_page = requests.get("https://www.airlinequality.com/airline-reviews/{0}/page/{1}/".format(airline, page), headers=headers)
                    soup = BeautifulSoup(airline_page.content, 'html.parser')
                    df = get_reviews(soup)
                    review_list.append(df)

            df_airline = pd.concat(review_list, axis=0, sort=True)
            df_airline['airline'] = airline
            airlines_list.append(df_airline)
            print('done for {}'.format(airline))
        except:
            pass

    df_airlines = pd.concat(airlines_list, axis=0, sort=True)
    return df_airlines


if __name__ == '__main__':
    # the page where all the airlines appear
    a_z_page = requests.get("https://www.airlinequality.com/review-pages/a-z-airline-reviews/")
    airline_names = BeautifulSoup(a_z_page.content, 'html.parser')
    # find the airline names in the right format
    names = airline_names.find_all('a', href=re.compile('^/airline-reviews/'))

    # get the names of all the airlines
    all_airlines = []
    for name in list(names):
        name = re.search('s/(.*)"', str(name)).group(1)
        all_airlines.append(name)
    all_airlines = all_airlines[:519] # there are 519 airlines in total

    # get the dataset of all the airlines
    all_df = airline_reviews(all_airlines)
    all_df.to_csv('data/skytrax/skytrax_all.csv')
