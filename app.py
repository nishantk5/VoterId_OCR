import os
import os.path
import pytesseract
import re
from PIL import Image
from flask import Flask,jsonify,request,render_template
from werkzeug.utils import secure_filename
#pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
app=Flask(__name__)
UPLOAD_FOLDER='./uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def get_name(text):
    # Initializing data variable
    name = None
    fname = None
    nameline = []
    text0 = []
    text1 = []
    text2 = []

    # Searching
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    # print(text1)
    text1 = list(
        filter(None, text1))  # Attribute has to be converted into a list object before any additional processing
    # print(text1) #at this operation the new line strings become a list of strings

    lineno = 0  # to start from the first line of the text file.

    for wordline in text1:
        xx = wordline.split('\n')
        if ([w for w in xx if re.search(
                '(ELECTOR|PHOTO|IDENTITY|CARD|ELECTION|COMMISSION|INDIA|IND|NDIA)$',
                w)]):
            text1 = list(text1)
            lineno = text1.index(wordline)
            break
    # text1 = list(text1)
    text0 = text1[lineno + 1:]
    # print(text0) #Contains all the relevant extracted text in form of a list - uncomment to check
    try:
        for x in text0:
            for y in x.split():
                # print(x)
                nameline.append(x)
                break
    except:
        pass
    # print(nameline)
    try:
        name = nameline[2].rsplit(':', 1)[1]
        fname = nameline[4].rsplit(':', 1)[1]

    except:
        pass
    # Making tuples of data
    data = {}
    data['Name'] = name
    data['Father Name'] = fname
    return data

@app.route('/',methods=["GET","POST"])
def Voter_ID():
    if request.method=="POST":
        f=request.files['file']
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        file_path=os.path.join(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        img = Image.open(file_path)
        img = img.convert('RGBA')
        pix = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'],'temp.png'))
        # extracting text from image using tesseract
        text = pytesseract.image_to_string(Image.open(os.path.join(app.config['UPLOAD_FOLDER'],'temp.png')))
        # print(text)
        data = get_name(text)
        return jsonify({"voter_id_data":data})
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)



