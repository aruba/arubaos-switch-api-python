# arubaos-switch-python

These scripts are written for ArubaOS Switch API version 4.0.

## Structure

* REST API call functions are found in the /src folder.
* Functions from the /src folder are combined to emulate network processes that are stored in the /workflows folder.
* Data to be imported into functions is stored in the /sampledata folder.


## How to run this code
There are different workflows covered in this repo under /workflows directory. Before starting ensure the switch REST API is enabled:
```switch# rest-interface```


In order to run these scripts, please complete the steps below:
1. install virtual env (refer https://docs.python.org/3/library/venv.html). Make sure python version 3 is installed in system.
    
    ```
    $ python3 -m venv switchenv
    ```
2. Activate the virtual env
    ```
    $ source switchenv/bin/activate
    ```
3. Install all packages required from requirements file
    ```
    (switchenv)$ pip install -r /arubaos-switch-api-python/requirements.txt
    ```

4. Open the project arubaos-switch-api-python from an editor (eg: Pycharm)
5. Set the project interpreter as the new virtual env created in step 1
6. Go to corresponding data yaml of each workflow and give the correct switch ip and credentials
7. Now you can run different workflows from arubaos-switch-api-python/workflows E.G. `base_provision.py` 
