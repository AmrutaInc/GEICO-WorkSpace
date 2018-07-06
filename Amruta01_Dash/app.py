import base64
import io

import flask
import dash
# from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import numpy as np
import pandas as pd
# import xlwt
import os

app = dash.Dash()
app.config['UPLOAD_FOLDER'] = "static"
server = app.server
app.title = 'AmrutaInc'
app.scripts.config.serve_locally = True

app.layout = html.Div([

        html.A(html.Img(src="/static/amruta_logo.jpg", alt='Amruta Inc',
                        style={

                                'width': '30%',
                                'height': '100px'
                                }
                        ), href='http://amrutainc.com/'),

            html.H2('GEICO'),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={

            'width': '30%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'float': 'left'
        },
        # Allow multiple files to be uploaded
        multiple=True
                ),

    html.A(html.Button('Download',
        style={

                'width': '30%',
                'height': '62px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'float': 'left'
                },),
                id='download-link',
                download="Fraud_Data.csv",
                href="",
                target="_blank",
                n_clicks=0
        ),

    html.Div(id='output-data-upload'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})

])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df['Score'] = np.random.randint(1, 1000, size=len(df))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        dt.DataTable(rows=df.to_dict(orient='records'), row_selectable=True,),
            html.P('Do you agree?',
                    style={
                            'textAlign': 'center',
                        }),
            dcc.RadioItems(
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': ' No ', 'value': 'No'},
            ],
            value='No',
            style={
                'textAlign': 'center',
                    }
        )

        # For debugging, display the raw contents provided by the web browser
        #html.Div('Raw Content'),
        #html.Pre(contents[0:200] + '...', style={
            #'whiteSpace': 'pre-wrap',
            #'wordBreak': 'break-all'
        #})
    ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'Robsonbillponte-Sinem-File-Downloads.ico')

@app.callback(
    Output('download-link', 'href'),
    [Input('download-link', 'n_clicks')])

def generate_report_url(n_clicks):

    return '/dash/urldownload'

@app.server.route('/dash/urldownload')

def generate_report_url():

    return flask.send_file('Fraud_Data.csv', attachment_filename='Fraud_Data.csv', as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)
