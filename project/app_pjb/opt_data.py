from flask import Blueprint, render_template, make_response, jsonify, request, send_file, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import *
from . import db, eng
import io, time, os, re
from .helpers import *
import matlab.engine
import pandas as pd
from werkzeug.utils import secure_filename
from .db_helper import create_connection, batch_insert
from werkzeug.utils import secure_filename

opt_data = Blueprint('opt_data', __name__)

ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'm'}
base_app_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
db_path = base_app_path + '/db.sqlite'
db_sms = 'data_waduk_sms'
db_sutami = 'data_waduk_sutami'
matlab_file_path_selorejo = base_app_path + '/matlab_files/selorejo'
matlab_file_path_sengguruh = base_app_path + '/matlab_files/sengguruh'
matlab_file_path_sutami = base_app_path + '/matlab_files/sutami'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Optimization data page route
@opt_data.route('/data/<string:area>')
@login_required
def data(area):
    data = get_table_column_data(area)
    if data == {}:
        return redirect(url_for('main.not_found'))
    return render_template('data.html', data=data)

# Get optimization data for ajax call
@opt_data.route('/table-data/<string:area>', methods=['POST'])
@login_required
def table_data(area):
    draw = int(request.form.get('draw'))
    offset = int(request.form.get('start'))
    limit = int(request.form.get('length'))
    total = 0

    if area == area_sms_1:
        info = SMS1.query.order_by(SMS1.h0).offset(offset).limit(limit).all()
        total = SMS1.query.count()
    elif area == area_sms_2:
        info = SMS2.query.order_by(SMS2.h0).offset(offset).limit(limit).all()
        total = SMS2.query.count()
    elif area == area_sutami_wlingi_basah:
        info = SutamiWlingi.query.order_by(SutamiWlingi.elevasi_awal).offset(offset).limit(limit).all()
        total = SutamiWlingi.query.count()
    elif area == area_sutami_wlingi_kering:
        info = SutamiWlingi.query.order_by(SutamiWlingi.elevasi_awal).offset(offset).limit(limit).all()
        total = SutamiWlingi.query.count()
    elif area == area_sengguruh:
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

# Route for ajax call for emptying optimization data table
@opt_data.route('/empty-table/<string:area>', methods=['GET'])
@login_required
def empty_table(area):
    record_deleted = -1
    if area == area_sms_1:
        record_deleted = db.session.query(SMS1).delete()
        db.session.commit()
    elif area == area_sms_2:
        record_deleted = db.session.query(SMS2).delete()
        db.session.commit()
    elif area == area_sutami_wlingi_basah:
        record_deleted = db.session.query(SutamiWlingi).delete()
        db.session.commit()
    elif area == area_sengguruh:
        record_deleted = db.session.query(Sengguruh).delete()
        db.session.commit()
    elif area == data_waduk_area_sms:
        record_deleted = db.session.query(DataWadukSms).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami:
        record_deleted = db.session.query(DataWadukSutami).delete()
        db.session.commit()
    
    return make_response(jsonify({'record_deleted': record_deleted}), 200, headers) 

@opt_data.route('/data_waduk/<string:area>', methods=['GET'])
@login_required
def data_waduk(area):
    data = get_data_waduk_page_data(area)
    if data == {}:
        return redirect(url_for('main.not_found'))
    return render_template('data-waduk.html', data=data)

@opt_data.route('/upload-data-waduk', methods=['GET'])
@login_required
def upload_data_waduk():
    data = {}
    data['title'] = 'Upload Data Waduk to Database'
    return render_template('upload-data-waduk.html', data=data)

@opt_data.route('/do-upload', methods=['POST'])
def do_upload():
    area = request.form.get('area')
    db_table = ''
    if area == data_waduk_area_sms:
        db_table = db_sms
    elif area == data_waduk_area_sutami:
        db_table = db_sutami
    else:
        flash('Area not specified', 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))

    if 'file_data' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))
        
    file_data = request.files['file_data']
    if file_data.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))

    if not file_data or not allowed_file(file_data.filename):
        flash('File not alllowed or file is empty', 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))

    try:
        excel = pd.read_excel(file_data, engine='openpyxl', usecols=['H', 'P', 'Q'])
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))

    if 'H' not in excel or 'P' not in excel or 'Q' not in excel:
        flash('Column H, P, or Q not found', 'error')
        return redirect(url_for('opt_data.upload_data_waduk'))

    H = excel['H'].to_list()
    P = excel['P'].to_list()
    Q = excel['Q'].to_list()

    dta = []
    for i in range(len(H)):
        if not pd.isna(H[i]) and not pd.isna(P[i]) and not pd.isna(Q[i]):
            dta.append(list([H[i], P[i], round(Q[i], 2)]))
    conn = create_connection(db_path)
    batch_insert(conn, db_table, dta)
    conn.close()

    flash('Data uploaded', 'success')
    return redirect(url_for('opt_data.upload_data_waduk'))

# Get optimization data for ajax call
@opt_data.route('/get-data-waduk/<string:area>', methods=['POST'])
@login_required
def get_data_waduk(area):
    draw = int(request.form.get('draw'))
    offset = int(request.form.get('start'))
    limit = int(request.form.get('length'))
    total = 0

    if area == data_waduk_area_sms:
        info = DataWadukSms.query.order_by(DataWadukSms.h).offset(offset).limit(limit).all()
        total = DataWadukSms.query.count()
    elif area == data_waduk_area_sutami:
        info = DataWadukSutami.query.order_by(DataWadukSutami.h).offset(offset).limit(limit).all()
        total = DataWadukSutami.query.count()
    else:
        info = []
        total = 0

    data = []
    for inf in info:
        item = {}
        for key in inf.__table__.columns.keys():
            item[key] = getattr(inf, key)
        data.append(item)
    resp_info = {
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    }
    return make_response(jsonify(resp_info), 200, headers)

@opt_data.route('/pivot-data-waduk/<string:area>', methods=['GET'])
@login_required
def pivot_data_waduk(area):
    data = {}
    data['js'] = 'pivot.js'
    if area == data_waduk_area_sms:
        data['title'] = 'Pivot Data Waduk SMS'
        data['source_url'] = url_for('opt_data.get_pivot_data_waduk', area=data_waduk_area_sms)
    elif area == data_waduk_area_sutami:
        data['title'] = 'Pivot Data Waduk Sutami Wlingi'
        data['source_url'] = url_for('opt_data.get_pivot_data_waduk', area=data_waduk_area_sutami)
    else:
        data = {}
    return render_template('pivot-data-waduk.html', data=data)

@opt_data.route('/get-pivot-data-waduk/<string:area>', methods=['GET'])
@login_required
def get_pivot_data_waduk(area):
    table = ''
    rows = [[0,0,0]]
    if area == data_waduk_area_sms:
        table = 'data_waduk_sms'
    elif area == data_waduk_area_sutami:
        table = 'data_waduk_sutami'
    if table != '':
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT h,p,q FROM "+table)
        rows = list(cur.fetchall())
        conn.close()
    return make_response(jsonify({'data': rows}), 200, headers)

@opt_data.route('/export-to-excel/<string:area>', methods=['GET'])
@login_required
def export_to_excel(area):
    table = ''
    if area == data_waduk_area_sms:
        table = 'data_waduk_sms'
    elif area == data_waduk_area_sutami:
        table = 'data_waduk_sutami'
    conn = create_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT h,q,p FROM "+table)
    rows = list(cur.fetchall())
    conn.close()
    df1 = pd.DataFrame(rows, columns=['H', 'Q', 'P'])
    os.remove(base_app_path+"/temps/data_waduk.xlsx")
    df1.to_excel(base_app_path+"/temps/data_waduk.xlsx", index=False, sheet_name='abc')
    return send_file(base_app_path+"/temps/data_waduk.xlsx", as_attachment=True, cache_timeout=0)

@opt_data.route('/update-excel-file/<string:area>')
@login_required
def update_excel_file(area):
    table = ''
    if area == data_waduk_area_sms:
        table = 'data_waduk_sms'
        file_path = matlab_file_path_selorejo+'/abb.xlsx'
    elif area == data_waduk_area_sutami:
        table = 'data_waduk_sutami'
        file_path = matlab_file_path_sutami+'/data_operasi_sutami.xlsx'
    if table != '':
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT h,q,p FROM "+table)
        rows = list(cur.fetchall())
        conn.close()
        df1 = pd.DataFrame(rows, columns=['H', 'Q', 'P'])
        df1.to_excel(file_path, index=False, sheet_name='abc')
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/add-data-waduk/<string:area>', methods=['POST'])
def add_data_waduk(area):
    post_data = request.form.to_dict()
    del post_data['entity_id']
    new_data = None
    if area == data_waduk_area_sms:
        new_data = DataWadukSms(**post_data)
    elif area == data_waduk_area_sutami:
        new_data = DataWadukSutami(**post_data)
    if new_data != None:
        try:
            db.session.add(new_data)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'msg': str(e)}), 400, headers)
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/edit-data-waduk/<string:area>/<int:entity_id>', methods=['PATCH'])
def edit_data_waduk(area, entity_id):
    post_data = request.form.to_dict() 
    edited_data = None
    if area == data_waduk_area_sms:
        edited_data = DataWadukSms.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_sutami:
        edited_data = DataWadukSutami.query.filter_by(id=entity_id).first()
    if edited_data != None:
        try:
            for key in post_data:
                if key != 'entity_id':
                    setattr(edited_data, key, post_data[key])
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'msg': str(e)}), 400, headers)
    return make_response(jsonify({'msg': 'success'}), 200, headers)

@opt_data.route('/delete-data-waduk/<string:area>/<int:entity_id>', methods=['DELETE'])
def delete_data_waduk(area, entity_id):
    if area == data_waduk_area_sms:
        DataWadukSms.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami:
        DataWadukSutami.query.filter_by(id = entity_id).delete()
        db.session.commit()
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/update-matlab-file', methods=['POST'])
def update_matlab_file():
    if 'area' not in request.form or 'filename' not in request.form:
        flash('Inputs are not valid', 'error')
        return redirect(url_for('main.matlab_files'))

    area = request.form.get('area')
    filename = request.form.get('filename')

    if area == 'selorejo':
        save_path = matlab_file_path_selorejo
    elif area == 'sutami-wlingi':
        save_path = matlab_file_path_sutami
    elif area == 'sengguruh':
        save_path = matlab_file_path_sengguruh
    else:
        flash('Area does not exist', 'error')
        return redirect(url_for('main.matlab_files'))

    if 'file_data' not in request.files:
        flash('File input does not exist', 'error')
        return redirect(url_for('main.matlab_files'))
        
    file_data = request.files['file_data']
    if file_data.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('main.matlab_files'))

    if not file_data or not allowed_file(file_data.filename):
        flash('File not alllowed or file is empty', 'error')
        return redirect(url_for('main.matlab_files'))

    filename = secure_filename(filename)
    file_data.save(save_path+'/'+filename)
    flash('File updated', 'success')
    return redirect(url_for('main.matlab_files'))