import yaml
import os

'''
This function is to load the yaml file used for workflows.
How to use this function?

By default getyaml.readyaml() will load data.yaml data.
But if teh workflow reffering to a different yaml file in sampledata folder, call the function like
getyaml.readyaml('data_workflowname.yaml')

If the workflow requires more data try to have a different yaml file under sampledata folder. format: "data_workflowname.yaml"
'''


def readyaml(filename='data.yaml'):
    filename = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sampledata',filename))
    with open(filename, 'r') as ymlfile:
        data = yaml.load(ymlfile)
    return data