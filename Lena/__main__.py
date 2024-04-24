import Anony
from Ash import app

if __name__ == "__main__":
    app.run()
    with app:
        app.send_message()
