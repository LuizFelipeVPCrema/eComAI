import re

def parse_openai_response(response_text):
    # Usando regex para capturar o Título Sugerido, Descrição Aprimorada e Tags
    title_match = re.search(r'\*\*Título Sugerido:\*\*\s*(.*?)\n', response_text, re.DOTALL)
    description_match = re.search(r'\*\*Descrição Aprimorada:\*\*\n(.*?)\n\*\*Tags:', response_text, re.DOTALL)
    tags_match = re.search(r'\*\*Tags:\*\*\n(.*?)$', response_text, re.DOTALL)
    
    # Se houver correspondências, extrai o conteúdo, senão retorna vazio
    optimized_title = title_match.group(1).strip() if title_match else ''
    enhanced_description = description_match.group(1).strip() if description_match else ''
    tags = [tag.strip() for tag in tags_match.group(1).split('-') if tag.strip()] if tags_match else []

    return {
        'optimized_title': optimized_title,
        'enhanced_description': enhanced_description,
        'tags': tags
    }
