# PJB
This is an application used for calculate some variables on a Hydro Powered Generator.

## Prerequisite
1. Matlab with minimum version R2018a 64-bit.
2. Python version 3.6 64-bit.

## Install Matlab
### Refer to guide on the link bellow on how to download and install Matlab. 
* Download Matlab from [Matlab](https://www.mathworks.com/downloads/).
* Install using this [Installation Guide](https://www.mathworks.com/help/install/install-products.html).

## Install Python
* Download python from this link [Python-3.6.8](https://www.python.org/downloads/release/python-368/).
* Python [Installation Guide](https://realpython.com/installing-python/).

## Setting up the project
1. Clone this [PJB Repo](https://github.com/Firdaus212/pjb.git).
2. Change the directory to repo directory.
    
    ``` bash
    $ cd pjb
     ```
3. Create python environment.
    ``` bash
    $ python -m venv [your-virtual-environment-name]
    ```
4. Activate the virtual environment.
    ```bash
    $ [your-virtual-environment-name]\Script\activate
    ```
5. Change directory to **project** folder.
    ``` bash
    $ cd project
    ```
6. Install the python requirements.
    ``` bash
    $ pip install -r requirements.txt
    ```
7. Install Matlab Engine API to the python environment
    #### Change directory to matlab engine api for python installation directory and install the library. See [Matlab Engine API Installation for Python Guide](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html).
    ``` bash
    $ cd [your-matlab-installation-directory]\[matlab-version]\extern\engines\python

    $ python setup.py install
    ```
8. Change the directory back to the repository project folder.
    ``` bash
    $ cd [your-clonned-repo-path]\project
    ```
9. Run the Flask App.
    ``` bash
    $ flask run
    ```
10. The app should be served on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    Open that url address on the browser.
    ``` 
    Credential
    Username : admin@pjb.com
    Pasword  : 1q2w3e4r
    ```
