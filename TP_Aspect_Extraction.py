!pip install sentence_transformers
import pandas as pd
import numpy as np
from sentence_transformers import CrossEncoder
from spacy.lang.en import English # updated


def read_dirty_test_file(path):
  with open(path, 'r') as file1:
    lines = file1.readlines()
  clean_lines = [line.strip('\n') for line in lines]
  df = pd.DataFrame({clean_lines[0]: clean_lines[1:]})

  return df


def split_text_to_sentences(raw_text):
  nlp = English()
  nlp.max_length = 12306482 
  nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
  doc = nlp(raw_text)
  sentences = [sent.string.strip() for sent in doc.sents]
  return sentences

# Topic modelling

aspects= {
    "food": "food meal dinner drink dish snacks",
    "staff": "crew hostess onboarding service staff",
    "seat": "seat space knees comfort leg",
    "entertainment": "screen movie display video music",
    "luggage": "bag suitcase handbag",
}

def topic_modelling(df, model):
    for aspect in aspects.keys():
      df[aspect] = df.full_message.apply(lambda x: score_topic_sentence(x, aspect=aspect))
      
    df["best_aspect"] = "None"
    df["max_score"] = df[aspects.keys()].max(axis=1)
    for aspect in aspects.keys():
      df.loc[(df[aspect] == df["max_score"]) & (df["max_score"] > 0.1), "best_aspect"] = aspect
    df = df.drop(columns= "max_score")
    return df

def score_topic_sentence(sentence, aspect="food"):
  aspect_description = aspects[aspect]
  score = model.predict((sentence, aspect_description))
  return score


if __name__ == "__main__":
    path = "/content/drive/MyDrive/Hackathon_eleven/datasets/"
    file_name = "text_data.txt"
    df = read_dirty_test_file(path + file_name)
    
    # Scoring Reviews against each topic
    model = CrossEncoder('cross-encoder/stsb-roberta-base')
    df = topic_modelling(df, model)

    df.to_csv(path + "TEST_data_with_Topics.csv")


