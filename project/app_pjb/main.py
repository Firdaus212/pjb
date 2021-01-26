from flask import Blueprint, render_template, make_response, jsonify, request, send_file, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db, eng
import io, time, os, re
from .helpers import *

main = Blueprint('main', __name__)
matlab_file_path_selorejo = r''+os.getcwd()+r'\app_pjb\matlab_files\selorejo'
matlab_file_path_sengguruh = r''+os.getcwd()+r'\app_pjb\matlab_files\sengguruh'
matlab_file_path_sutami = r''+os.getcwd()+r'\app_pjb\matlab_files\sutami'
headers = {"Content-Type": "application/json"}

def generateInsertData(result, area):
    if area == 'sms1':
        return SMS1(**result)
    elif area == 'sms2':
        return SMS2(**result)
    elif area == 'sutami-wlingi':
        return SutamiWlingi(**result)
    elif area == 'sengguruh':
        return Sengguruh(**result)

def checkDataExistInDatabase(input, area):
    found = None
    if area == 'sms1':
        found = SMS1.query.filter_by(**input).first()
    elif area == 'sms2':
        found = SMS2.query.filter_by(**input).first()
    elif area == 'sutami-wlingi':
        found = SutamiWlingi.query.filter_by(**input).first()
    elif area == 'sengguruh':
        found = Sengguruh.query.filter_by(**input).first()
    if found != None:
        return True, found
    return False, found

def converToFloat(inp):
    try:
        for k in inp:
            inp[k] = float(inp[k])
    except Exception as e:
        return False, str(e)
    return True, inp

def performOptimization(resp_dict, post_data, area):
    start_time = time.time()
    conv_status, conv_res = converToFloat(post_data)
    if conv_status == False:
        resp_dict['msg'] = 'Invalid Input'
        return resp_dict, 400
    
    result = {}

    is_data_exist, data_found = checkDataExistInDatabase(conv_res, area)

    if is_data_exist:
        data_found = data_found.__dict__
        del data_found['_sa_instance_state']
        result = data_found
    else:
        try:
            if area == 'sms1':
                eng.addpath(matlab_file_path_selorejo)
                result = eng.sms1(conv_res, nargout=1)
            elif area == 'sms2':
                eng.addpath(matlab_file_path_selorejo)
                result = eng.sms2(conv_res, nargout=1)
            elif area == 'sutami-wlingi':
                eng.addpath(matlab_file_path_sutami)
                result = eng.opt(conv_res, nargout=1)
            elif area == 'sengguruh':
                eng.addpath(matlab_file_path_sengguruh)
                result = eng.opt_senguruh(conv_res, nargout=1)
            # eng.quit()
        except Exception as e:
            resp_dict['msg'] = str(e)
            return resp_dict, 400

        if result != {}:
            result.update(conv_res)
            insert_data = generateInsertData(result, area)
            try:
                db.session.add(insert_data)
                db.session.commit()
            except Exception as e:
                resp_dict['db_insert_error'] = str(e)

    resp_dict['exec_time'] = time.time() - start_time
    resp_dict['error'] = False
    resp_dict['data'] = result
    return resp_dict, 200

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

@main.route('/data/<string:area>')
@login_required
def data(area):
    data = getTableColumnData(area)
    if data == {}:
        return redirect(url_for('main.not_found'))
    return render_template('data.html', data=data)

@main.route('/not_found')
@login_required
def not_found():
    return render_template('404.html', data=data)

@main.route('/table_data/<string:area>', methods=['POST'])
@login_required
def table_data(area):
    draw = int(request.form.get('draw'))
    offset = int(request.form.get('start'))
    limit = int(request.form.get('length'))
    total = 0

    if area == "sms1":
        info = SMS1.query.order_by(SMS1.h0).offset(offset).limit(limit).all()
        total = SMS1.query.count()
    elif area == "sms2":
        info = SMS2.query.order_by(SMS2.h0).offset(offset).limit(limit).all()
        total = SMS2.query.count()
    elif area == "sutami-wlingi":
        info = SutamiWlingi.query.order_by(SutamiWlingi.elevasi_awal).offset(offset).limit(limit).all()
        total = SutamiWlingi.query.count()
    elif area == "sengguruh":
        info = Sengguruh.query.order_by(Sengguruh.inflow_sengguruh).offset(offset).limit(limit).all()
        total = Sengguruh.query.count()

    data = []
    for inf in info:
        item = {}
        for key in inf.__table__.columns.keys():
            if key != 'id':
                item[key] = getattr(inf, key)
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
    if area == 'sms1':
        data = getSMSOpt1PageData()
    elif area == 'sms2':
        data = getSMSOpt2PageData()
    elif area == 'sutami-wlingi':
        data = getSutamiWlingiOptPageData()
    elif area == 'sengguruh':
        data = getSengguruhOptPageData()
    else:
        return redirect(url_for('main.not_found'))
    data['name'] = current_user.name
    return render_template('optimization.html', data=data )

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

    if area == 'sms1':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sms2':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sutami-wlingi':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
    elif area == 'sengguruh':
        resp_dict, status = performOptimization(resp_dict, post_data, area)
        
    return make_response(jsonify(resp_dict), status, headers)  

@main.route('/matlab_files', methods=['GET'])
@login_required
def matlab_files():
    data = {}
    data['title'] = "Matlab Files for Optimization"
    data['selorejo'] = os.listdir(matlab_file_path_selorejo)
    data['sutami-wlingi'] = os.listdir(matlab_file_path_sutami)
    data['sengguruh'] = os.listdir(matlab_file_path_sengguruh)
    return render_template('matlab-data.html', data=data)

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
        return send_file(folder_name + '\\' +filename, as_attachment=True)
    else:
        return make_response(jsonify({'status': 'error', 'msg': 'File not found'}), 400, headers)  

@main.route('/empty_table/<string:area>', methods=['GET'])
def empty_table(area):
    record_deleted = -1
    if area == 'sms1':
        record_deleted = db.session.query(SMS1).delete()
        db.session.commit()
    elif area == 'sms2':
        record_deleted = db.session.query(SMS2).delete()
        db.session.commit()
    elif area == 'sutami-wlingi':
        record_deleted = db.session.query(SutamiWlingi).delete()
        db.session.commit()
    elif area == 'sengguruh':
        record_deleted = db.session.query(Sengguruh).delete()
        db.session.commit()
    
    return make_response(jsonify({'record_deleted': record_deleted}), 200, headers) 