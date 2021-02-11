# GROUP 12 TECHNICAL ANALYSIS CODE
## ELEVEN : CENTRALE - ESSEC HACKATHON

In this project, we aim to generate business insights from the vast textual data resource that is 
the web. In order to successfully do so, we tap into our Web-scraping and Natural Language Processing
skills :)

Broadly, our technical analysis has the following pipline:
1. Web scraping
2. Data pre-processing
3. Natural Language Processing
    a. Topic Modelling using LDA
    b. Topic Extraction & Aspect Based Sentiment Analysis

In order to successfully implement our pipeline, you will need to do the following:
* Clone this repository onto your local machine
* Create a virtual environment following the requirements detailed in the REQUIREMENTS.txt file
* Web-scraping. Run the following commands in order:
    - python scraping_seatguru.py
    - python scraping_skytrax.py
* Data pre-processing. Run:
    - python merge_and_preprocess.py
* Topic Modelling using LDA. Run:
    - python topic_model.py
* Topic Modelling visualizations:
    - If you would like to visualize the outputs of our LDA model, simply open the 
    topic_modelling_visualizations.ipynb jupyter notebook
* Topic Extraction & Aspect Based Sentiment Analysis. Run the following commands in order:
    - python TP_Aspect_Extraction.py
    - (store the TEST dataset with the filename as "data/evaluation/text_data.txt")
    - python ABSA.py

And there you go! You've successfully extracted and gathered meaningful information from different textual 
web data sources! 

## IMPORTANT!
Don't forget to visualize the results of our 2 main models:
    - Topic Modelling: open the topic_modelling_visualizations.ipynb jupyter notebook 
    - Sentiment Analysis: open 'TEST_data_with_Topics_Sentiments.tsv' stored in the 'data/results/' folder. 
    Please note that for the sentiment values outputted, the mapping is as: 0 is neutral, 1 is negative, 2 is positive

Thank you for reading!