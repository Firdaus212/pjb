from flask import Blueprint, render_template, make_response, jsonify, request
from flask_login import login_required, current_user
from .models import Pltainfo
from . import db
import matlab.engine
import io
import time
import os
import re
from .helpers import getSMSOpt1PageData, getSMSOpt2PageData, getSutamiWlingiOptPageData, getSengguruhOptPageData, getTableDataPageData

main = Blueprint('main', __name__)
matlab_file_path_selorejo = r''+os.getcwd()+r'\app_pjb\matlab_files\selorejo'
matlab_file_path_sengguruh = r''+os.getcwd()+r'\app_pjb\matlab_files\sengguruh'
matlab_file_path_sutami = r''+os.getcwd()+r'\app_pjb\matlab_files\sutami'
headers = {"Content-Type": "application/json"}

# def valid_input(value):
#     return value != None and value != ''

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
    return render_template('profile.html', data={'user_info': user_info})

# @main.route('/calc_sms', methods=['POST'])
# @login_required
# def calc_sms():
#     resp_dict = {
#         'error': True,
#         'data': {},
#         'msg' : '',
#         'exec_time': False
#     }
#     elv_awal = request.form.get('elv_awal')
#     elv_akhir = request.form.get('elv_akhir')
#     inf_selorejo = request.form.get('inf_selorejo')
#     supl = request.form.get('supl')
#     if valid_input(elv_awal) == False or valid_input(elv_akhir) == False or valid_input(inf_selorejo) == False or valid_input(supl) == False:
#         resp_dict['msg'] = "Invalid input"
#         return make_response(jsonify(resp_dict), 400, headers)

#     try:
#         elv_awal = float(elv_awal)
#         elv_akhir = float(elv_akhir)
#         inf_selorejo = float(inf_selorejo)
#         supl = float(supl)
#     except Exception as e:
#         resp_dict['msg'] = str(e)
#         return make_response(jsonify(resp_dict), 400, headers)
    
#     start_time = time.time()
    
#     result = {}

#     match_data = Pltainfo.query.filter_by(elevasi_awal=elv_awal, elevasi_target=elv_akhir, inflow_selorejo=inf_selorejo).first()
#     if match_data != None:
#         tmp = match_data.__dict__
#         del tmp['_sa_instance_state']
#         result = tmp
#     else:
#         eng = matlab.engine.start_matlab()
#         eng.addpath(matlab_file_path_selorejo)
        
#         try:
#             result = eng.pjb_func(matlab.double([elv_awal]), matlab.double([elv_akhir]), matlab.double([inf_selorejo]), matlab.double([supl]), nargout=1)
#             # result = eng.test(matlab.double([elv_awal]), matlab.double([elv_akhir]), nargout=1)
#         except Exception as e:
#             resp_dict['msg'] = str(e)
#             return make_response(jsonify(resp_dict), 400, headers)

#         eng.quit()

#         dam_data = Pltainfo(**result)
#         try:
#             db.session.add(dam_data)
#             db.session.commit()
#         except Exception as e:
#             print(str(e))

@main.route('/data')
@login_required
def data():
    return render_template('data.html', data=getTableDataPageData())

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

@main.route('/optimization/<string:area>', methods=['GET'])
@login_required
def optimization(area):
    if area == 'sms':
        data = getSMSOpt1PageData()
    elif area == 'sms_m':
        data = getSMSOpt2PageData()
    elif area == 'sutami-wlingi':
        data = getSutamiWlingiOptPageData()
    elif area == 'sengguruh':
        data = getSengguruhOptPageData()
    else:
        data = {}
    data['name'] = current_user.name
    return render_template('optimization.html', data=data )

def performOptimization(resp_dict, post_data, area):
    start_time = time.time()
    conv_status, conv_res = converToFloat(post_data)
    if conv_status == False:
        resp_dict['msg'] = 'Invalid Input'
        return resp_dict, 400
    
    result = {}

    if area == 'sms':
        eng = matlab.engine.start_matlab()
        eng.addpath(matlab_file_path_selorejo)
        
        try:
            result = eng.sms1(conv_res, nargout=1)
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400
        eng.quit()
    elif area == 'sms_m':
        eng = matlab.engine.start_matlab()
        eng.addpath(matlab_file_path_selorejo)
        
        try:
            result = eng.sms2(conv_res, nargout=1)
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400
        eng.quit()
    elif area == 'sutami-wlingi':
        eng = matlab.engine.start_matlab()
        eng.addpath(matlab_file_path_sutami)
        
        try:
            result = eng.opt(conv_res, nargout=1)
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400
        eng.quit()
    elif area == 'sengguruh':
        eng = matlab.engine.start_matlab()
        eng.addpath(matlab_file_path_sengguruh)
        
        try:
            result = eng.opt_senguruh(conv_res, nargout=1)
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400
        eng.quit()

    resp_dict['exec_time'] = time.time() - start_time
    resp_dict['error'] = False
    resp_dict['data'] = result
    return resp_dict, 200

@main.route('/optimize', methods=['POST'])
@login_required
def optimize():
    start_time = time.time()
    status = 200
    area = request.form.get('area')
    post_data = request.form.to_dict()
    del post_data['area']

    resp_dict = {
        'error': True,
        'data': {},
        'msg' : '',
        'exec_time': -1
    }

    if area == 'sms':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sms_m':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sutami-wlingi':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sengguruh':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
        
    return make_response(jsonify(resp_dict), status, headers)  