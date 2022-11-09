from gtts import gTTS
import os 

txt = "Hello World, just trying out text to speech frameworks."

language = 'en'

myobj = gTTS(text=txt, lang=language, slow=False)
  
myobj.save("welcome.mp3")
os.system("mpg321 welcome.mp3")