from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
from pprint import pprint

# Fetch the service account key JSON file contents
cred = credentials.Certificate('botframe-2d07e-firebase-adminsdk-gt6r2-644290ce5e.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://botframe-2d07e.firebaseio.com/'
})

# import firebase_admin
# from firebase_admin import credentials, firestore
#
# cred = credentials.Certificate("botframe-2d07e-firebase-adminsdk-gt6r2-038b5d6c34.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

app = Flask(__name__)
CORS(app)

base_response = {
    'speech': "sample response",
    'source': 'Manual'
}


# doc_ref = db.collection(u'question').document(u'elmPUPLG3a4v45M2VuKt')
# doc = doc_ref.get().to_dict()
# print(doc)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    data = request.get_json(silent=True)
    pprint(data)
    if data["result"]["action"] == "BMI.BMI-custom.BMI-calculate-custom":
        w = int(data['result']['parameters']['weight'])
        h = int(data['result']['parameters']['height']) / 100
        bmi = (w / (h * h))
        print(bmi)
        if bmi < 18.5:
            result = 'คุณผอมไป กินข้าวเยอะๆ'
        elif 18.5 <= bmi <= 22.9:
            result = 'คุณหุ่นดีสุดๆเลย'
        elif 23 <= bmi <= 24.9:
            result = 'คุณเริ่มอ้วนแล้วนะ'
        elif 25 <= bmi <= 29.9:
            result = 'คุณอ้วนแล้ว ออกกำลังกายด่วน'
        else:
            result = 'คุณอ้วนมากแล้วอันตราย หาหมอด่วนควย'
        reply = {
            'speech': result,
        }
        return jsonify(reply)
    elif data["result"]["action"] == "input.unknown":
        # if data['originalRequest']['data'] != {}:
        #     msg = data['originalRequest']['data']['message']['text']
        if data['result']['resolvedQuery'] != "":
            msg = data['result']['resolvedQuery']
        ref = db.reference('question')
        ref.push({
            'question': msg,
        })
        return '', 200
    elif data["result"]["action"] == '':
        name = data["result"]["metadata"]["intentName"]
        ref = db.reference('/intentCount/' + name)
        if ref.get() is None:
            ref.push({
                'success': 1,
                'fail': 0
            });
        else:
            updateref = db.reference('/intentCount/' + name)
            temp = updateref.get()

            for key, val in temp.items():
                keyid = key
                successcount = val["success"]

            ref.update({
                keyid + '/success': successcount + 1
            })

        return '', 200


@app.route('/countfail', methods=['GET', 'POST', 'OPTION'])
def countFail():
    data = request.get_json(silent=True)
    name = data["name"];
    ref = db.reference('/intentCount/' + name)
    if ref.get() is None:
        ref.push({
            'success': 0,
            'fail': 1
        });
    else:
        updateref = db.reference('/intentCount/' + name)
        temp = updateref.get()

        for key, val in temp.items():
            keyid = key
            failcount = val["fail"]

        ref.update({
            keyid + '/fail': failcount+1
        })
    return jsonify(data)


@app.route('/getcount', methods=['GET', 'OPTION'])
def getcount():
    # data = request.get_json(silent=True)
    # name = data["name"];
    ref = db.reference('/intentCount/')
    print(type(ref.get().items()))
    labels = []
    success = []
    fail = []
    sumsuccess = 0
    sumfail = 0
    for item in ref.get().items():
        # temp = dict(item)
        for i in item:
            if type(i) is not str:
                t = dict(i).items()
                for key, val in t:
                    success.append(val["success"])
                    fail.append(val["fail"])
                    sumfail += val["fail"]
                    sumsuccess += val["success"]
            else:
                labels.append(i)
    reply = {
        'Labels': labels,
        'success': success,
        'fail': fail,
        'sumsuccess': sumsuccess,
        'sumfail': sumfail,
    }
    return jsonify(reply)


# https://sut-line-bot.herokuapp.com/webhook
if __name__ == '__main__':
    app.run()
