from fastapi import FastAPI

def create_app():
    app = FastAPI()

    @app.get('/')
    def root():
        return {'message': 'Hello World'}

    return app