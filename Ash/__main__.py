import uvloop
from Ash import app
from Anony import LOGGER_GROUP

if __name__ == "__main__":
    uvloop.install()
    app.run()
    with app:
        app.send_message(LOGGER_GROUP, "Asʜ Kᴇᴛᴄʜᴜᴍ Hᴀs Bᴇᴇɴ Sᴜᴄᴄᴇssғᴜʟʟʏ Aᴡᴀᴋᴇɴᴇᴅ !")
