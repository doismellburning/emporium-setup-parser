from flask import Flask, request
import setuptools


app = Flask(__name__)

@app.route('/parse', methods=["POST"])
def parse():
    setuppy = request.get_data()
    setup_data = {}

    def fake_setup(*args, **kwargs):
        setup_data["install_requires"] = kwargs.get("install_requires")
        setup_data["extras_require"] = kwargs.get("extras_require")
        setup_data["tests_require"] = kwargs.get("tests_require")

    setuptools.setup = fake_setup

    exec(setuppy)

    return str(setup_data)


if __name__ == '__main__':
    app.run()
