from .app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", use_reloader=True, debug=True)
