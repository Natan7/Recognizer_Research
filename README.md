# AVALIAÇÃO DE MODELOS DE REDES NEURAIS PARA TRANSCRIÇÃO DE ÁUDIOS EM PORTUGUES BRASILEIRO

## Resumo
Este trabalho de conclusão de curso apresenta uma análise da eficácia de modelos de redes neurais profundas na tarefa de transcrição de áudio em Português do Brasil. É possível identificar diferenças qualitativas em ferramentas de transcrição populares, o que aumenta a importância de um melhor entendimento sobre as vantagens e desvantagens (e.g. complexidade e custo computacional) que cada ferramenta apresenta, para que se possa escolher a mais adequada para cada contexto de uso. Muitas vezes as diferenças entre ferramentas para transcrição de áudio estão relacionadas à escassez de dados para um treinamento adequado, o que pode ocasionar erros de transcrição associados ao sotaque, entonação, tipo de locutor, entre outros. Neste contexto, propõe-se uma avaliação de desempenho entre ferramentas disponíveis para transcrição de voz em portugues brasileiro. As ferramentas utilizadas foram AssemblyAI, Whisper e Google Speech Recognition, disponíveis por meio de bibliotecas na linguagem de programação Python, de modo que todas foram analisadas em suas versões gratuitas. Com auxílio desses métodos, extrai-se a transcrição de uma base de dados de áudios obtida do site Agência Brasil, sendo feita uma checagem quanto à similaridade entre a transcrição publicada no site e a transcrição gerada pelas ferramentas propostas nesta pesquisa. Os métodos para determinação da similaridade utilizados foram distância Cosseno, Jaccard, SBERT e SpaCy. A partir dos resultados de similaridade obtidos, é possível concluir que a ferramenta AssemblyAI possui uma melhor acurácia no processo de transcrições de áudios em portugues brasileiro em relação às outras ferramentas testadas, embora possua restrições de tempo de uso em sua versão gratuita, diferentemente da ferramenta Whisper, que é totalmente gratuita e possui resultados muito próximos do AssemblyAI para o modelo Small. Vale destacar que o tempo de inferência para as transcrições mostrou ser menor para ferramenta Google Speech Recognition (cerca de 8 segundos), e muito superior a ferramenta do Whisper (cerca de 36 segundos), tendo em vista que o modelo é processado localmente, o que requer um hardware mais robusto para se obter tempos de resposta menores e maior acurácia. Os resultados obtidos podem orientar profissionais que necessitam transcrever conteúdos em português. Eles ajudam na seleção da ferramenta mais apropriada de acordo com as necessidades particulares de cada usuário, seja em contextos acadêmicos, jornalísticos ou empresariais. A ferramenta AssemblyAI apresentou  a maior acurácia para reconhecimento de fala das ferramentas avaliadas neste estudo, embora ela possua limitação de transcrições para sua versão gratuita. A melhor opção, sem limitação de transcrições, é a ferramenta Whisper que apresentou resultados muito próximos aos da AssemblyAI.

## Palavras chave
Transcrição de Áudios, Reconhecimento de Fala, Eficácia Transcrição, Ferramentas Transcrição.

### Ambiente de Execução
Para realização do experimento, foi utilizada uma máquina local com a seguinte configuração: 
  - Sistema: Linux Mint 21.3 Virginia - Cinnamon 6.0.4;
  - Placa Mãe: ASUSTeK modelo P8H61-M LE R2.0;
  - CPU: Intel Core i7-2700K (64 bits quad core model);
  - Placa Gráfica: AMD Radeon RX 570 Series (polaris10 LLVM 15.0.7 DRM 3.42 5.15.0-122-generic);
  - Memória Principal: 7.71 GiB;
  - Memoria Secundaria: 226.45 GiB;
  - Conexão a Internet: velocidade de  upload de 50 Mbs - velocidade de download de 100 Mbs.

Em adição, foi utilizada a linguagem de programação JavaScript  no processo de coleta de dados, por meio da biblioteca Puppeteer, além da linguagem de programação Python no tratamento, obtenção e análise dos resultados, por meio da utilização de diversas bibliotecas como assemblyai, speech_recognition, whisper, spacy, torch, Levenshtein, numpy, pandas e matplotlib. Todo o código utilizado neste trabalho, está disponível no repositório GitHub.

### Coleta de Dados - [web_scraping_ebc/](https://github.com/Natan7/Recognizer_Research/tree/main/web_scraping_ebc)
O primeiro passo para a realização deste trabalho foi encontrar uma base de dados vasta e disponível publicamente. O site Agência Brasil possui conteúdos reproduzidos por milhares de usuários e veículos impressos de todo o país e também do exterior,  com textos traduzidos para inglês e espanhol. Presente na web e nas redes sociais, a Agência Brasil cobre todos os eventos importantes do país, publicando diariamente dezenas de matérias. O outro motivo para escolha se dá pelo fato de que o site fornece uma quantidade razoável de matérias contendo a versão em áudio delas, essas, gravadas por pessoas de diferentes lugares do Brasil (expondo os respectivos sotaques) e diferentes gêneros.
Dessa forma, utilizou-se web scraping com auxílio linguagem de programação JavaScript que contém a biblioteca Puppeteer, que simula um ser humano acessando a internet e oferece opções para interação com a página, bem como a extração do código HTML da página.
Essa automatização do acesso para coleta das matérias textuais  e em áudio (no formato MP3) foi realizada a partir da página que lista as notícias do site Agência Brasil, pois ela oferece os links de acesso às matérias que são armazenadas em uma variável. Com essa lista de URLs, cada matéria foi acessada e realizou-se o download das versões em texto e áudio MP3 da matéria. 
Todo conteúdo coletado é armazenado em arquivos identificados com o identificador da matéria (contido na URL), de forma que eles, por sua vez, são armazenados numa pasta local.

### Processamento dos Dados - [algorithms_audio_recognizing/](https://github.com/Natan7/Recognizer_Research/tree/main/algorithms_audio_recognizing)
Observa-se que nas versões em áudio, as matérias também contém, ao final,  uma breve apresentação do locutor e de qual agência ele pertence, algo que não possui um padrão bem definido. Também observa-se que existem reportagens contendo entrevistas, músicas ou trechos que não são transcritos no corpo da matéria escrita. 
Para reduzir possíveis inconsistências entre a matéria e sua respectiva versão em áudio, considera-se apenas os primeiros 30 segundos de todas as matérias, reduzindo também a quantidade em horas de áudios analisados pelas ferramentas de transcrição.
O processo de corte no arquivo MP3 e no texto coletado é realizado utilizando a linguagem Python, e também a utilização de algumas bibliotecas como a própria Google Speech Recognition para identificar o ponto de corte da matéria em sua versão em texto.
Para retirar apenas os 30 segundos do texto original transcrito, realiza-se a transcrição dos últimos 5 segundos desse pedaço de 30 segundos, por meio da ferramenta Google Speech Recognition. A partir desses pedaços de textos transcritos, uma comparação é realizada entre o texto original e o pedaço obtido dos últimos 5 segundos, utilizando um algoritmo que implementa o conceito da Distância de Levinstein, para que o texto original seja truncado e armazenado em uma nova pasta que contém a versão em áudio truncada (30 segundos).
Todo esse processo gerou erros e acabou reduzindo parte da base de dados final tratada obtida já que algumas das transcrições geradas não possuíam 100% de acurácia, o que iria interferir no casamento entre termos buscados no texto original.

### Obtenção das Transcrições - [data/](https://github.com/Natan7/Recognizer_Research/tree/main/data)
Com os arquivos de áudio devidamente cortados em 30 segundos, realiza-se a transcrição do conteúdo por meio de bibliotecas das ferramentas AssemblyAI (com a biblioteca assemblyai), Whisper (com a biblioteca whisper) e Google Speech Recognition (com a biblioteca speech_recognition). O conteúdo transcrito é armazenado numa pasta contendo o nome da ferramenta, representado pelo nome análogo ao nome do arquivo original obtido no site Agência Brasil.  Além disso, o tempo para realização da transcrição também é armazenado, com o propósito  de análise futura.

## Requisitos

### Bibliotecas Python:
  - numpy
  - pandas
  - scikit-learn
  - transformers
  - tensorflow ou torch
  - spacy
  - matplotlib
  - Levenshtein
  - asyncio
  - whisper
  - assemblyai
  - speech_recognition

### Bibliotecas JavaScript:
  - puppeteer: "^23.1.0"
  - fs
  - https
