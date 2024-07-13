# importing the necessary libraries
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as YTA
from dotenv import load_dotenv

# load all the environment variables
load_dotenv()

# getting the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt for generating the youtube transcript summary 
prompt="""You are an erpert Yotube video summarizer. You will be taking the transcript 
text as input and summarizing the entire video and providing the important summary in 
paragraph within 300 words. Please provide the summary of the text given here:  """

# fetching the transcript data from youtube videos
def extract_transcript(yt_video_url):
    try:
        video_id=yt_video_url.split("v=")[1]
        transcripted_txt=YTA.get_transcript(video_id)
        
        # converting the list 'transcripted_txt' to string 'transcript'
        transcript=""
        for i in transcripted_txt: 
            transcript+=" "+ i["text"]
        return transcript
   
    except Exception as e:
        raise e
    
# generating the summary of the youtube transcript
def generate_summary(transcripted_text,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt + transcripted_text)
    return response.text

# creating the STREAMLIT app
st.title("YouTube Transcript to Short Notes")
st.text("[Works only for public youtube videos]")
yt_link=st.text_input("Enter the YouTube video link:")

if yt_link:
    video_id=yt_link.split('v=')[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    
if st.button("Get Notes"):
    yt_transcript=extract_transcript(yt_link)
    if yt_transcript:
        summary=generate_summary(yt_transcript,prompt)
        st.markdown("## Detailed Notes")
        st.write(summary)