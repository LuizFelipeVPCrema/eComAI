from flask import Blueprint, request, jsonify
from services.openai_service import enhance_product_description
from utils.helpers import ajust_img
import base64

product_blueprint = Blueprint('product_blueprint', __name__)

@product_blueprint.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem fornecida'}), 400

    image_file = request.files['image']
    title = request.form.get('title', '')
    initial_description = request.form.get('description', '')
    
    processed_image = ajust_img(image_file)
    
    image_base64 = base64.b64encode(processed_image.read()).decode('utf-8')

    # Passar a imagem para o serviço que faz a análise
    result = enhance_product_description(image_base64, title, initial_description)

    if 'error' in result:
        return jsonify(result), 500

    # Criar a estrutura de resposta
    product_data = {
        'original_title': title,
        'optimized_title': result['optimized_title'],
        'initial_description': initial_description,
        'enhanced_description': result['enhanced_description'],
        'tags': result['tags'],
        'full_response': result['full_response']
    }

    return jsonify({
        'message': 'Processamento concluído',
        'product': product_data
    }), 200
