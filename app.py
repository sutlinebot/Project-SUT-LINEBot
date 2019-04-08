from flask import Flask, request, abort, jsonify
app = Flask(__name__)

base_response = {
                'speech':"sample response",
                'source' : 'Manual'
                }

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    data = request.get_json(silent=True)
    print(data)
    w = int(data['result']['parameters']['weight'])
    h = int(data['result']['parameters']['height'])/100
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


if __name__ == '__main__':
    app.run()
