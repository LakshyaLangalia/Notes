# main.py runs the app by calling the create_app function in __init__.py

from Website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

