import os
import subprocess
import redis
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    r = redis.StrictRedis(
        host=os.environ['REDIS_HOST'],
        port=6379,
        db=0
    )
    result = subprocess.run(['hostname', '-i'], stdout=subprocess.PIPE)
    ip = result.stdout.decode('utf-8')
    counter = r.get('visit_counter')
    if counter is None:
        r.set('visit_counter', 1)
        counter = 1
    r.incr('visit_counter')
    return "Hello human # {} from IP: {}".format(int(counter), ip)


@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
