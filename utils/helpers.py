import re

def parse_openai_response(response_text):
    description_match = re.search(r'Descrição Aprimorada:\s*(.*?)\nTags:', response_text, re.DOTALL)
    tags_match = re.search(r'Tags:\s*(.*?)\nTítulo Otimizado:', response_text, re.DOTALL)
    title_match = re.search(r'Título Otimizado:\s*(.*)', response_text)
    
    description = description_match.group(1).strip() if description_match else ''
    tags = [tag.strip() for tag in tags_match.group(1).split(',')] if tags_match else []
    optimized_title = title_match.group(1).strip() if title_match else ''
    
    return {
        'description': description,
        'tags': tags,
        'optimized_title': optimized_title
    }
    