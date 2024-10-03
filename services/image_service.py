from io import BytesIO
from .openai_service import enhance_product_description
import cloudinary.uploader
from config import Config
from PIL import Image
import requests

# Configuração do Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CONFIG['cloud_name'],
    api_key=Config.CLOUDINARY_CONFIG['api_key'],
    api_secret=Config.CLOUDINARY_CONFIG['api_secret']
)

# Função para fazer o upload da imagem para o Cloudinary
def upload_image(image_file):
    try:
        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result.get('secure_url')
        return image_url
    except Exception as e:
        print(f"Erro ao fazer o upload da imagem: {e}")
        return None


# Função que combina o upload da imagem com a geração de descrição e tags usando ChatGPT
def process_image_and_generate_description(image_file, title, description):
    # Fazer o upload da imagem para o Cloudinary
    image_url = upload_image(image_file)

    if image_url is None:
        return {'error': 'Erro ao fazer o upload da imagem'}

    # Usar a API do ChatGPT para gerar o título otimizado, descrição aprimorada e tags
    chatgpt_response = enhance_product_description(title, description, image_url)

    if "Erro" in chatgpt_response:
        return {'error': 'Erro ao gerar a descrição do produto usando ChatGPT'}
    
    # Separar a resposta do ChatGPT
    try:
        enhanced_description = chatgpt_response.split('Descrição Aprimorada:')[1].split('Tags:')[0].strip()
        tags = chatgpt_response.split('Tags:')[1].split('Título Otimizado:')[0].strip().split(',')
        optimized_title = chatgpt_response.split('Título Otimizado:')[1].strip()
    except Exception as e:
        print(f"Erro ao processar a resposta do ChatGPT: {e}")
        return {'error': 'Erro ao processar a resposta do ChatGPT'}

    return {
        'image_url': image_url,
        'enhanced_description': enhanced_description,
        'tags': [tag.strip() for tag in tags],  # Limpar os espaços das tags
        'optimized_title': optimized_title
    }
