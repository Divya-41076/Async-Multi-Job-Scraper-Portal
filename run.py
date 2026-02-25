# entry point for the Flask application
import os
from app import create_app #this line imports the create_app function from the app module that is init file in the app package
from app.extensions.db import db


app = create_app() #this line calls the create_app function to create an instance of the Flask application

with app.app_context():
    # db.drop_all()
    db.create_all()

# for confirmation
# print("DB USER:", os.getenv("DB_USER"))
# print("DB HOST:", os.getenv("DB_HOST"))

if __name__ == "__main__":
    app.run(debug=True) #this line runs the Flask application in debug mode if the script is executed directly

