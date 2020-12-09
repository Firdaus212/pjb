from flask import Blueprint, render_template, make_response, jsonify, request
from flask_login import login_required, current_user
from .models import Pltainfo
from . import db
import matlab.engine
import io
import time
import os

main = Blueprint('main', __name__)
matlab_file_path_selorejo = r''+os.getcwd()+r'\app_pjb\matlab_files\selorejo'
matlab_file_path_sengguruh = r''+os.getcwd()+r'\app_pjb\matlab_files\sengguruh'
matlab_file_path_sutami = r''+os.getcwd()+r'\app_pjb\matlab_files\sutami'
headers = {"Content-Type": "application/json"}

def valid_input(value):
    return value != None and value != ''

def converToFloat(inp):
    try:
        for k in inp:
            inp[k] = float(inp[k])
    except Exception as e:
        return False, str(e)
    return True, inp

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

@main.route('/calc', methods=['POST'])
@login_required
def calc():
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
        eng.addpath(matlab_file_path_selorejo)
        
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

@main.route('/sutamiwlingi')
@login_required
def sutamiwlingi():
    input_fields = ['elevasi_awal', 'elevasi_akhir', 'inflow', 'beban_wlingi', 'elevasi_real_wlingi', 'elevasi_target_wlingi', 'q_wlingi_yesterday', 'jam_mati_wlingi_kemarin']
    output_table = ['vol_tersedia', 'vol_used', 'volume_sisa', 'mean_beban_sutami_1', 'mean_beban_sutami_2', 'mean_beban_sutami_3', 
    'sum_beban_sutami_1', 'sum_beban_sutami_2', 'sum_beban_sutami_3', 'beban_total_sutami', 'beban_total_wlingi', 'jam_mulai_operasi_today',
    'jam_mati_operasi_wlingi', 'waktu_operasi_wlingi', 'energi_cascade']
    return render_template('sutamiwlingi.html', name=current_user.name, input_fields=input_fields, output_table=output_table, js='calc.js')

@main.route('/calc_sutamiwlingi', methods=['POST'])
@login_required
def calc_sutamiwlingi():
    resp_dict = {
        'error': True,
        'data': {},
        'msg' : '',
        'exec_time': False
    }

    conv_status, conv_res = converToFloat(request.form.to_dict())

    if conv_status == False:
        resp_dict['msg'] = conv_res
        return make_response(jsonify(resp_dict), 400, headers)
    
    start_time = time.time()
    
    result = {}

    
    # match_data = Pltainfo.query.filter_by(elevasi_awal=elv_awal, elevasi_target=elv_akhir, inflow_selorejo=inf_selorejo).first()
    # if match_data != None:
    #     tmp = match_data.__dict__
    #     del tmp['_sa_instance_state']
    #     result = tmp
    # else:
    eng = matlab.engine.start_matlab()
    eng.addpath(matlab_file_path_sutami)
    

    try:
        result = eng.opt(conv_res, nargout=1)
    except Exception as e:
        resp_dict['msg'] = str(e)
        return make_response(jsonify(resp_dict), 400, headers)

    eng.quit()

    #     dam_data = Pltainfo(**result)
    #     try:
    #         db.session.add(dam_data)
    #         db.session.commit()
    #     except Exception as e:
    #         print(str(e))

    resp_dict['exec_time'] = time.time() - start_time
    resp_dict['error'] = False
    resp_dict['data'] = result
    return make_response(jsonify(resp_dict), 200, headers)

@main.route('/sengguruh')
@login_required
def sengguruh():
    input_fields = ['inflow_sengguruh']
    output_table = ['beban_1', 'beban_2', 'energi_1', 'energi_2', 'total_energi']
    return render_template('sengguruh.html', name=current_user.name, input_fields=input_fields, output_table=output_table, js='calc.js')

@main.route('/calc_sengguruh', methods=['POST'])
@login_required
def calc_sengguruh():
    resp_dict = {
        'error': True,
        'data': {},
        'msg' : '',
        'exec_time': False
    }
    
    inflow_sengguruh = request.form.get('inflow_sengguruh')
    if valid_input(inflow_sengguruh) == False:
        resp_dict['msg'] = "Invalid input"
        return make_response(jsonify(resp_dict), 400, headers)

    try:
        inflow_sengguruh = float(inflow_sengguruh)
    except Exception as e:
        resp_dict['msg'] = str(e)
        return make_response(jsonify(resp_dict), 400, headers)

    start_time = time.time()

    eng = matlab.engine.start_matlab()
    eng.addpath(matlab_file_path_sengguruh)
    
    try:
        result = eng.opt_senguruh(matlab.double([inflow_sengguruh]), nargout=1)
        # result = eng.test(matlab.double([elv_awal]), matlab.double([elv_akhir]), nargout=1)
    except Exception as e:
        resp_dict['msg'] = str(e)
        return make_response(jsonify(resp_dict), 400, headers)

    eng.quit()

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
    col_to_disp = ['inflow_selorejo', 'elevasi_awal', 'elevasi_target', 'elevasi_akhir', 'outflow_selorejo','mw_selorejo', 'mwh_selorejo', 
    'limpas']
    return render_template('data.html', column=table_col, col_to_disp=col_to_disp, js='data.js')

@main.route('/elevation_data', methods=['POST'])
@login_required
def elevation_data():
    draw = int(request.form.get('draw'))
    offset = int(request.form.get('start'))
    limit = int(request.form.get('length'))
    info = Pltainfo.query.order_by(Pltainfo.elevasi_akhir).offset(offset).limit(limit).all()
    total = Pltainfo.query.count()
    data = []
    for inf in info:
        item = []
        for key in inf.__table__.columns.keys():
            if key != 'id':
                item.append(getattr(inf, key))
        data.append(item)
    resp_info = {
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    }
    return make_response(jsonify(resp_info), 200, headers)