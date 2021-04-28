import pyrebase

config = {
  "apiKey": "--------",
  "authDomain": "-------",
  "databaseURL": "-------",
  "storageBucket": "--------"
}

# initialize app with config
firebase = pyrebase.initialize_app(config)

# authenticate a user
auth = firebase.auth()


db = firebase.database()
