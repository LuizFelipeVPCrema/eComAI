from .product_routes import product_blueprint

def register_routes(app):
    app.register_blueprint(product_blueprint)
    
    
__all__ = ['register_routes']