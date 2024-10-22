import base64
import requests
from config import Config
from utils.helpers import parse_openai_response


# OpenAI API Key
api_key = Config.OPENAI_API_KEY

def enhance_product_description(base64_image, title=None, description=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the prompt and image data in the messages
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Por favor, gere um título, descrição aprimorada e tags baseadas nesta imagem do produto: {description}. Título sugerido: {title}."
                },
                {
                    "type": "text",
                    "text": (
                        "Por favor, gere um título otimizado, descrição aprimorada e tags baseadas nesta imagem do produto."
                        " Certifique-se de que a resposta siga exatamente o formato abaixo:"
                        "\n\n"
                        "**Título Sugerido:** [Coloque o título aqui]\n\n"
                        "**Descrição Aprimorada:**\n[Coloque a descrição aqui]\n\n"
                        "**Tags:**\n- [Tag1],\n- [Tag2],\n- [Tag3]\n\n"
                        "As tags devem estar separadas por vírgulas e listadas uma por linha, começando com '-'."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        if response.status_code != 200:
            return {"error": f"Erro ao processar a imagem: {response.status_code} - {response.json()}"}
        
        result = response.json()

        if not result or "choices" not in result or not result["choices"]:
            return {"error": "Erro ao processar a imagem: resposta inválida do ChatGPT"}

        # Extração do conteúdo
        content = result["choices"][0]["message"]["content"].strip()

        parsed_result = parse_openai_response(content)

        # Aqui você pode ajustar como deseja extrair as informações (título, descrição, tags) do conteúdo retornado
        return {
            'optimized_title': parsed_result['optimized_title'],  # Título otimizado pode ser processado conforme necessário
            'enhanced_description': parsed_result['enhanced_description'],  # Descrição aprimorada
            'tags': parsed_result['tags'],  # Tags podem ser extraídas da resposta, se aplicável
            'full_response': content
        }

    except Exception as e:
        return {"error": f"Erro ao processar a imagem: {e}"}