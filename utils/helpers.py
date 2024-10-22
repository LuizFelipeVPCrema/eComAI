from PIL import Image
import io
import re

def parse_openai_response(response_text):

    title_match = re.search(r'\*\*Título Sugerido:\*\*\s*(.*?)\n', response_text, re.DOTALL)
    description_match = re.search(r'\*\*Descrição Aprimorada:\*\*\n(.*?)\n\*\*Tags:', response_text, re.DOTALL)
    tags_match = re.search(r'\*\*Tags:\*\*\n(.*?)$', response_text, re.DOTALL)

    optimized_title = title_match.group(1).strip() if title_match else ''
    enhanced_description = description_match.group(1).strip() if description_match else ''
    tags = [tag.strip() for tag in tags_match.group(1).split('-') if tag.strip()] if tags_match else []

    return {
        'optimized_title': optimized_title,
        'enhanced_description': enhanced_description,
        'tags': tags
    }

def ajust_img(file):
    try:
        img = Image.open(file)
        
        if img.mode in("RGBA", "P"):
            img = img.convert("RGB")
            
        max_size = (1280, 720)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size)
            
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return img_io
    except Exception as e:
        raise ValueError(f"Erro ao processar a imagem: {e}")
