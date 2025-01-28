from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    """
    使用vader分析文本的情感倾向
    arags: text(str)
    return dict:包含情感得分的字典,例如,position,negivite,neu,compund(综合得分)
    """
    analyzer=SentimentIntensityAnalyzer()
    scores=analyzer.polarity_scores(text)
    return scores
    
