from os import listdir, remove


for file in listdir("./flask_session"):
    remove(f"./flask_session/{file}")
