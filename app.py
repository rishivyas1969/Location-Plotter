from branca.element import Div
from bs4.element import Script
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas
from geopy.geocoders import Nominatim
from Map import map
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', btn=None)

@app.route('/success', methods=['POST'])
def success():
    global file, lst
    if request.method=='POST':
        file = request.files['file']
        file.save(secure_filename('uploaded'+file.filename))
        
        data = pandas.read_csv('uploaded'+file.filename.replace(' ', '_'))


        col = data.columns
        col = [ x.lower() for x in col]
        data.columns = col

        if 'address' not in data.columns:
            return render_template("index.html", btn=['noAddress.html'])
        else:
            arc = Nominatim(user_agent="ny_explorer")

            lst = []

            for i in range(data.shape[0]):
                sub_lst = []
                sub_lst.append(data['address'][i])
                n=arc.geocode(data['address'][i])
                sub_lst.append(n.latitude)
                sub_lst.append(n.longitude)
                lst.append(sub_lst)
                print(sub_lst)

            print(len(lst))

        return render_template("index.html", btn='coordinates.html', lst=lst)


@app.route('/plot')
def plot():
    
    html_str = map(lst)

    if type(html_str) == None:
        return render_template('sample.html', txt="Can't reload again. Visit Home!")

    soup = BeautifulSoup(html_str, 'html.parser')
    style = soup.find_all('style')[-1]
    script = soup.find_all('script')[-1]
    div=soup.div

    return render_template('map.html', style=style, script=script, div=div)

if __name__ == '__main__':
    app.debug=True
    app.run()