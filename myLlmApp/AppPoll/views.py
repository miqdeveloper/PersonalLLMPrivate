from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from langchain.document_loaders import SeleniumURLLoader
import requests
import json

template = "index/index.html"
models = "mistral:v0.2"
urls_test = [
    "https://docs.djangoproject.com/en/5.0/topics/async/#asgiref.sync.sync_to_async"]
global context_convers
context_convers = []
file = "beggin.txt"

def gravar_array_arquivo(array, arquivo):
  """
  Grava uma linha que é um array em um arquivo de texto.

  Args:
    array: O array a ser gravado.
    arquivo: O arquivo de texto em que o array será gravado.
  """

  with open(arquivo, "a") as f:
    f.write(",".join(map(str, array)))

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

async def middleware(request):
    url = " http://localhost:11434/api/generate"
    # headers = {'Content-Type': 'application/json'}
    

    if (request.POST['prompt'] and request.POST['model']):

        # urlHtml = SeleniumURLLoader(urls_test)
        # urlHtml = urlHtml.load()
        # urlHtml = urlHtml[0]
        # prom_test = urlHtml.page_content
        prompt = request.POST['prompt']
        # prompt = prom_test
        # prompt = "Please make a summary in PT-BR, divided into details, based on the text below. Also translate into en-us language.\n\n " + prom_test
        # print(len(prompt))
        model = request.POST['model']

        if model == "":
            return "model vazio "
        else:
            model = request.POST['model']
            
        a= ler_array_arquivo(file)
        if a == None:
            context_convers  = []
        
        data = {
            "model": model,
            "prompt": prompt,
            "context": context_convers,
            "options": {
                "temperature": 0.9,
                "num_predict": -1,
                "repeat_penalty": 1.1,
                "mirostat_eta": 0.7,
                "mirostat_tau": 6.0,
                "mirostat": 0,
                "top_k": 50,
                "top_p": 0.90,
                "tfs_z": 2.0,
                #"num_ctx": 2024,

            }
        }

        try:
                
            response = requests.post(url, data=json.dumps(data))
            # print("MY RESPONSE:", response)
            #print(context_convers)
            if response.status_code == 200:  # HTTP status code for "OK"
                resp = response.text
                list_words = []
                linhas = resp.split("\n")
                l = int(len(linhas)-2)

                sl = linhas[l:]
                dt_context = json.loads(sl[0])
                for i in dt_context["context"]:
                    context_convers.append(i)
                
                #print(gravar_array_arquivo(context_convers, file))

                a = len(linhas) - 2

                for x in range(a):
                    j = json.loads(linhas[x])
                    list_words.append(j['response'])

                text = ''.join(list_words)

                return text
            else:
                print("Error:", response.status_code, response.reason)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)

        return data
    if (request.POST['prompt'] == ""):
        return "prompt vazio digite alguma coisa"
    else:
        return "prompt vazio digite alguma coisa"


async def index(request):
    # print(request)
    return_prompt = "Seja bem vindo ao PrivateGPT"
    if (request.POST):
        # radioEscolha =

        # print("dbg -->", request.POST)
        # return_prompt = request.POST

        return_prompt = await middleware(request)

    return render(request, template, {
        "prt": return_prompt,
    })

# Create your views here.
