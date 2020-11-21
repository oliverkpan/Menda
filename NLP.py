import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analysis(sentiment_text):

    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)

    neg = score['neg']

    pos = score['pos']

    print(score)

    if neg > pos:
        print("Negative :(")
    elif pos > neg:
        print("Positive :)")
    else:
        print("Neutral")
        

sentiment_analysis("today was the worst day ever. im going to cry when i get home")