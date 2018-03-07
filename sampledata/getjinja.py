

from jinja2 import Environment, FileSystemLoader
import os


def readjinja(file):
    # filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sampledata', file))
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(file)
    return template
