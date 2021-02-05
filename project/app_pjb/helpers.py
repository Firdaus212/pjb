from flask import url_for

# There are some html entities used to display the unit of measurement
# See https://www.freeformatter.com/html-entities.html to get more details 
area_sms_1 = 'sms1'
area_sms_2 = 'sms2'
area_sutami_wlingi_basah = 'sutami-wlingi-basah'
area_sutami_wlingi_kering = 'sutami-wlingi-kering'
area_sengguruh = 'sengguruh'
data_waduk_area_sms = 'sms'
data_waduk_area_sutami = 'sutami-wlingi'
js_optimize_file = 'optimize.js'
js_data_file = 'data.js'
js_data_waduk_file = 'data-waduk.js'
headers = {"Content-Type": "application/json"}


def getSMSOpt1PageData():
    data = {}
    data['title'] = 'Cascade SMS Opt 1'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'h0', 'type': 'number', 'min': 600, 'max': 622, 'step': 0.1, 'unit': 'mdpl'  },
        { 'label': "Inflow Selorejo", 'name': 'q_in', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Outflow Selorejo", 'name': 'Qout', 'type': 'number', 'min': 6.33, 'max': 16.67, 'step': 0.1, 'unit': 'm&sup3;/s' },
        { 'label': "Suplesi Siman", 'name': 'suplesi', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Time Frame", 'name': 't', 'type': 'text', 'unit': 'jam' }
    ]
    data['columns'] = [
        { 'label': 'Inflow', 'id': 'inflow', 'unit': 'm&sup3;/s' },
        { 'label': 'Elevasi Awal', 'id': 'elevasi_awal', 'unit': 'mdpl' },
        { 'label': 'Elevasi Akhir', 'id': 'elevasi_akhir', 'unit': 'mdpl' },
        { 'label': 'Outflow Selorejo', 'id': 'outflow_selorejo', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Selorejo', 'id': 'daya_output_selorejo', 'unit': 'MW' },
        { 'label': 'Energi Output Selorejo', 'id': 'energi_output_selorejo', 'unit': 'MWh' },
        { 'label': 'Inflow Mendalan', 'id': 'inflow_mendalan', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Mendalan #1', 'id': 'daya_output_mendalan_1', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #2', 'id': 'daya_output_mendalan_2', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #3', 'id': 'daya_output_mendalan_3', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #4', 'id': 'daya_output_mendalan_4', 'unit': 'MW' },
        { 'label': 'Total Daya Output Mendalan', 'id': 'total_daya_output_mendalan', 'unit': 'MW' },
        { 'label': 'Energi Output Mendalan', 'id': 'energi_output_mendalan', 'unit': 'MWh' },
        { 'label': 'Suplesi', 'id': 'suplesi', 'unit': 'm&sup3;/s' },
        { 'label': 'Inflow Siman', 'id': 'inflow_siman', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Siman #1', 'id': 'daya_output_siman_1', 'unit': 'MW' },
        { 'label': 'Daya Output Siman #2', 'id': 'daya_output_siman_2', 'unit': 'MW' },
        { 'label': 'Daya Output Siman #3', 'id': 'daya_output_siman_3', 'unit': 'MW' },
        { 'label': 'Total Daya Output Siman', 'id': 'total_daya_output_siman', 'unit': 'MW' },
        { 'label': 'Energi Output Siman', 'id': 'energi_output_siman', 'unit': 'MWh' }
    ]
    data['hidden_input_value'] = area_sms_1
    data['js'] = js_optimize_file
    data['data_url'] = url_for('main.optimize')
    return data

def getSMSOpt2PageData():
    data = {}
    data['title'] = 'Cascade SMS Opt 2'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'h0', 'type': 'number', 'min': 600, 'max': 622, 'step': 0.1, 'unit': 'mdpl' },
        { 'label': "Elevasi Akhir", 'name': 'ht', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Inflow Selorejo", 'name': 'q_in', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Suplesi Siman", 'name': 'suplesi', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Time Frame", 'name': 't', 'type': 'text', 'unit': 'jam' }
    ]
    data['columns'] = [
        { 'label': 'Inflow', 'id': 'inflow', 'unit': 'm&sup3;/s' },
        { 'label': 'Elevasi Awal', 'id': 'elevasi_awal', 'unit': 'mdpl' },
        { 'label': 'Elevasi Akhir', 'id': 'elevasi_akhir', 'unit': 'mdpl' },
        { 'label': 'Outflow Selorejo', 'id': 'outflow_selorejo', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Selorejo', 'id': 'daya_output_selorejo', 'unit': 'MW' },
        { 'label': 'Energi Output Selorejo', 'id': 'energi_output_selorejo', 'unit': 'MWh' },
        { 'label': 'Inflow Mendalan', 'id': 'inflow_mendalan', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Mendalan #1', 'id': 'daya_output_mendalan_1', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #2', 'id': 'daya_output_mendalan_2', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #3', 'id': 'daya_output_mendalan_3', 'unit': 'MW' },
        { 'label': 'Daya Output Mendalan #4', 'id': 'daya_output_mendalan_4', 'unit': 'MW' },
        { 'label': 'Total Daya Output Mendalan', 'id': 'total_daya_output_mendalan', 'unit': 'MW' },
        { 'label': 'Energi Output Mendalan', 'id': 'energi_output_mendalan', 'unit': 'MWh' },
        { 'label': 'Suplesi', 'id': 'suplesi', 'unit': 'm&sup3;/s' },
        { 'label': 'Inflow Siman', 'id': 'inflow_siman', 'unit': 'm&sup3;/s' },
        { 'label': 'Daya Output Siman #1', 'id': 'daya_output_siman_1', 'unit': 'MW' },
        { 'label': 'Daya Output Siman #2', 'id': 'daya_output_siman_2', 'unit': 'MW' },
        { 'label': 'Daya Output Siman #3', 'id': 'daya_output_siman_3', 'unit': 'MW' },
        { 'label': 'Total Daya Output Siman', 'id': 'total_daya_output_siman', 'unit': 'MW' },
        { 'label': 'Energi Output Siman', 'id': 'energi_output_siman', 'unit': 'MWh' }
    ]
    data['hidden_input_value'] = area_sms_2
    data['js'] = js_optimize_file
    data['data_url'] = url_for('main.optimize')
    return data

def getSutamiWlingiWetOptPageData():
    data = {}
    data['title'] = 'Cascade Sutami-Wlingi Basah Opt'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'elevasi_awal', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Elevasi Akhir", 'name': 'elevasi_akhir', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Inflow Minimum", 'name': 'inflow_min', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Inflow Maximum", 'name': 'inflow_max', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Jam Operasi Sutami 1", 'name': 't1', 'type': 'text', 'unit': 'jam' },
        { 'label': "Jam Operasi Sutami 2", 'name': 't2', 'type': 'text', 'unit': 'jam' },
        { 'label': "Jam Operasi Sutami 3", 'name': 't3', 'type': 'text', 'unit': 'jam' },
        { 'label': "Elevasi Awal Wlingi", 'name': 'elevasi_awal_wlingi', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Elevasi Akhir Wlingi", 'name': 'elevasi_akhir_wlingi', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Remain Basin Minimum", 'name': 'r_basin_min', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Remain Basin Maximum", 'name': 'r_basin_max', 'type': 'text', 'unit': 'm&sup3;/s' }
        
    ]
    data['columns'] = [
        { 'label': 'Mean Beban Sutami #1', 'id': 'beban_sutami_1_mean', 'unit': 'MW' },
        { 'label': 'Mean Beban Sutami #2', 'id': 'beban_sutami_2_mean', 'unit': 'MW' },
        { 'label': 'Mean Beban Sutami #3', 'id': 'beban_sutami_3_mean', 'unit': 'MW' },
        { 'label': 'Energi Sutami #1', 'id': 'energi_sutami_1', 'unit': 'MWh' },
        { 'label': 'Energi Sutami #2', 'id': 'energi_sutami_2', 'unit': 'MWh' },
        { 'label': 'Energi Sutami #3', 'id': 'energi_sutami_3', 'unit': 'MWh' },
        { 'label': 'Energi Total Sutami', 'id': 'energi_total_sutami', 'unit': 'MWh' },
        { 'label': 'Beban Wlingi Perjam', 'id': 'beban_wlingi_perjam', 'unit': '' },
        { 'label': 'Energi Wlingi', 'id': 'energi_wlingi', 'unit': 'MW' }
       
    ]
    data['hidden_input_value'] = area_sutami_wlingi_basah
    data['js'] = js_optimize_file
    data['data_url'] = url_for('main.optimize')
    return data

def getSutamiWlingiDryOptPageData():
    data = {}
    data['title'] = 'Cascade Sutami-Wlingi Kering Opt'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'elevasi_awal', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Elevasi Akhir", 'name': 'elevasi_akhir', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Inflow", 'name': 'inflow', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Jam Operasi Sutami 1", 'name': 't1', 'type': 'text', 'unit': 'jam' },
        { 'label': "Jam Operasi Sutami 2", 'name': 't2', 'type': 'text', 'unit': 'jam' },
        { 'label': "Jam Operasi Sutami 3", 'name': 't3', 'type': 'text', 'unit': 'jam' },
        { 'label': "Beban Wlingi", 'name': 'beban_wlingi', 'type': 'text', 'unit': 'MW' },
        { 'label': "Elevasi Real Wlingi", 'name': 'elevasi_real_wlingi', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Elevasi Target Wlingi", 'name': 'elevasi_target_wlingi', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Q Wlingi Yesterday", 'name': 'q_wlingi_yesterday', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Jam Mati Wlingi Kemarin", 'name': 'jam_mati_wlingi_kemarin', 'type': 'text', 'unit': 'jam' }
    ]
    data['columns'] = [
        { 'label': 'Vol Tersedia', 'id': 'vol_tersedia', 'unit': 'm&sup3;' },
        { 'label': 'Vol Used', 'id': 'vol_used', 'unit': 'm&sup3;' },
        { 'label': 'Volume Sisa', 'id': 'volume_sisa', 'unit': 'm&sup3;' },
        { 'label': 'Mean Beban Sutami #1', 'id': 'mean_beban_sutami_1', 'unit': 'MW' },
        { 'label': 'Mean Beban Sutami #2', 'id': 'mean_beban_sutami_2', 'unit': 'MW' },
        { 'label': 'Mean Beban Sutami #3', 'id': 'mean_beban_sutami_3', 'unit': 'MW' },
        { 'label': 'Sum Beban Sutami #1', 'id': 'sum_beban_sutami_1', 'unit': 'MW' },
        { 'label': 'Sum Beban Sutami #2', 'id': 'sum_beban_sutami_2', 'unit': 'MW' },
        { 'label': 'Sum Beban Sutami #3', 'id': 'sum_beban_sutami_3', 'unit': 'MW' },
        { 'label': 'Beban Total Sutami', 'id': 'beban_total_sutami', 'unit': 'MW' },
        { 'label': 'Beban Total Wlingi', 'id': 'beban_total_wlingi', 'unit': 'MW' },
        { 'label': 'Jam Mulai Operasi Today', 'id': 'jam_mulai_operasi_today', 'unit': 'jam' },
        { 'label': 'Jam Mati Operasi Wlingi', 'id': 'jam_mati_operasi_wlingi', 'unit': 'jam' },
        { 'label': 'Waktu Operasi Wlingi', 'id': 'waktu_operasi_wlingi', 'unit': 'jam' },
        { 'label': 'Energi Cascade', 'id': 'energi_cascade', 'unit': 'MWh' },
       
    ]
    data['hidden_input_value'] = area_sutami_wlingi_kering
    data['js'] = js_optimize_file
    data['data_url'] = url_for('main.optimize')
    return data

def getSengguruhOptPageData():
    data = {}
    data['title'] = 'Cascade Sengguruh Opt'
    data['inputs'] = [
        { 'label': "Inflow Min", 'name': 'inflow_min', 'type': 'text', 'unit': 'm&sup3;/s' },
        { 'label': "Inflow Max", 'name': 'inflow_max', 'type': 'text', 'unit': 'm&sup3;/s' }
    ]
    data['columns'] = [
        { 'label': 'Beban Rata-Rata Mesin #1', 'id': 'beban_1_total', 'unit': 'MW' },
        { 'label': 'Beban Rata-Rata Mesin #2', 'id': 'beban_2_total', 'unit': 'MW' },
        { 'label': 'Total Energi Perjam Mesin #1', 'id': 'energi_1', 'unit': 'MWh' },
        { 'label': 'Total Energi Perjam Mesin #2', 'id': 'energi_2', 'unit': 'MWh' },
        { 'label': 'Rata-Rata Debit', 'id': 'q_mean', 'unit': 'm&sup3;/s' }
    ]
    data['hidden_input_value'] = area_sengguruh
    data['js'] = js_optimize_file
    data['data_url'] = url_for('main.optimize')
    return data

def getTableColumnData(area):
    data = {}

    if area == area_sms_1:
        data['title'] = "SMS 1 Optimization Data" 
        data['column'] = [c['id'] for c in getSMSOpt1PageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSMSOpt1PageData()['inputs']]
        data['area'] = area_sms_1
    elif area == area_sms_2:
        data['title'] = "SMS 2 Optimization Data"
        data['column'] = [c['id'] for c in getSMSOpt2PageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSMSOpt2PageData()['inputs']]
        data['area'] = area_sms_2
    elif area == area_sutami_wlingi_basah:
        data['title'] = "Sutami Wlingi Basah Optimization Data"
        data['column'] = [c['id'] for c in getSutamiWlingiOptPageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSutamiWlingiOptPageData()['inputs']]
        data['area'] = area_sutami_wlingi_basah
    elif area == area_sutami_wlingi_kering:
        data['title'] = "Sutami Wlingi Kering Optimization Data"
        data['column'] = [c['id'] for c in getSutamiWlingiOptPageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSutamiWlingiOptPageData()['inputs']]
        data['area'] = area_sutami_wlingi_kering
    elif area == area_sengguruh:
        data['title'] = "Sengguruh Optimization Data"
        data['column'] = [c['id'] for c in getSengguruhOptPageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSengguruhOptPageData()['inputs']]
        data['area'] = area_sengguruh
    
    if data != {}:
        data['column'] = data['col_to_disp'] + list(set(data['column']) - set(data['col_to_disp']))
        data['url'] = url_for('opt_data.table_data', area=area)
        data['empty_url'] = url_for('opt_data.empty_table', area=area)
        if area == area_sengguruh:
            data['col_to_disp'] = data['column']
        data['js'] = js_data_file
    
    return data

def getDataWadukPageData(area):
    data = {}
    data['column'] = ['id', 'H', 'P', 'Q']
    data['js'] = js_data_waduk_file
    data['url'] = url_for('opt_data.get_data_waduk', area=area)
    data['empty_url'] = url_for('opt_data.empty_table', area=area)
    data['area'] = area

    if area == data_waduk_area_sms:
        data['title'] = "Data Waduk SMS"
    elif area == data_waduk_area_sutami:
        data['title'] = "Data Waduk Sutami-Wlingi"
    else:
        data = {}

    return data