import os
from app import create_app, db
from app.models import Post, Tag, User, Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Tag=Tag, User=User, Role=Role)


if __name__ == '__main__':
    app.run()