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
from .permission import admin_authority

opt_data = Blueprint('opt_data', __name__)

ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'm'}
base_app_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
db_path = base_app_path + '/db.sqlite'
db_selorejo = 'data_waduk_selorejo'
db_mendalan = 'data_waduk_mendalan'
db_siman = 'data_waduk_siman'
db_sutami = 'data_waduk_sutami'
db_wlingi = 'data_waduk_wlingi'
db_sutami2 = 'data_waduk_sutami_operasi'
matlab_file_path_selorejo = base_app_path + '/matlab_files/selorejo'
matlab_file_path_sengguruh = base_app_path + '/matlab_files/sengguruh'
matlab_file_path_sutami = base_app_path + '/matlab_files/sutami'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Optimization data page route
@opt_data.route('/data/<string:area>')
@login_required
@admin_authority
def data(area):
    data = get_table_column_data(area)
    if data == {}:
        return redirect(url_for('main.not_found'))
    return render_template('data.html', data=data)

# Get optimization data for ajax call
@opt_data.route('/table-data/<string:area>', methods=['POST'])
@login_required
@admin_authority
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
@admin_authority
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
    elif area == data_waduk_area_selorejo:
        record_deleted = db.session.query(DataWadukSelorejo).delete()
        db.session.commit()
    elif area == data_waduk_area_mendalan:
        record_deleted = db.session.query(DataWadukMendalan).delete()
        db.session.commit()
    elif area == data_waduk_area_siman:
        record_deleted = db.session.query(DataWadukSiman).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami:
        record_deleted = db.session.query(DataWadukSutami).delete()
        db.session.commit()
    elif area == data_waduk_area_wlingi:
        record_deleted = db.session.query(DataWadukWlingi).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami2:
        record_deleted = db.session.query(DataWadukSutamiOperasi).delete()
        db.session.commit()
    
    return make_response(jsonify({'record_deleted': record_deleted}), 200, headers) 

@opt_data.route('/data_waduk/<string:area>', methods=['GET'])
@login_required
@admin_authority
def data_waduk(area):
    data = get_data_waduk_page_data(area)
    if data == {}:
        return redirect(url_for('main.not_found'))
    return render_template('data-waduk.html', data=data)

@opt_data.route('/upload-data-waduk', methods=['GET'])
@login_required
@admin_authority
def upload_data_waduk():
    data = {}
    data['title'] = 'Upload Data Waduk to Database'
    return render_template('upload-data-waduk.html', data=data)

@opt_data.route('/do-upload', methods=['POST'])
@login_required
@admin_authority
def do_upload():
    area = request.form.get('area')
    db_table = ''
    if area == data_waduk_area_selorejo:
        db_table = db_selorejo
    elif area == data_waduk_area_mendalan:
        db_table = db_mendalan
    elif area == data_waduk_area_siman:
        db_table = db_siman
    elif area == data_waduk_area_sutami:
        db_table = db_sutami
    elif area == data_waduk_area_wlingi:
        db_table = db_wlingi
    elif area == data_waduk_area_sutami2:
        db_table = db_sutami2
    else:
        flash('Area not specified', 'error')
        return redirect(url_for('opt_data.data_waduk', area=area))

    if 'file_data' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('opt_data.data_waduk', area=area))
        
    file_data = request.files['file_data']
    if file_data.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('opt_data.data_waduk', area=area))

    if not file_data or not allowed_file(file_data.filename):
        flash('File not alllowed or file is empty', 'error')
        return redirect(url_for('opt_data.data_waduk', area=area))

    col = get_data_waduk_page_data(area)
    try:
        excel = pd.read_excel(file_data, engine='openpyxl', usecols=col['column'][1:])
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('opt_data.data_waduk', area=area))

    excel_col = {}
    for c in col['column']:
        if c != 'id':
            if c not in excel:
                flash('Column not found', 'error')
                return redirect(url_for('opt_data.data_waduk', area=area))
            else:
                excel_col[c] = excel[c].to_list()

    dta = []
    for i in range(len(excel_col[col['column'][1]])):
        item = []
        for c in col['column'][1:]:
            if not pd.isna(excel_col[c][i]):
                item.append(round(excel_col[c][i], 2))
            else:
                item.append(None) 
        dta.append(item)    
    conn = create_connection(db_path)
    batch_insert(conn, db_table, col['column'][1:], dta)
    conn.close()

    flash('Data uploaded', 'success')
    return redirect(url_for('opt_data.data_waduk', area=area))

# Get optimization data for ajax call
@opt_data.route('/get-data-waduk/<string:area>', methods=['POST'])
@login_required
@admin_authority
def get_data_waduk(area):
    draw = int(request.form.get('draw'))
    offset = int(request.form.get('start'))
    limit = int(request.form.get('length'))
    total = 0

    if area == data_waduk_area_selorejo:
        info = DataWadukSelorejo.query.order_by(DataWadukSelorejo.h).offset(offset).limit(limit).all()
        total = DataWadukSelorejo.query.count()
    elif area == data_waduk_area_mendalan:
        info = DataWadukMendalan.query.order_by(DataWadukMendalan.id).offset(offset).limit(limit).all()
        total = DataWadukMendalan.query.count()
    elif area == data_waduk_area_siman:
        info = DataWadukSiman.query.order_by(DataWadukSiman.id).offset(offset).limit(limit).all()
        total = DataWadukSiman.query.count()
    elif area == data_waduk_area_sutami:
        info = DataWadukSutami.query.order_by(DataWadukSutami.elevation).offset(offset).limit(limit).all()
        total = DataWadukSutami.query.count()
    elif area == data_waduk_area_wlingi:
        info = DataWadukWlingi.query.order_by(DataWadukWlingi.elevation).offset(offset).limit(limit).all()
        total = DataWadukWlingi.query.count()
    elif area == data_waduk_area_sutami2:
        info = DataWadukSutamiOperasi.query.order_by(DataWadukSutamiOperasi.h).offset(offset).limit(limit).all()
        total = DataWadukSutamiOperasi.query.count()
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
@admin_authority
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
@admin_authority
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
@admin_authority
def export_to_excel(area):
    data_waduk = get_data_waduk_page_data(area)
    conn = create_connection(db_path)
    cur = conn.cursor()
    str_select = ",".join(data_waduk['column'][1:])
    if area == 'selorejo' or area == 'sutami':
        str_select = "h,q,p"
    cur.execute("SELECT "+str_select+" FROM "+data_waduk['table'])
    rows = list(cur.fetchall())
    conn.close()
    arr_col = [c for c in data_waduk['column'][1:]]
    if area == 'selorejo' or area == 'sutami':
        arr_col = ['H', 'Q', 'P']
    df1 = pd.DataFrame(rows, columns=arr_col)
    if os.path.exists(base_app_path+"/temps/"+area+".xlsx"):
        os.remove(base_app_path+"/temps/"+area+".xlsx")
    df1.to_excel(base_app_path+"/temps/"+area+".xlsx", index=False, sheet_name=area.title())
    return send_file(base_app_path+"/temps/"+area+".xlsx", as_attachment=True, cache_timeout=0)

@opt_data.route('/update-excel-file/<string:area>')
@login_required
@admin_authority
def update_excel_file(area):
    file_path = ''
    if area == data_waduk_area_selorejo:
        file_path = matlab_file_path_selorejo+'/Performance Selorejo.xlsx'
    elif area == data_waduk_area_mendalan:
        file_path = matlab_file_path_selorejo+'/Performance Mendalan.xlsx'
    elif area == data_waduk_area_siman:
        file_path = matlab_file_path_selorejo+'/Performance Siman.xlsx'
    elif area == data_waduk_area_sutami:
        file_path = matlab_file_path_sutami+'/data_waduk_sutami.xlsx'
    elif area == data_waduk_area_wlingi:
        file_path = matlab_file_path_sutami+'/data_waduk_wlingi.xlsx'
    elif area == data_waduk_area_sutami2:
        file_path = matlab_file_path_sutami+'/data_operasi_sutami.xlsx'

    if file_path != '':
        data_waduk = get_data_waduk_page_data(area)
        str_select = ",".join(data_waduk['column'][1:])
        arr_col = [c for c in data_waduk['column'][1:]]
        if area == 'selorejo' or area == 'sutami':
            str_select = "h,q,p"
            arr_col = ['H', 'Q', 'P']
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT "+str_select+" FROM "+data_waduk['table'])
        rows = list(cur.fetchall())
        conn.close()
        df1 = pd.DataFrame(rows, columns=arr_col)
        df1.to_excel(file_path, index=False, sheet_name=area.title())
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/add-data-waduk/<string:area>', methods=['POST'])
@login_required
@admin_authority
def add_data_waduk(area):
    post_data = request.form.to_dict()
    del post_data['entity_id']
    new_data = None
    if area == data_waduk_area_selorejo:
        new_data = DataWadukSelorejo(**post_data)
    elif area == data_waduk_area_mendalan:
        new_data = DataWadukMendalan(**post_data)
    elif area == data_waduk_area_siman:
        new_data = DataWadukSiman(**post_data)
    elif area == data_waduk_area_sutami:
        new_data = DataWadukSutami(**post_data)
    elif area == data_waduk_area_wlingi:
        new_data = DataWadukWlingi(**post_data)
    elif area == data_waduk_area_sutami2:
        new_data = DataWadukSutamiOperasi(**post_data)
    if new_data != None:
        try:
            db.session.add(new_data)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'msg': str(e)}), 400, headers)
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/edit-data-waduk/<string:area>/<int:entity_id>', methods=['PATCH'])
@login_required
@admin_authority
def edit_data_waduk(area, entity_id):
    post_data = request.form.to_dict() 
    edited_data = None
    if area == data_waduk_area_selorejo:
        edited_data = DataWadukSelorejo.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_mendalan:
        edited_data = DataWadukMendalan.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_siman:
        edited_data = DataWadukSiman.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_sutami:
        edited_data = DataWadukSutami.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_wlingi:
        edited_data = DataWadukWlingi.query.filter_by(id=entity_id).first()
    elif area == data_waduk_area_sutami2:
        edited_data = DataWadukSutamiOperasi.query.filter_by(id=entity_id).first()
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
@login_required
@admin_authority
def delete_data_waduk(area, entity_id):
    if area == data_waduk_area_selorejo:
        DataWadukSelorejo.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_mendalan:
        DataWadukMendalan.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_siman:
        DataWadukSiman.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami:
        DataWadukSutami.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_wlingi:
        DataWadukWlingi.query.filter_by(id = entity_id).delete()
        db.session.commit()
    elif area == data_waduk_area_sutami2:
        DataWadukSutamiOperasi.query.filter_by(id = entity_id).delete()
        db.session.commit()
    return make_response(jsonify({'data': 'success'}), 200, headers)

@opt_data.route('/update-matlab-file', methods=['POST'])
@login_required
@admin_authority
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
    file_data.save(save_path+'/'+filename.replace('_', ' '))
    flash('File updated', 'success')
    return redirect(url_for('main.matlab_files'))

@opt_data.route('/data-waduk-model/<string:area>', methods=['GET'])
@login_required
@admin_authority
def data_waduk_model(area):
    resp_dict = {
        'error': True,
        'data': {},
        'msg' : ''
    }
    try:
        if area == data_waduk_area_selorejo:
            eng.addpath(matlab_file_path_selorejo)
            result = eng.modelselorejo()
        elif area == data_waduk_area_mendalan:
            eng.addpath(matlab_file_path_selorejo)
            result = eng.modelmendalan()
        elif area == data_waduk_area_siman:
            eng.addpath(matlab_file_path_selorejo)
            result = eng.modelsiman()
        elif area == data_waduk_area_sutami:
            eng.addpath(matlab_file_path_sutami)
            result = eng.modelsutami()
        elif area == data_waduk_area_wlingi:
            eng.addpath(matlab_file_path_sutami)
            result = eng.modelwlingi()
        elif area == data_waduk_area_sutami2:
            eng.addpath(matlab_file_path_sutami)
            result = eng.modelsutami2()
    except Exception as e:
        resp_dict['msg'] = str(e)
        return make_response(jsonify(resp_dict), 400, headers) 
    for key in result:
        for i in range(len(result[key]['coeffvalues'])):
            result[key]['coeffvalues'][i] = "{:.3e}".format(result[key]['coeffvalues'][i])
    resp_dict['error'] = False
    resp_dict['data'] = result
    return make_response(jsonify(resp_dict), 200, headers)  