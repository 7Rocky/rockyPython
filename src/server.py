import bicimad_api.app
#import hello_app.app
import os

from flask import Flask

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
  bicimad_api.app.main(app)
  #hello_app.app.main(app)
  app.run(host='0.0.0.0', port=port, debug=True)
