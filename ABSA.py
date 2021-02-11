!pip install aspect_based_sentiment_analysis
import pandas as pd
import numpy as np
import aspect_based_sentiment_analysis as absa


# ABSA

def extract_sentiment(bundled):
  text, aspect = bundled
  pred = nlp(text, aspects=[aspect])
  return pred.subtasks[aspect].sentiment.value

def preprocess_for_ABSA(df):
  df["text_aspect"] = list(zip(df.full_message, df.best_aspect))
  return df

aspects= {
    "food": "food meal dinner drink dish snacks",
    "staff": "crew hostess onboarding service staff",
    "seat": "seat space knees comfort leg",
    "entertainment": "screen movie display video music",
    "luggage": "bag suitcase handbag",
}


if __name__ == "__main__":
    path = "/content/drive/MyDrive/Hackathon_eleven/datasets/"
    file_name = "TEST_data_with_Topics.csv"
    df = pd.read_csv( path + file_name)

    # Applying ABSA
    nlp = absa.load(name = 'absa/classifier-rest-0.2')
    df = preprocess_for_ABSA(df)
    df["sentiment"] = df.text_aspect.apply(extract_sentiment)

    # reorder for output
    df["predicted_aspect"] = df["best_aspect"].copy()
    df = df[["text_aspect", "predicted_aspect", "sentiment",
             "food", "staff", "seat", "entertainment", "luggage"]].copy()
    print(df)
    df.to_csv(path + "TEST_data_with_Topics_Sentiments.csv")
