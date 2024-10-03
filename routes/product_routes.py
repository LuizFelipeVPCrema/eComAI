# from flask import Blueprint, request, jsonify
# from services.image_service import generate_image_description
# # from models.product import Product
# # from database.db import get_db
# import cloudinary.uploader

# product_blueprint = Blueprint('product_blueprint', __name__)

# # Rota para processar a imagem e gerar a descrição
# @product_blueprint.route('/process_image', methods=['POST'])
# def process_image():
#     # Verificar se a imagem foi enviada
#     if 'image' not in request.files:
#         return jsonify({'error': 'Nenhuma imagem fornecida'}), 400

#     # Receber o arquivo de imagem
#     image_file = request.files['image']

#     # Enviar a imagem para o Cloudinary
#     # upload_result = cloudinary.uploader.upload(image_file)
#     # image_url = upload_result.get('secure_url')

#     result = generate_image_description(image_file)
    
#     if 'error' in result:
#         return jsonify(result), 500
    
#     # Receber o título e a descrição inicial
#     title = request.form.get('title', '')
#     initial_description = request.form.get('description', '')

#     # Gerar a descrição da imagem com o serviço BLIP
#     # description = generate_image_description(image_url)
    
#     # if description is None:
#     #     return jsonify({'error': 'Erro ao gerar descrição da imagem'}), 500

#     # Criar o produto e salvar no banco de dados
#     # product = Product({
#     #     'original_title': title,
#     #     'optimized_title': title,  # Aqui você pode incluir otimizações no título se necessário
#     #     'initial_description': initial_description,
#     #     'enhanced_description': description,
#     #     'tags': [],  # Adicione as tags conforme necessário
#     #     'image_url': image_url
#     # })

#     product_data = {
#         'original_title': title,
#         'optimized_title': title,  # Aqui você pode incluir otimizações no título se necessário
#         'initial_description': initial_description,
#         'enhanced_description': result['description'],
#         'tags': [],  # Adicione as tags conforme necessário
#         'image_url': result['image_url']
#     }

#     # Obter a instância do banco de dados
#     # db = get_db()

#     # # Verificar se o banco de dados foi obtido corretamente
#     # if db is None:
#     #     return jsonify({'error': 'Conexão com o banco de dados falhou'}), 500

#     # # Salvar o produto no banco de dados
#     # db.products.insert_one(product.to_dict())
    
#     # Retornar a resposta
#     # return jsonify({
#     #     'message': 'Processamento concluído',
#     #     'description': description,
#     #     'image_url': image_url
#     # }), 200
    
#     # Retornar a resposta diretamente, sem salvar no banco de dados
#     return jsonify({
#         'message': 'Processamento concluído',
#         'product': product_data
#     }), 200


from flask import Blueprint, request, jsonify
from services.image_service import process_image_and_generate_description
# from models.product import Product
# from database.db import get_db
import cloudinary.uploader

product_blueprint = Blueprint('product_blueprint', __name__)

# Rota para processar a imagem e gerar a descrição
@product_blueprint.route('/process_image', methods=['POST'])
def process_image():
    # Verificar se a imagem foi enviada
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem fornecida'}), 400

    # Receber o arquivo de imagem
    image_file = request.files['image']
    
    # Enviar a imagem para o Cloudinary
    upload_result = cloudinary.uploader.upload(image_file)
    image_url = upload_result.get('secure_url')

    # Receber o título e a descrição inicial
    title = request.form.get('title', '')
    initial_description = request.form.get('description', '')
    
    
    # Processar a imagem e gerar a descrição
    result = process_image_and_generate_description(image_url, title, initial_description)

    if 'error' in result:
        return jsonify(result), 500
    

    # Criar uma estrutura para o retorno
    product_data = {
        'original_title': title,
        'optimized_title': result['optimized_title'],
        'initial_description': initial_description,
        'enhanced_description': result['enhanced_description'],
        'tags': result['tags'],
        'image_url': result['image_url']
    }

    # Retornar a resposta diretamente, sem salvar no banco de dados
    return jsonify({
        'message': 'Processamento concluído',
        'product': product_data
    }), 200