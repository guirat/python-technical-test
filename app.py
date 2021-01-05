from flask import redirect
import os
import config

connexion_app = config.connexion_app

connexion_app.add_api('api.yml')

app = config.app


@app.route('/')
def doc_root():
    return redirect("/api/ui")


if __name__ == "__main__":
    connexion_app.run(debug=True)