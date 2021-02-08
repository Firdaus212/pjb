from flask import Blueprint, render_template, make_response, jsonify, request, send_file, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import *
from . import db, eng
import io, time, os, re
from .helpers import *
import matlab.engine
import pandas as pd

main = Blueprint('main', __name__)
base_app_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
matlab_file_path_selorejo = base_app_path + '/matlab_files/selorejo'
matlab_file_path_sengguruh = base_app_path + '/matlab_files/sengguruh'
matlab_file_path_sutami = base_app_path + '/matlab_files/sutami'

# Remove key from dictionary
def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]
    return the_dict

# Generate data to insert to the database
def generate_insert_data(result, area):
    if area == area_sms_1:
        return SMS1(**result)
    elif area == area_sms_2:
        return SMS2(**result)
    elif area == area_sutami_wlingi_basah:
        return SutamiWlingi(**result)
    elif area == area_sengguruh:
        return Sengguruh(**result)

# Check if data with certain input value already present on the database
def check_data_exist_in_database(input, area):
    found = None
    if area == area_sms_1:
        found = SMS1.query.filter_by(**input).first()
    elif area == area_sms_2:
        found = SMS2.query.filter_by(**input).first()
    elif area == area_sutami_wlingi_basah:
        found = SutamiWlingi.query.filter_by(**input).first()
    elif area == area_sengguruh:
        found = Sengguruh.query.filter_by(**input).first()
    if found != None:
        return True, found
    return False, found

# Conver input to float data type
def conver_to_float(inp):
    try:
        for k in inp:
            if k == 't1' or k == 't2' or k == 't3':
                inp[k] = [float(v) for v in inp[k]]
            else:    
                inp[k] = float(inp[k])
    except Exception as e:
        return False, str(e)
    return True, inp

# Perform cascade optimization calculation by executing matlab function script
# using matlab engine for python.
# See https://www.mathworks.com/help/matlab/matlab-engine-for-python.html for more details
def perform_optimization(resp_dict, post_data, area):
    start_time = time.time()
    conv_status, conv_res = conver_to_float(post_data)
    if conv_status == False:
        resp_dict['msg'] = 'Invalid Input'
        return resp_dict, 400
    
    result = {}

    is_data_exist = False

    if area == area_sms_1 or area == area_sms_2:
        is_data_exist, data_found = check_data_exist_in_database(conv_res, area)

    if is_data_exist:
        data_found = data_found.__dict__
        del data_found['_sa_instance_state']
        result = data_found
    else:
        try:
            if area == area_sms_1:
                eng.addpath(matlab_file_path_selorejo)
                result = eng.sms1(conv_res)
            elif area == area_sms_2:
                eng.addpath(matlab_file_path_selorejo)
                result = eng.sms2(conv_res)
            elif area == area_sutami_wlingi_basah:
                eng.addpath(matlab_file_path_sutami)
                result = eng.sutami_wlingi_basah(conv_res)
            elif area == area_sutami_wlingi_kering:
                eng.addpath(matlab_file_path_sutami)
                result = eng.sutami_wlingi_kering(conv_res)
            elif area == area_sengguruh:
                eng.addpath(matlab_file_path_sengguruh)
                result = eng.sengguruh(conv_res)
            # eng.quit()
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400

        if result != {} and ( area == area_sms_1 or area == area_sms_2 ):
            result.update(conv_res)
            insert_data = generate_insert_data(result, area)
            try:
                db.session.add(insert_data)
                db.session.commit()
            except Exception as e:
                resp_dict['db_insert_error'] = str(e)

    resp_dict['exec_time'] = time.time() - start_time
    resp_dict['error'] = False
    resp_dict['data'] = result
    return resp_dict, 200

# Index or Home page route
@main.route('/')
def index():
    name = current_user.name if hasattr(current_user, 'name') else ""
    return render_template('index.html', name=name)



# Page not found route
@main.route('/not_found')
# @login_required
def not_found():
    return render_template('404.html', data=data)

# Optimization page route
@main.route('/optimization/<string:area>', methods=['GET'])
@login_required
def optimization(area):
    if area == area_sms_1:
        data = get_sms_opt_1_page_data()
    elif area == area_sms_2:
        data = get_sms_opt_2_page_data()
    elif area == area_sutami_wlingi_basah:
        data = get_sutami_wlingi_wet_opt_page_data()
    elif area == area_sutami_wlingi_kering:
        data = get_sutami_wlingi_dry_opt_page_data()
    elif area == area_sengguruh:
        data = get_sengguruh_opt_page_data()
    else:
        return redirect(url_for('main.not_found'))
    data['name'] = current_user.name
    return render_template('optimization.html', data=data )

# Route for ajax call to perfom optimization process based on input provided
@main.route('/optimize', methods=['POST'])
@login_required
def optimize():
    start_time = time.time()
    status = 200
    area = request.form.get('area')
    post_data = request.form.to_dict()
    if area == area_sutami_wlingi_basah or area == area_sutami_wlingi_kering:
        post_data['t1'] = request.form.getlist('t1[]')
        post_data['t2'] = request.form.getlist('t2[]')
        post_data['t3'] = request.form.getlist('t3[]')
        post_data = entries_to_remove(('area', 't1[]', 't2[]', 't3[]'), post_data)
    else:
        post_data = entries_to_remove(('area',), post_data)

    resp_dict = {
        'error': True,
        'data': {},
        'msg' : '',
        'exec_time': -1
    }
    if area == area_sms_1:
        resp_dict, status = perform_optimization(resp_dict, post_data, area)
    elif area == area_sms_2:
        resp_dict, status = perform_optimization(resp_dict, post_data, area)
    elif area == area_sutami_wlingi_basah:
        resp_dict, status = perform_optimization(resp_dict, post_data, area)
    elif area == area_sutami_wlingi_kering:
        resp_dict, status = perform_optimization(resp_dict, post_data, area)
    elif area == area_sengguruh:
        resp_dict, status = perform_optimization(resp_dict, post_data, area)
        
    return make_response(jsonify(resp_dict), status, headers)  

# Matlab files page route
@main.route('/matlab-files', methods=['GET'])
@login_required
def matlab_files():
    data = {}
    data['title'] = "Matlab Files for Optimization"
    data['selorejo'] = os.listdir(matlab_file_path_selorejo)
    data['sutami-wlingi'] = os.listdir(matlab_file_path_sutami)
    data['sengguruh'] = os.listdir(matlab_file_path_sengguruh)
    return render_template('matlab-data.html', data=data)

# Route for downloading matlab file saved on the server
@main.route('/download/<string:folder>/<string:filename>', methods=['GET'])
@login_required
def download(folder, filename):
    folder_name = ''

    if folder == 'selorejo':
        folder_name = matlab_file_path_selorejo
    elif folder == 'sutami-wlingi':
        folder_name = matlab_file_path_sutami
    elif folder == 'sengguruh':
        folder_name = matlab_file_path_sengguruh

    if folder_name != '' and os.path.exists(folder_name + '\\' +filename):
        return send_file(folder_name + '\\' +filename, as_attachment=True, cache_timeout=0)
    else:
        return make_response(jsonify({'status': 'error', 'msg': 'File not found'}), 400, headers)  
