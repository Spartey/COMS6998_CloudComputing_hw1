from flask import Flask
from flask import render_template, request
import twittDataBaseQuery
app = Flask(__name__)
@app.route("/",methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		id = int(request.form.get('q'))
		twitts= twittDataBaseQuery.getTwitts(id)
		return render_template('index.html', data = twitts)
	else:
		return render_template('index.html')
if __name__ == '__main__':
    app.run()