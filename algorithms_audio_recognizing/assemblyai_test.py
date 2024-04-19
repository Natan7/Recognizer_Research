import assemblyai as aai

aai.settings.api_key = "123678cf5dbb45e5b32a57a05c8c2ff0"

config = {
    'language_code': 'pt',
}
transcriber = aai.Transcriber(config=aai.TranscriptionConfig(language_code='pt'))

#transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
#transcript = transcriber.transcribe("./simpsons_test_en_cut.mp3")

 

transcript = transcriber.transcribe("../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.mp3")

print(transcript.text)