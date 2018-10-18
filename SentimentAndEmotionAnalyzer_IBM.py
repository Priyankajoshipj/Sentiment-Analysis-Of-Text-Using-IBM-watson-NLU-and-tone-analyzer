#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

def main(dict):

    # coding: utf-8
    import json
    import os
    from watson_developer_cloud import NaturalLanguageUnderstandingV1
    from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
    from watson_developer_cloud import ToneAnalyzerV3
    
    
    # Using NLU to check sentiment score
    ReturnString={}
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2017-02-27',
        username='********-****-****-****-************',
        password='************')
        
    #Using Tone Analyzer to Check Emotion and Writing tone
    
    tone_analyzer = ToneAnalyzerV3(
            username='********-****-****-****-************',
            password='************',
            version='2016-02-11')
    
    if( "text" in dict):
        #text="I do not understand what you are telling me. Earlier you said that I could fix the problem by doing one thing, now you’re saying that I have to do something else? Am I ever going to be able to get my data back? Do you actually know what you’re talking about!? Let me talk to your supervisor or someone who UNDERSTANDS HOW FRUSTRATING THIS IS AND HOW IMPORTANT MY INFORMATION THAT I LOST WAS. This needs to be fixed NOW."
        text=dict['text']
        print(text)
        response = natural_language_understanding.analyze(
                    text=text,
                    features=Features(entities=EntitiesOptions(sentiment=True,limit=3), keywords=KeywordsOptions(sentiment=True,limit=3)))
        print(response)
        
        score=0
        for entity in response["entities"]:
            sentiment=entity["sentiment"]["score"]
            score=score+sentiment
        for keywords in response["keywords"]:
            sent=keywords["sentiment"]["score"]
            score=score+sent
        
        count=len(response["entities"])+len(response["keywords"])
        avgSent=score/count
        #print("Sentiment score for the email is: ",avgSent)
        
        
        
        #FindLabel
        if (avgSent<0):
            label="Negative"
            avgSent*=-1
        elif(avgSent>0):
            label="Positive"
        else:
            label="Neutral"
        #print("Sentiment seems to be, ",label)
        ReturnString['Sentiment_label']=label
        ReturnString['Sentiment_score']=round(float(avgSent),2)
        
        
   
        content_type = 'application/json'
        tone = tone_analyzer.tone({"text": text},content_type)
        
        doc_emotions={}
        doc_writing={}
        doc_social={}
        print(tone)
        for tone_category in tone["document_tone"]["tone_categories"]:
                category=tone_category["category_id"]
                #print(category)
                if(category=='emotion_tone' or category=='writing_tone' or category=='social_tone'):
                    for tones in tone_category['tones']:
                        score=round(float(tones['score']),2)
                        tone_name=tones['tone_name']
                        if(score>=0.45):
                            if(category=='emotion_tone'):
                                doc_emotions[tone_name]=score
                            elif(category=='writing_tone'):
                                doc_writing[tone_name]=score
                            else:
                                doc_social[tone_name]=score
        
        if(doc_emotions!= {} ):
            ReturnString['emotions']=doc_emotions
        if(doc_writing!= {} ):
            ReturnString['writing_tone']=doc_writing
        if(doc_social!= {} ):
            ReturnString['social_tone']=doc_social
    else:
        ReturnString['text']= {"Custom Error":"Input might not be in required JSON format, verify and retry!"}
    return ReturnString 

