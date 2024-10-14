from bson.objectid import ObjectId


class Product:
    def __init__(self, data):
        self.id = data.get('_id', ObjectId())
        self.original_title = data.get('original_title')
        self.optimized_title = data.get('optimized_title')
        self.initial_description = data.get('initial_description')
        self.enhanced_description = data.get('enhanced_description')
        self.tags = data.get('tags')
        self.full_response = data.get('full_response')
        
    def to_dict(self):
        return{
            '_id': self.id,
            'original_title': self.original_title,
            'optimized_title': self.optimized_title,
            'initial_description': self.initial_description,
            'enhanced_description': self.enhanced_description,
            'tags': self.tags,
            'full_response': self.full_response
        }