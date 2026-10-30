"""DeployLite's lightweight Flask dashboard."""

from flask import Flask, jsonify, render_template
import os
import platform
import socket

app = Flask(__name__)
VERSION = "1.0.0"


@app.get("/")
def index():
    return render_template(
        "index.html",
        version=VERSION,
        hostname=socket.gethostname(),
        python_version=platform.python_version(),
        platform_name=platform.system(),
        port=os.environ.get("PORT", "5000"),
    )


@app.get("/health")
def health():
    return jsonify(status="healthy", application="DeployLite", version=VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
