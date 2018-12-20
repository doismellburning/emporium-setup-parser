from flask import Flask, request
import setuptools
import collections


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
    setuptools.find_packages = lambda *args, **kwargs: None

    real_import = __import__

    class FakeThing():
        def __getattr__(self, name):
            return FakeThing()
        def __call__(self, *args, **kwargs):
            return FakeThing()
        def __int__(self):
            return 0
        def __enter__(self):
            return FakeThing()
        def __exit__(self, *args, **kwargs):
            pass
        def __add__(self, other):
            return other

    def fake_import(*args, **kwargs):
        if args[0] in ["sys", "setuptools", "tokenize", "time", "io", "os", "codecs", "re"]:
            return real_import(*args, **kwargs)

        print(args[0])

        return FakeThing()


    def fake_open(*args, **kwargs):
        import io
        return io.StringIO("")


    setup_locals = collections.defaultdict(FakeThing, locals())
    setup_locals["__file__"] = ""
    setup_globals = collections.defaultdict(FakeThing, globals())
    setup_globals["__builtins__"].__import__ = fake_import
    setup_globals["__builtins__"].open = fake_open

    exec(setuppy, setup_globals, setup_locals)

    return str(setup_data)


if __name__ == '__main__':
    app.run()
