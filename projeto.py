from colorthief import ColorThief
from PIL import Image
import requests
from io import BytesIO

def obter_paleta_da_imagem(url_imagem, quantidade_cores=7):
    resposta = requests.get(url_imagem)
    imagem = Image.open(BytesIO(resposta.content))
    
    if imagem.mode != 'RGB':
        imagem = imagem.convert('RGB')
    
    imagem.save('temp_image.jpg')
    color_thief = ColorThief('temp_image.jpg')
    paleta = color_thief.get_palette(color_count=quantidade_cores, quality=10)
    cores_hex = []
    
    for cor in paleta:
        r = cor[0]
        g = cor[1]
        b = cor[2]
        cor_hex = f'#{r:02x}{g:02x}{b:02x}'
        cores_hex.append(cor_hex)
    
    return cores_hex

def criar_arquivo_css(cores, nome_arquivo="paleta.css"):
    arquivo = open(nome_arquivo, "w")
    
    arquivo.write(":root {\n")
    
    for i in range(len(cores)):
        nome_variavel = f"    --cor-{i + 1}"
        cor = cores[i]
        arquivo.write(f"{nome_variavel}: {cor};\n")
    
    arquivo.write("}")
    arquivo.close()

def gerar_paleta(url_imagem):
    cores = obter_paleta_da_imagem(url_imagem)
    
    criar_arquivo_css(cores)
    
    print("Paleta gerada com sucesso!")
    print("Cores extraídas:")
    for i in range(len(cores)):
        print(f"Cor {i + 1}: {cores[i]}")

# url = "https://wallpaperaccess.com/full/4958475.jpg"
url = input("Digite a URL da imagem: ")

gerar_paleta(url)