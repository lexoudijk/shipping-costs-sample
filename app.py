#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {
    'Food':"Pizza. Most definitely pizza. Too cold. Too hot. I don't care. There's no such thing as bad pizza. Except pineapple pizza", 
    'Drink':"Westmalle Tripel. Fantastic Belgian beer. Non-alcoholic: good coffee. I mean good. Artisan and all. And fresh OJ", 
    'Sports team':"Ajax Amsterdam", 
    'Country':"My own, The Netherlands. The US, Canada and England aren't too bad either", 
    'City':"Hard to choose, either London or San Francisco. Depends on the day and my mood I guess",
    'Brand':"Nike. It has been cool for as long as I know. That is an amazin achievement. And the flagship store at Oxford Circus is awesome. Niketown, a must-visit",
    'Restaurant':"McD..., uh no. Let's say Noma. Google it."
    }

    speech = "My favorite " + zone + " is " + str(cost[zone]) + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
