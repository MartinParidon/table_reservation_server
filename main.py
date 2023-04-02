from flask import Flask, render_template, jsonify, request
import json
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True
app.logger.setLevel('DEBUG')


@app.route('/seats')
def seats():
    with open('data/seats.csv', 'r') as f:
        seats_data = f.read()
    return jsonify(seats_data)


@app.route('/')
def index():
    # Read the seat data from the CSV file
    seat_data = pd.read_csv('data/seats.csv').to_dict(orient='records')

    # Generate the HTML code for the table
    table_html = '<table>'
    table_html += '<tr><th>Seat #</th><th>Status</th><th>Name</th><th>Reserve</th></tr>'
    for seat in seat_data:
        status = 'green' if seat['status'] == 'available' else 'red'
        name = seat['name'] if seat['name'] else ''
        reserve_button = f'<button class="reserve-btn" data-seat="{seat["number"]}">Reserve</button>'
        #table_html += f'<tr><td>{seat["number"]}</td><td><div class="status {status}"></div></td><td>{name}</td><td>{reserve_button}</td></tr>'
        table_html += f'<tr><td>{seat["number"]}</td><td><div class="status {status}"></div></td><td><div class="name">{name}</div></td><td>{reserve_button}</td></tr>'
    table_html += '</table>'

    # Render the template file with the HTML code for the table
    return render_template('index.html', table_html=table_html)


@app.route('/reserve', methods=['POST'])
def reserve():
    seat_data = pd.read_csv('data/seats.csv')
    seat_number = int(request.form['seat'])
    name = request.form['name']
    seat_data.loc[seat_data['number'] == seat_number, 'status'] = 'reserved'
    seat_data.loc[seat_data['number'] == seat_number, 'name'] = name
    seat_data.to_csv('data/seats.csv', index=False)
    return jsonify({'status': 'success'})


# @app.route('/reserve', methods=['POST'])
# def reserve():
#     seats_df = pd.read_csv('data/seats.csv', index_col='number')
#     seat_num = request.form['seat']
#     name = request.form['name']
#     seats_df.at[int(seat_num), 'status'] = 'reserved'
#     seats_df.at[int(seat_num), 'name'] = name
#     seats_df.to_csv('data/seats.csv')
#     if seats_df.loc[int(seat_num), 'status'] == 'reserved':
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False})


if __name__ == '__main__':
    app.run(debug=True)
