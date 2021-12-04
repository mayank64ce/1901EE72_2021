# storing roots of the webpages
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import json
import shutil
from flask_cors import cross_origin
from pathlib import Path
# this file is a blueprint of our site
from subprocess import run


views = Blueprint('views', __name__)

BASE_PATH = os.path.dirname(
    os.path.realpath(__file__))

UPLOAD_FOLDER = BASE_PATH + "/uploads"
IMG_UPLOAD = UPLOAD_FOLDER + "/img"
CSV_UPLOAD = UPLOAD_FOLDER + "/csv"
TRANSCRIPT_DIR = BASE_PATH + "/output/transcriptsIITP"
GRADES = BASE_PATH + "/output/grade_sheets"


def vali():
    a = os.listdir(CSV_UPLOAD)
    if 'grades.csv' in a and 'names-roll.csv' in a and 'subjects_master.csv' in a:
        return True
    return False


def get_extension(file):
    ext = os.path.splitext(file)[1]
    return ext


@views.route('/deleteResidualOutput', methods=['GET'])
@cross_origin()
def delete_residual():
    if request.method == 'GET':
        try:
            run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
            run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])

            # run(f'rm -rf {GRADES}/*', shell=True)
            # run(['touch', str(GRADES+"/placeholder.txt")])

            run(f'rm -rf {IMG_UPLOAD}/*', shell=True)
            run(['touch', str(IMG_UPLOAD+"/placeholder.txt")])

            run(f'rm {CSV_UPLOAD}/*', shell=True)
            run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
            return json.dumps({'Success': "Residual files deleted."})
        except Exception as e:
            return json.dumps({'Error': str(e)})

    return "done"


@views.route('/upload/grades', methods=['GET', 'POST'])
@cross_origin()
def grades_csv():
    print("grades_csv")
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return json.dumps({"Error": "No file part found."})

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                return json.dumps({"Error": "No selected file."})

            print(file.filename, "************", get_extension(file.filename))

            if get_extension(file.filename) != ".csv":
                print('not allowed')
                return json.dump({"Error": "File not allowed."})

            # filename = secure_filename(file.filename)
            filename = "grades.csv"
            # print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(CSV_UPLOAD, filename))
            print("File Saved!")
            # is_master_uploaded = True
            # redirect(request.url)

            if vali():
                try:
                    from .semwise_marksheet_generator import generate_marksheet
                    print("Generating Marksheets")
                    generate_marksheet()
                    print("Marksheets Generated")

                    # return json.dumps({"Success": "Grades Processing Done"})
                except Exception as e:
                    print(e)
                    # raise Exception()
                    run(f'rm {CSV_UPLOAD}/*', shell=True)
                    run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
                    return json.dumps({"Error": str(e)})

            return json.dumps({"Success": "grades.csv file uploaded!"})

        except Exception as e:
            run(f'rm {CSV_UPLOAD}/*', shell=True)
            run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route('/upload/seal', methods=['GET', 'POST'])
@cross_origin()
def seal():
    print("seal")
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return json.dumps({"Error": "No file part found."})

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                # raise Exception()
                return json.dumps({"Error": "Error! No selected file."})

            print(file.filename, "************", get_extension(file.filename))

            if get_extension(file.filename) != ".jpeg" and get_extension(file.filename) != ".png":
                print('not allowed')
                return json.dumps({"Error": "File not allowed."})

            # filename = secure_filename(file.filename)
            filename = "seal.png"
            # print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(IMG_UPLOAD, filename))
            print("File Saved!")
            # is_master_uploaded = True
            # redirect(request.url)

            return json.dumps({"Success": "file uploaded!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route('/upload/signature/', methods=['GET', 'POST'])
@cross_origin()
def sign():
    print("sign")
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return json.dumps({"Error": "No file part found."})

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                return json.dumps({"Error": "Error! No selected file."})

            print(file.filename, "************", get_extension(file.filename))

            if get_extension(file.filename) != ".jpeg" and get_extension(file.filename) != ".png":
                print('not allowed')
                return json.dumps({"Error": "File not allowed."})

            # filename = secure_filename(file.filename)
            filename = "sign.png"
            # print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(IMG_UPLOAD, filename))
            print("File Saved!")
            # is_master_uploaded = True
            # redirect(request.url)

            return json.dumps({"Success": "file uploaded!"})

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route("/query/range/", methods=['GET', 'POST'])
@cross_origin()
def range():
    print("sign")
    if request.method == 'POST':
        try:
            print("working..")

            try:
                print("I will delete.")
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
            except Exception as e:
                return json.dumps({"Error": str(e)})

            content = request.json
            print(content)

            start = content['from']['rangeFrom']
            end = content['to']['rangeTo']

            print(start, end)
            if len(start) == 0 or len(end) == 0:
                return json.dumps({"Error": "Invalid Range"})

            # implement clear output directory in generate_in_range.py

            if not vali():
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
                run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
                return json.dumps({"Error": "Some required csv files are missing."})

            from .generate_in_range import generate_in_range
            print("Start Range")
            try:
                start = start.upper()
                end = end.upper()
                not_found = generate_in_range(start, end)
                print("These were not found", not_found)
            except Exception as e:
                print(e)
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
                run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
                return json.dumps({"Error": str(e)})
            print("End Range")

            # output not_found somehow??
            # not_found = []

            # print("Hello")
            return json.dumps({"Success": "Range Files Generated!", "Info": not_found})

        except Exception as e:
            run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
            run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route("/downloadzip/", methods=['GET', 'POST'])
@cross_origin()
def downloadzip():
    print("downloadzip")
    if request.method == 'GET':
        try:
            print("working..")
            # put in download script here

            dir = BASE_PATH + "/output/transcriptsIITP"

            if "placeholder.txt" in os.listdir(dir) and len(os.listdir(dir)) == 1:
                print("No Files To download")
                return json.dumps({"Error": "No Files To download"})

            output_file = BASE_PATH + "/output/send_back/transcriptsIITP"

            shutil.make_archive(output_file, 'zip', dir)
            print("Done Compressing")
            import webbrowser
            # return send_file(output_file+".zip", as_attachment=True)
            return webbrowser.open(output_file+".zip")

        except Exception as e:
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route("/query/full/", methods=['GET', 'POST'])
@cross_origin()
def full():
    print("full")
    if request.method == 'GET':
        try:
            print("working..")

            if not vali():
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
                run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
                raise Exception("Error.. Some required csv files are missing.")

            from .generate_transcript_all import generate
            print("Generating all transcripts")

            try:
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
                print("I will delete.")

            except Exception as e:
                return json.dumps({"Error": str(e)})

            try:
                generate()
            except:
                run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
                run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
                return json.dumps({"Error": "Could not generate all transcripts."})

            print("All transcripts generated")
            return json.dumps({"Success": "All Transcripts Generated Successfully"})

        except Exception as e:
            run(f'rm -rf {TRANSCRIPT_DIR}/*', shell=True)
            run(['touch', str(TRANSCRIPT_DIR+"/placeholder.txt")])
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route('/upload/stud_roll', methods=['GET', 'POST'])
@cross_origin()
def names_roll():
    print("names_roll")
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return json.dumps({"Error": "No file part found."})

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                return json.dumps({"Error": "No selected file."})

            print(file.filename, "************", get_extension(file.filename))

            if get_extension(file.filename) != ".csv":
                print('not allowed')
                return json.dump({"Error": "File not allowed."})

            # filename = secure_filename(file.filename)
            filename = "names-roll.csv"
            # print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(CSV_UPLOAD, filename))
            print("File Saved!")
            # is_master_uploaded = True
            # redirect(request.url)
            if vali():
                try:
                    from .semwise_marksheet_generator import generate_marksheet
                    print("Generating Marksheets")
                    generate_marksheet()
                    print("Marksheets Generated")
                except Exception as e:
                    print(e)
                    run(f'rm {CSV_UPLOAD}/*', shell=True)
                    run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
                    return json.dumps({"Error": str(e)})

            return json.dumps({"Success": "names-roll.csv file uploaded!"})

        except Exception as e:
            run(f'rm {CSV_UPLOAD}/*', shell=True)
            run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")


@views.route('/upload/subject_master', methods=['GET', 'POST'])
@cross_origin()
def subjects_master():
    print("subjects_master")
    if request.method == 'POST':
        try:
            print("working..")
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return json.dumps({"Error": "No file part found."})

            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if not file or file.filename == '':
                print('No selected file')
                return json.dumps({"Error": "No selected file."})

            print(file.filename, "************", get_extension(file.filename))

            if get_extension(file.filename) != ".csv":
                print('not allowed')
                return json.dump({"Error": "File not allowed."})

            # filename = secure_filename(file.filename)
            filename = "subjects_master.csv"
            # print('UPLOAD', UPLOAD_FOLDER, os.getcwd())
            file.save(os.path.join(CSV_UPLOAD, filename))
            print("File Saved!")
            # is_master_uploaded = True
            # redirect(request.url)
            if vali():
                try:
                    from .semwise_marksheet_generator import generate_marksheet
                    print("Generating Marksheets")
                    generate_marksheet()
                    print("Marksheets Generated")
                except Exception as e:
                    print(e)
                    run(f'rm {CSV_UPLOAD}/*', shell=True)
                    run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
                    raise Exception("Could not generate marksheets.")

            return json.dumps({"Success": "subjects_master.csv file uploaded!"})

        except Exception as e:
            run(f'rm {CSV_UPLOAD}/*', shell=True)
            run(['touch', str(CSV_UPLOAD+"/placeholder.txt")])
            return json.dumps({"Error": str(e)})

    return "done"  # render_template("client/public/index.html")
