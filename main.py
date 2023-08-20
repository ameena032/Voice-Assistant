import openai
import pyttsx3
import speech_recognition as sr
import random



#set OpenAI key
openai.api_key="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"
model_id='gpt-3.5-turbo'

#initialize  the text-to-speech engine
engine = pyttsx3.init()

#change speech rate
engine.setProperty('rate', 180)

#get the available voice
voices = engine.getProperty('voices')

#choose a voice based on the voice id
engine.setProperty('voice', voices[1].id)

#counter just for interacting purposes
interaction_counter = 0


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")
            #print('Skipping unknown error')


def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
     )

    api_usage = response['usage']
    print('Total token consumed:{0}'.format(api_usage['total_tokens']))
    conversation.append({'role':response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


#starting conversation
conversation =[]
conversation.append({'role':'user', 'content':'Please ,Act like Friday AI from Iron Man, make a 1 sentence phrase introducing yourself without saying something that sounds like this chat its already'})
conversation= ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(),conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())


def activate_assistant():
     starting_chat_phrases = ["Yes sir, how may I assist you?",
                            "Yes, What can I do for you?",
                            "How can I help you, sir?",
                            "Friday here, how can I help you today?",
                            "Yes, what can I do for you today?",
                            "yes sir, what's pn your mind?",
                            "Friday ready to assist, what can I do for you?",
                            "At your command, sir. How may I help you today?",
                            "Yes, sir.How may I be of assistant to you right now?",
                            "yes boss, I'm here to help.What do you need from me?",
                            "Yes, I'm listening.What can I do for you,sir?",
                            "How can I assist you today,sir?",
                            "yes,sir.How can I make your day easier?",
                            "Yes boss, what's the plan?",
                            "yes, What's on your mind,sir?"]
     continued_chat_phrases = ["yes", "yes,sir", "yes,boss", "I'm all ears"]
     random_chat = ""
     if(interaction_counter == 1):
         random_chat = random.choice(starting_chat_phrases)
     else:
         random_chat= random.choice(continued_chat_phrases)
     return random_chat

# explicit function to take input commands
# and recognize them
def takeCommandHindi():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        # seconds of non-speaking audio before
        # a phrase is considered complete
        print('Listening')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='hi-In')

            # for listening the command in indian english
            print("the query is printed='", Query, "'")

        # handling the exception, so that assistant can
        # ask for telling again the command
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
        return Query


# Driver Code

# call the function
takeCommandHindi()

from gtts import gTTS
from gtts import gTTS
import os

def speak_in_hindi(text):
    tts = gTTS(text, lang='hi')
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows. Use appropriate command for other platforms

text_to_speak = "नमस्ते, मैं आपकी सहायता कैसे कर सकता हूँ?"
speak_in_hindi(text_to_speak)

# import required module
import speech_recognition as sr



def append_to_log(text):
    with open("chat_log.txt","a") as f:
        f.write(text + "\n")


while True:
    #wait for user to say "friday"
    print("Say'Friday' to start....")
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "friday" in transcription.lower():
                interaction_counter += 1

                #record audio
                filename= "input.wav"

                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                        # transcribe audio to text
                text = transcribe_audio_to_text(filename)

                if text:
                    print(f"you said:{text}")
                    append_to_log(f"you: {text}\n")

                    #generate response using chatGPT
                    print(f"Friday says: {conversation}")

                    prompt = text

                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGPT_conversation(conversation)

                    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content']))

                    append_to_log(f"Friday:{conversation[-1]['content'].strip()}\n")


                    #read response using text-to-speech
                    speak_text(conversation[-1]['content'].strip())
        except Exception as e:
            continue
            #print("An error occured:{}".format(e))
