import whisper

modelo = whisper.load_model("small")
resposta = modelo.transcribe("../Web_Scraping_EBC/materias_coletadas/19-04-24_-_gabriel_brum_-_passaportes_ra_ps.mp3")

print(resposta["text"])