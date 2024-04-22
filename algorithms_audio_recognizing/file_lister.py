import os

def mp3_files(path_file):
    mp3_files = []
    for file_name in os.listdir(path_file):
        path = os.path.join(path_file, file_name)
        if os.path.isfile(path):
            if path.lower().endswith('.mp3'):
                mp3_files.append(path)
    return mp3_files