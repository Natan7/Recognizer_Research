def output(file_path, file_name, generated_text):
    try:
        with open(file_path + file_name,'w') as f:
            f.write('{}\n'.format(generated_text))
        print("Transcrição gerada: ")
        print(file_path + file_name)
        print()
    except:
        print("Ocoreu um erro ao salvar o texto")