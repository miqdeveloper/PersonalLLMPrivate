from langchain.document_loaders import PlaywrightURLLoader
from langchain.llms import Ollama
from langchain_community.chat_models import ChatOllama
import requests
import json, re
from pprint import pprint as pp
from pypdf import PdfReader

context_convers = []

urls_test = [
    "https://docs.djangoproject.com/en/5.0/topics/async/#asgiref.sync.sync_to_async"]

chunks = []

file = "beggin.txt"

def gravar_array_arquivo(array, arquivo):
    
    
    """
    Grava uma linha que é um array em um arquivo de texto.

    Args:
        array: O array a ser gravado.
        arquivo: O arquivo de texto em que o array será gravado.
    """

    with open(arquivo, "w") as f:
        f.write("[" + ",".join(map(str, array)) + "]\n")
def ler_array_arquivo(arquivo):
  """
  Lê um arquivo de texto e retorna o array com as "[]".

  Args:
    arquivo: O arquivo de texto a ser lido.

  Returns:
    O array lido.
  """

  with open(arquivo, "r") as f:
    linhas = f.readlines()

  array = []
  for linha in linhas:
    array.append(linha.split(","))

    return array[0][0:]

def break_text(text, chunk_size=4048):
    """
    Quebra o texto em partes menores, com base no tamanho do pedaço.

    Args:
      text: O texto a ser quebrado.
      chunk_size: O tamanho do pedaço.

    Returns:
      Uma lista de partes do texto.
    """

    
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start = end
    return chunks

def summarize_link(url):
    """
    Resumir o conteúdo do link.

    Args:
      url: O link do conteúdo a ser resumido.

    Returns:
      Um resumo do conteúdo.
    """

    # Carrega o conteúdo do link.
    # se for a rimeira vez execute "playwright install"
    urlHtml = PlaywrightURLLoader(url, remove_selectors=["header", "footer"])
    urlHtml = urlHtml.load()
    urlHtml = urlHtml[0]
    prom_test = urlHtml.page_content

    # Quebra o texto em partes menores.
    text_chunks = break_text(prom_test)
    print(len(text_chunks))
    # # Envia cada parte do texto para o modelo de geração de texto.
    # summaries = []
    for text_chunk in text_chunks:
        print(text_chunk)
        data = {
            "model": "mistral:v0.2",
            "prompt": text_chunk,
            "context": context_convers,
            "options": {
                "temperature": 0.9,
                "num_predict": -1,
                "repeat_penalty": 1.5,
                "mirostat_eta": 0.9,
                "mirostat_tau": 5.0,
                "mirostat": 0,
                "top_k": 50,
                "top_p": 0.90,
                "tfs_z": 2.0,
                # "num_ctx": 324,
            }
        }
        response = requests.post(url, data=json.dumps(data))
    #     if response.status_code == 200:
    #         resp = response.text
    #         list_words = []
    #         linhas = resp.split("\n")

    #         sl = linhas[l:]
    #         dt_context = json.loads(sl[0])
    #         for i in dt_context["context"]:
    #             context_convers.append(i)

    #         a = len(linhas)-2

    #         for x in range(a):
    #             j = json.loads(linhas[x])
    #             list_words.append(j['response'])

    #         text = ''.join(list_words)
    # #          print("context: ", context_convers)
    #         print("\n\n", text)

def middleware(impt):

    url = " http://localhost:11434/api/generate"
    # headers = {'Content-Type': 'application/json'}
    list_words = []

    # urlHtml = SeleniumURLLoader(urls_test)
    # urlHtml = urlHtml.load()
    # urlHtml = urlHtml[0]

    # prom_test = urlHtml.page_content
    # prompt = request.POST['prompt']
    # prompt = prom_test
    # prompt = "Please make a summary in PT-BR, divided into details, based on the text below. Also translate into en-us language.\n\n "+ prom_test
    # print(len(prompt))
    data = {
        "model": "mistral:7b-instruct-v0.2-q8_0",
        "prompt": impt,
        "context": context_convers,
        "options": {
            "temperature": 0.9,
            "num_predict": -1,
            "repeat_penalty": 1.5,
            "mirostat_eta": 0.9,
            "mirostat_tau": 5.0,
            "mirostat": 0,
            "top_k": 50,
            "top_p": 0.90,
            "tfs_z": 2.0,
            # "num_ctx": 324,

        }
    }

    # headers = {'Content-Type': 'application/json'}

    try:
    
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 200:  # HTTP status code for "OK"
            resp = response.text
            # respj = json.loads(json.dumps(resp))
            # print(type(resp))
            linhas = resp.split("\n")
            # linha = [linha for linha in linhas]
            l = int(len(linhas)-2)

            sl = linhas[l:]
            dt_context = json.loads(sl[0])
            for i in dt_context["context"]:
                context_convers.append(i)

            a = len(linhas)-2
            gravar_array_arquivo(context_convers, file)
            for x in range(a):
                j = json.loads(linhas[x])
                list_words.append(j['response'])

            text = ''.join(list_words)
            # print("context: ", context_convers)
            print("\n\n", text)

            return text
        else:
            print("Error:", response.status_code, response.reason)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)

    # return data
file_name = []
pagePdf = []

def extract() -> str:
    
    reader = PdfReader("django.pdf")
    page = reader.pages
    for page_ in page:
        text_ = break_text(page_.extract_text())
    return str(text_[0:10])
    
def download(url):
    
    response = requests.get(url, stream=True)
    filename = response.url.split('/')[-1]
    extension = url.split('/')[-1].split('.')[-1]
    
    if extension == "pdf" or "epub":
        file_name.append(filename)
        with open(filename, "wb") as out_file:
            contents = response.content
            out_file.write(contents)
        out_file.close()
        
    # print(file_name)

    # print("File '{}' has been downloaded.".format(filename))
def post_request():
    import json
    import requests
    key="AIzaSyASeL1rBAdqNADK_fHQJ0CYVIsMTF8BwDY"
    query = "filetype: pdf OR epub  programacao"
    url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx=004867295691306056793:tnmgrobc-km&q={query}"
    data = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3"}
    json_data = json.dumps(data)
    response = requests.get(url, headers=data)
    ppp = json.loads(json.dumps(response.json()))
    links = [ ppp["items"][link]["link"] for link in range(0, len(ppp["items"])) ]
    for d in links:
        print("link: ", d)
        download(d)

def langchain_():
    from langchain.schema import HumanMessage
    chat_m = ChatOllama(model="mistral:7b-instruct-v0.2-q8_0")

    messages = [
        HumanMessage(
            content="What color is the sky at different times of the day? responda em pt-br"
        )
        ] 
    response_ = chat_m(messages).content
    print(response_)
# middleware(extract())
# while True:

# try:
#     impt = input("sua pergunta: ")
#     # middleware(impt)
#     print(break_text(impt))
# except Exception as err:
#     pass
#     continue
langchain_()