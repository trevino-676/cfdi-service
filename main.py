"""
author: Luis Manuel Torres Trevino
date: 13/04/2021
"""
from app import create_app

app = create_app()

app.run(host="0.0.0.0", port=5000)