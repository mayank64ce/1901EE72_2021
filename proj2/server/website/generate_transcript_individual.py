import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
plt.rcParams.update({'font.size': 8})

BASE_PATH = os.path.dirname(
    os.path.realpath(__file__))

TEMP_ASSET_DIR = BASE_PATH + "/output/assets/"
PERM_ASSET_DIR = BASE_PATH + "/assets/"
TRANSCRIPT_DIR = BASE_PATH + "/output/transcriptsIITP/"


def is_seal_uploaded():
    # path = os.getcwd()
    path = BASE_PATH + "/uploads/img"
    if "seal.png" in os.listdir(path) or "seal.jpg" in os.listdir(path):
        return True
    return False


def is_sign_uploaded():
    path = BASE_PATH + "/uploads/img"
    if "sign.png" in os.listdir(path) or "sign.jpg" in os.listdir(path):
        return True
    return False


all_branches = {
    "CS": "Computer Science and Engineering",
    "EE": "Electrical Engineering",
    "ME": "Mechanical Engineering",
    "MM": "Metalurgical and Materials Engineering",
    "CB": "Chemical and Bio-Chemical Engineering",
    "MA": "Mathematics",
    "PH": "Physics",
    "CH": "Chemistry"
}

all_programs = {
    "01": "B.Tech",
    "11": "M.Tech",
    "12": "M.Sc",
    "21": "PhD."
}


def get_details(rollno):
    bcode = rollno[4:6]
    branch = all_branches[bcode]
    year = "20"+rollno[0:2]
    prog_code = rollno[2:4]
    program = all_programs[prog_code]
    return year, branch, program


def generate_transcript(rollno):
    print("Hello, I am here")
    excel_file = BASE_PATH + "/output/grade_sheets/" + str(rollno) + ".xlsx"

    xls = pd.ExcelFile(excel_file)
    # sem1 = pd.read_excel(xls, "Sem1")
    # print(sem1.loc[0])
    try:
        overall = pd.read_excel(xls, "Overall")
    except:
        print("No Overall sheet")
        raise Exception("No Overall Detected")
    try:
        overall.drop(columns=["Roll No."], inplace=True)
        credits_taken = overall.iloc[3].values
        # print(credits_taken)
        credits_clear = overall.iloc[4].values  # change this in future
        spi_all = overall.iloc[5].values
        cpi_all = overall.iloc[7].values
        student_name = overall.iloc[0].values[0]
        rollno = overall.columns[0]
        year, branch, program = get_details(rollno)
    except Exception as e:
        print(e)
        raise e
    print(student_name, rollno, branch, year)

    print("check", overall.columns)

    def get_sems(xls):
        sems = xls.sheet_names
        sems = sems[1:]
        return sems
    print("Hello 1")
    sems = get_sems(xls)

    total_sems = len(sems)

    def plot_sem(excel, sem):
        # overall = pd.read_excel(xls, "Overall")
        sheet_name = sem
        df = pd.read_excel(excel, sheet_name)
        df = df[['Subject No.', 'Subject Name', 'L-T-P', 'Credit', 'Grade']]

        fig, ax = plt.subplots()

        # hide axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        tab = ax.table(cellText=df.values, colLabels=df.columns, loc='center', colWidths=[
            0.10, 0.4, 0.15, 0.1, 0.1], cellLoc='center')
        tab.auto_set_font_size(False)
        tab.set_fontsize(8)
        # tab.auto_set_column_width([0,1,2,3,4,5,6])
        fig.tight_layout()

        sem_name = "Semester"+str(sem.split(' ')[-1])
        # plt.title(sem_name, y=1.08)

        # ax.set_title(sem_name)
        output_img = TEMP_ASSET_DIR + sem_name+'.png'
        plt.savefig(output_img, dpi=200)
        # plt.show()
    print("Hello 2")

    def generate_semester_images(xls):

        df = pd.read_excel(xls)
        print("Hello from gen_sem_images")
        for sem in sems:
            print(sem)
            plot_sem(xls, sem)
    print("******************")
    generate_semester_images(xls)
    print("Hello 3")

    def setup_pdf():
        if(total_sems > 6):
            pdf = FPDF(orientation="P", format="A3")
        else:
            pdf = FPDF(orientation="L", format="A4")

        pdf.add_page()
        pdf.set_font('Arial', 'B', 7)
        pdf.set_margins(left=15, top=10)

        pdf.line(15-0.2, 10-0.2, 15-0.2, 200+0.2)  # L
        # pdf.line(300-15, 10+0.2, 300+15, 200)
        pdf.line(300-15+0.2, 10, 300-15+0.2, 200)  # R

        pdf.line(15, 200+0.2, 300-15, 200+0.2)

        pdf.line(15, 10-0.2, 300-15, 10-0.2)
        pdf.cell(w=10, h=10)
        pdf.image(PERM_ASSET_DIR + "/iitp_banner.jpeg",  w=260, type="jpeg")
        pdf.ln(h=0.2)
        pdf.line(15, pdf.get_y()+0.2, 300-15, pdf.get_y()+0.2)

        upper_base = pdf.get_y()
        pdf.set_xy(x=45, y=upper_base+1)
        pdf.image(PERM_ASSET_DIR + "/student_info_card.png", w=200)
        pdf.set_xy(x=45+17, y=upper_base+2.5)
        pdf.cell(w=55, h=5, txt=rollno)
        pdf.cell(w=110, h=5, txt=student_name)
        pdf.cell(w=25, h=5, txt=year)

        pdf.set_xy(x=50+17, y=upper_base+2.5+5)
        pdf.cell(w=55, h=5, txt=program)
        pdf.cell(w=110, h=5, txt=branch)
        pdf.set_xy(x=15, y=upper_base+2.5+10+2)
        # pdf.cell()
        # pdf.ln(h=15)
        # xog = pdf.get_x()
        # yog = pdf.get_y()
        return pdf
    pdf = setup_pdf()
    print("Hello 4")

    def generate_semesters_pdf(pdf, xls, total_sems):
        xof = pdf.get_x()
        yof = pdf.get_y()

        base = yof
        max_pv_row = 0

        for j, sem in enumerate(sems):
            # print()
            # print("og", xof, yof, base)
            # pdf.set_x(xof)
            pdf.set_y(yof)
            pdf.set_x(xof)

            sem_no = int(sem.split(' ')[-1])

            # if(sem == 1 or sem == 7):
            #   yog = yof
            #   xog = xof

            # print("sem", pdf.get_x(), pdf.get_y())
            pdf.set_xy(x=pdf.get_x()+4, y=pdf.get_y()+3)
            pdf.cell(w=12, h=5, txt="Semester "+str(sem_no), border=0)
            # pdf.set_xy(x=pdf.get_x(), y=pdf.get_y()-)
            # yof += 6
            # pdf.set_y(yof)

            pdf.set_x(pdf.get_x()-15)

            # pdf.cell(w=12, h=5, txt="Semester "+str(sem), border=0)
            # print("chk", pdf.get_x(), xof)
            pdf.set_xy(pdf.get_x()-5, pdf.get_y()-15)
            # print("chk", pdf.get_x(), xof)
            # print("chk", pdf.get_x(), xof)
            # print("image", pdf.get_x(), pdf.get_y())
            img_name = BASE_PATH + "/output/assets/" + \
                "Semester"+str(sem_no) + ".png"
            pdf.image(name=img_name, w=int(270/3), type="png")
            # pdf.ln(h=1)
            pdf.set_xy(pdf.get_x()+5, pdf.get_y()-20)
            pdf.rect(pdf.get_x(), pdf.get_y()+2, w=int(270/3)-10-3, h=6)
            c_taken = credits_taken[j]
            c_clear = credits_clear[j]
            spi = spi_all[j]
            cpi = cpi_all[j]
            pdf.cell(w=270/3-20, h=10, txt="Credits taken:  "+str(c_taken)+"    "+"Credits cleared:  " +
                     str(c_clear)+"    "+"SPI:"+str("%.2f" % round(spi, 2))+"    "+"CPI:"+str("%.2f" % round(cpi, 2)))
            # print("end", pdf.get_x(), pdf.get_y())
            pdf.set_xy(pdf.get_x(), pdf.get_y()+15)

            max_pv_row = max(max_pv_row, pdf.get_y())

            xof += int(270/3+1)
            pdf.set_y(base)
            pdf.set_x(xof)
            # print(yof, pdf.get_y())

            if (j+1) == 3 or (j+1) == 6 or (j+1) == 9:
                yof = max_pv_row
                base = yof
                xof = 15
                pdf.set_y(base)
                pdf.set_x(xof)
                pdf.line(15, base-3, 300-15, base-3)

    generate_semesters_pdf(pdf, xls, total_sems)
    print("Hello 5")

    def add_seal_stamp(pdf, xls):
        bottom = 200
        if total_sems > 6:
            bottom = 410

        pdf.set_xy(15+5, bottom-30)
        pdf.cell(w=15, h=5, txt="Date of Generation: " +
                 str(datetime.date.today()), border=0)
        if(is_seal_uploaded()):
            pdf.image(x=270/2, y=bottom-30-15+5,
                      name=BASE_PATH + "/uploads/img/seal.png", w=20, type="png")

        pdf.set_xy(300-15-5-15-20, bottom-30)
        pdf.cell(w=20, h=5, txt="Assistant Registrar(Academic)")
        pdf.line(300-15-5-15-20, bottom-30-2, 300-15-5-15+10+5, bottom-30-2)
        if(is_sign_uploaded()):
            pdf.image(x=300-15-5-15-20+5, y=bottom-30-15 +
                      5, name=BASE_PATH + "/uploads/img/sign.png", w=25, type="png")

    add_seal_stamp(pdf, xls)
    print("Hello 6")
    return pdf


def generate_transcript_for(rollno):
    if rollno+".pdf" in os.listdir(TRANSCRIPT_DIR):
        print("Already Exists for "+rollno)
        return

    print("generating for ", rollno)

    pdf = generate_transcript(rollno)
    pdf.output(TRANSCRIPT_DIR+rollno+".pdf", 'F')
