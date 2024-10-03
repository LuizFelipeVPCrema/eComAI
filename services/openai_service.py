import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY


def enhance_product_description(title, description, image_url=None):
    messages = [
        {"role": "system", "content": "Você é um especialista em marketing de produtos para e-commerce."},
        {
            "role": "user",
            "content": f"Título do Produto: {title}\nDescrição Inicial: {description}"
        }
    ]
    if image_url is None:
        messages.append({"role": "user", "content": f"Imagem do Produto: {image_url}"})
    
    
    prompt = f"""
    Por favor, forneça:
    
    Título do Produto: {title}
    Descrição Inicial: {description}
    
    Por favor, forneça:
    
    1. Uma descrição detalhada e envolvente do produto.
    2. Uma lista de tags relevantes separadas por vírgulas.
    3. Um título otimizado para o produto.
    
    Responda no seguinte formato:
    
    Descrição Aprimorada: <sua descrição aqui>
    
    Tags: <tag1>, <tag2>, <tag3>, ...
    
    Título Otimizado: <seu título aqui>
    """
    
    messages.append({"role": "user", "content": prompt})
    
    try:
    
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            n=1,
            stop=None
        )
        
        # Extrair a resposta
        content = response.choices[0].message.content.strip()
        
        return content
    except AttributeError:
        print("Erro: Resposta da OpenAI está vazia ou mal formatada")
        content = "Erro ao processar a descrição do produto"