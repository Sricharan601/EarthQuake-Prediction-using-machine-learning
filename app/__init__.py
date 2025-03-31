from flask import Flask
def create_app():
    app=Flask(__name__,static_folder='static')
    
    # from .routes import init_routes
    from .routes import main
    app.register_blueprint(main)
    # init_routes(app)
    
    return app
