from flask import Blueprint, render_template, make_response, jsonify, request
from flask_login import login_required, current_user
from .models import Pltainfo
from . import db
import matlab.engine
import io
import time
import os

main = Blueprint('main', __name__)
matlab_file_path = r''+os.getcwd()+r'\app_pjb\matlab_files'

@main.route('/')
def index():
    name = current_user.name if hasattr(current_user, 'name') else ""
    return render_template('index.html', name=name)

@main.route('/profile')
@login_required
def profile():
    user_info = {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }
    return render_template('profile.html', user_info=user_info)

@main.route('/calculation')
@login_required
def calculation():
    output_table = {
        'inflow_selorejo': 0.0, 
        'elevasi_awal': 0.0, 
        'elevasi_target': 0.0, 
        'elevasi_akhir': 0.0, 
        'outflow_selorejo': 0.0, 
        'mw_selorejo': 0.0, 
        'mwh_selorejo': 0.0, 
        'limpas': 0.0, 
        'inflow_outflow_mendalan': 0.0, 
        'mw_mendalan_1': 0.0, 
        'mw_mendalan_2': 0.0, 
        'mw_mendalan_3': 0.0, 
        'mw_mendalan_4': 0.0, 
        'mw_mendalan': 0.0, 
        'mwh_mendalan': 0.0, 
        'suplesi_siman': 0.0, 
        'inflow_siman': 0.0, 
        'mw_siman_1': 0.0, 
        'mw_siman_2': 0.0, 
        'mw_siman_3': 0.0, 
        'mw_siman': 0.0, 
        'mwh_siman': 0.0
    }
    return render_template('calc.html', name=current_user.name, output_table=output_table, js='calc.js')

def valid_input(value):
    return value != None and value != ''

@main.route('/calc', methods=['POST'])
@login_required
def calc():
    headers = {"Content-Type": "application/json"}
    resp_dict = {
        'error': True,
        'data': {},
        'msg' : '',
        'exec_time': False
    }
    elv_awal = request.form.get('elv_awal')
    elv_akhir = request.form.get('elv_akhir')
    inf_selorejo = request.form.get('inf_selorejo')
    supl = request.form.get('supl')
    if valid_input(elv_awal) == False or valid_input(elv_akhir) == False or valid_input(inf_selorejo) == False or valid_input(supl) == False:
        resp_dict['msg'] = "Invalid input"
        return make_response(jsonify(resp_dict), 400, headers)

    try:
        elv_awal = float(elv_awal)
        elv_akhir = float(elv_akhir)
        inf_selorejo = float(inf_selorejo)
        supl = float(supl)
    except Exception as e:
        resp_dict['msg'] = str(e)
        return make_response(jsonify(resp_dict), 400, headers)
    
    start_time = time.time()
    
    result = {}

    match_data = Pltainfo.query.filter_by(elevasi_awal=elv_awal, elevasi_target=elv_akhir, inflow_selorejo=inf_selorejo).first()
    if match_data != None:
        tmp = match_data.__dict__
        del tmp['_sa_instance_state']
        result = tmp
    else:
        eng = matlab.engine.start_matlab()
        eng.addpath(matlab_file_path)
        
        try:
            result = eng.pjb_func(matlab.double([elv_awal]), matlab.double([elv_akhir]), matlab.double([inf_selorejo]), matlab.double([supl]), nargout=1)
            # result = eng.test(matlab.double([elv_awal]), matlab.double([elv_akhir]), nargout=1)
        except Exception as e:
            resp_dict['msg'] = str(e)
            return make_response(jsonify(resp_dict), 400, headers)

        eng.quit()

        dam_data = Pltainfo(**result)
        try:
            db.session.add(dam_data)
            db.session.commit()
        except Exception as e:
            print(str(e))

    resp_dict['exec_time'] = time.time() - start_time
    resp_dict['error'] = False
    resp_dict['data'] = result
    return make_response(jsonify(resp_dict), 200, headers)
    
@main.route('/data')
@login_required
def data():
    table_col = ['inflow_selorejo', 'elevasi_awal', 'elevasi_target', 'elevasi_akhir', 'outflow_selorejo', 'mw_selorejo', 'mwh_selorejo', 
    'limpas', 'inflow_outflow_mendalan', 'mw_mendalan_1', 'mw_mendalan_2', 'mw_mendalan_3', 'mw_mendalan_4', 'mw_mendalan', 'mwh_mendalan', 
    'suplesi_siman', 'inflow_siman', 'mw_siman_1', 'mw_siman_2', 'mw_siman_3', 'mw_siman', 'mwh_siman']
    col_to_disp = ['inflow_selorejo', 'elevasi_awal', 'elevasi_target', 'elevasi_akhir', 'outflow_selorejo',]
    return render_template('data.html', column=table_col, col_to_disp=col_to_disp, js='data.js')