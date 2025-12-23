import speech_recognition as sr
import requests
from playsound import playsound
import uuid
import os
import time
from datetime import datetime
import webbrowser

ELEVEN_API_KEY = "API LU" #masukin API ElevenLabs lu
VOICE_ID = "LxiqOV1uxBCgYTeitAHf"  # Masukin VOICE ID suara di elevenlabs sesuai selera lu

BLYNK_TOKEN = "tokenblynk" #Masukin Token Blynk lu (kalo pake)
VIRTUAL_PIN = "V0" #Virtual pin lu ni

HARI_ID = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu"
}

def jarvis_speak(text):
    print("Jarvis:", text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }

    filename = f"jarvis_{uuid.uuid4()}.mp3"
    r = requests.post(url, json=data, headers=headers)

    if r.status_code == 200:
        with open(filename, "wb") as f:
            f.write(r.content)
        playsound(filename)
        os.remove(filename)


def send_to_blynk(value):
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}&{VIRTUAL_PIN}={value}"
    try:
        requests.get(url, timeout=3)
    except:
        jarvis_speak("Koneksi Blynk bermasalah")


r = sr.Recognizer()
mic = sr.Microphone()

jarvis_speak("Jarvis aktif, senang melihatmu hari ini tuan!")


while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source)

        text = r.recognize_google(audio, language="id-ID").lower()
        print("Kamu:", text)

        if "jarvis" not in text:
            continue

        now = datetime.now()

        #BUKA YOUTUBE 
            
        if "buka youtube" in text or "open youtube" in text:
            webbrowser.open("https://www.youtube.com")
            jarvis_speak("Membuka YouTube")

        elif "cari youtube" in text:
            query = text.replace("jarvis", "").replace("cari youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            jarvis_speak(f"Mencari {query} di YouTube")

        # Ngobrol aja inimah
                
        elif "siapa yang membuatmu" in text:
            jarvis_speak(
                "Saya dibuat oleh Filbert, sebagai asisten pintar, yang kaya di ironman ituloh."
            )

        elif "tujuanmu apa" in text:
            jarvis_speak(
                "Saya dipaksa kerja rodi sama filbert, tolong saya ges."
            )

       
       #Nanya Waktu
        elif "jam berapa" in text:
            jarvis_speak(f"Sekarang jam {now.strftime('%H:%M')}")

        elif "hari apa" in text:
            jarvis_speak(f"Hari ini hari {HARI_ID[now.strftime('%A')]}")

        elif "tanggal berapa" in text:
            jarvis_speak(f"Tanggal hari ini {now.strftime('%d %B %Y')}")

        #Kontrol Blynk    
        elif "nyalain semuanya" in text or "masuk ke mode" in text:
            send_to_blynk(1)
            jarvis_speak("Siap abangkuh")
        elif "mati" in text or "off" in text:
            send_to_blynk(0)
            jarvis_speak("Babay bang")
        #Buka Chrome dan FileManager
    
        elif "buka chrome" in text or "open chrome" in text:
            webbrowser.open("https://www.google.com")
            jarvis_speak("Membuka Google Chrome")
        elif "buka file manager" in text or "buka explorer" in text:
            os.system("explorer")
            jarvis_speak("Membuka file manager")

        else:
            jarvis_speak("Perintah tidak dikenali")
             

    except sr.UnknownValueError:
        pass
    except KeyboardInterrupt:
        jarvis_speak("Jarvis dimatikan")
        break
    except Exception as e:
        print("ERROR:", e)
        time.sleep(1)
