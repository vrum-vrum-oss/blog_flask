import os
from app import create_app, db
from app.models import Post, Tag, User, Role, Follow


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Tag=Tag, User=User, Role=Role, Follow=Follow)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()