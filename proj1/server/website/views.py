# storing roots of the webpages
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import json
from flask_cors import cross_origin
# this file is a blueprint of our site
from subprocess import run

negative = 0
positive = 0
# is_responses_uploaded = False
# is_master_uploaded = False

views = Blueprint('views', __name__)
UPLOAD_FOLDER = os.getcwd() + '/website/uploads/csv'
OUTPUT_DIR = os.getcwd() + '/website/output/rollNumberWise'
OUTPUT_CONC_DIR = os.getcwd() + '/website/output/concise'
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# validate rem


@views.route('/deleteResidualOutput', methods=['GET'])
@cross_origin()
def delete_residual():
    if request.method == 'GET':
        try:
            run(f'rm -rf {OUTPUT_DIR}/*', shell=True)
            run(['touch', str(OUTPUT_DIR+"/placeholder.txt")])

            run(f'rm -rf {OUTPUT_CONC_DIR}/*', shell=True)
            run(['touch', str(OUTPUT_CONC_DIR+"/placeholder.txt")])

            run(f'rm -rf {UPLOAD_FOLDER}/*', shell=True)
            run(['touch', str(UPLOAD_FOLDER+"/placeholder.txt")])
            return json.dumps({"Success": "Residual files deleted."})
        except Exception as e:
            return json.dumps({'Error:': str(e)})

    return "done"


@views.route('/upload/master/', methods=['GET', 'POST'])
@cross_origin()
def master():
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                raise Exception("Error! No file part found.")

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                raise Exception("Error! No selected file.")

            if not allowed_file(file.filename):
                print('not allowed')
                raise Exception("Error! File not allowed.")

            # filename = secure_filename(file.filename)
            filename = "master.csv"
            print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # is_master_uploaded = True
            # redirect(request.url)
            return json.dumps({"Success": "file uploaded!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


# validate rem
@views.route('/upload/responses/', methods=['GET', 'POST'])
@cross_origin()
def responses():
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                raise Exception("Error! No file part found.")

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                raise Exception("Error! No selected file.")

            if not allowed_file(file.filename):
                print('not allowed')
                raise Exception("Error! File not allowed.")

            # filename = secure_filename(file.filename)
            filename = "responses.csv"
            print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # is_responses_uploaded = True
            # redirect(request.url)
            return json.dumps({"Success": "file uploaded!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route('/output/marksheet/', methods=['GET', 'POST'])
@cross_origin()
def marksheet():
    global positive, negative
    if request.method == 'POST':
        try:
            # operation validations
            if not os.path.exists(UPLOAD_FOLDER+'/master.csv') or not os.path.exists(UPLOAD_FOLDER+'/responses.csv'):
                raise Exception(
                    "Files not uploaded. Cant generate marksheets ")
            content = request.json
            positive = float(content['positive']['posMark'])
            negative = float(content['negative']['negMark'])
            # print(positive, negative)
            from .rollNoWise import driver
            driver()
            # redirect(request.url)
            return json.dumps({"Success": "marksheets generated!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"


@views.route('/output/concise-marksheet/', methods=['GET', 'POST'])
@cross_origin()
def concise_marksheet():
    if request.method == 'GET':
        try:
            # operation validations
            if not os.path.exists(UPLOAD_FOLDER+'/master.csv') or not os.path.exists(UPLOAD_FOLDER+'/responses.csv'):
                raise Exception(
                    "Files not uploaded. Can't do any operations. ")
            if os.path.exists(OUTPUT_DIR+'/placeholder.txt') and len(os.listdir(OUTPUT_DIR)) == 1:
                raise Exception(
                    "Marksheets have not been generated. Can't generate concise marksheet. ")
            from .concise import driver
            driver()
            # redirect(request.url)
            return json.dumps({"Success": "concise generated!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"


@views.route('/send-email/', methods=['GET', 'POST'])
@cross_origin()
def send_email():
    if request.method == 'GET':
        try:
            # operation validations
            if not os.path.exists(UPLOAD_FOLDER+'/master.csv') or not os.path.exists(UPLOAD_FOLDER+'/responses.csv'):
                raise Exception(
                    "Files not uploaded. Can't do any operations. ")
            if os.path.exists(OUTPUT_DIR+'/placeholder.txt'):
                raise Exception(
                    "Marksheets have not been generated. Can't send emails. ")
            print("Sending Email.......")
            from .email_marksheets import email_marksheets
            email_marksheets()
            # redirect(request.url)
            return json.dumps({"Success": "emails sent!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"
