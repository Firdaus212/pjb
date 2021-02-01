from flask import url_for

# There are some html entities used to display the unit of measurement
# See https://www.freeformatter.com/html-entities.html to get more details 

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
    data['hidden_input_value'] = 'sms1'
    data['js'] = 'optimize.js'
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
    data['hidden_input_value'] = 'sms2'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getSutamiWlingiOptPageData():
    data = {}
    data['title'] = 'Cascade Sutami-Wlingi Opt'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'elevasi_awal', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Elevasi Akhir", 'name': 'elevasi_akhir', 'type': 'text', 'unit': 'mdpl' },
        { 'label': "Inflow", 'name': 'inflow', 'type': 'text', 'unit': 'm&sup3;/s' },
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
    data['hidden_input_value'] = 'sutami-wlingi'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getSengguruhOptPageData():
    data = {}
    data['title'] = 'Cascade Sengguruh Opt'
    data['inputs'] = [
        { 'label': "Inflow Sengguruh", 'name': 'inflow_sengguruh', 'type': 'text', 'unit': 'm&sup3;/s' }
    ]
    data['columns'] = [
        { 'label': 'Daya Output Sengguruh #1', 'id': 'beban_1', 'unit': 'MW' },
        { 'label': 'Daya Output Sengguruh #2', 'id': 'beban_2', 'unit': 'MW' },
        { 'label': 'Energi Output Sengguruh #1', 'id': 'energi_1', 'unit': 'MWh' },
        { 'label': 'Energi Output Sengguruh #2', 'id': 'energi_2', 'unit': 'MWh' },
        { 'label': 'Total Daya Output Sengguruh', 'id': 'total_beban', 'unit': 'MW' },
        { 'label': 'Total Energi Output Sengguruh', 'id': 'total_energi', 'unit': 'MWh' }
    ]
    data['hidden_input_value'] = 'sengguruh'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getTableColumnData(area):
    data = {}

    if area == "sms1":
        data['title'] = "SMS 1 Optimization Data" 
        data['column'] = [c['id'] for c in getSMSOpt1PageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSMSOpt1PageData()['inputs']]
        data['area'] = 'sms1'
    elif area == "sms2":
        data['title'] = "SMS 2 Optimization Data"
        data['column'] = [c['id'] for c in getSMSOpt2PageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSMSOpt2PageData()['inputs']]
        data['area'] = 'sms2'
    elif area == "sutami-wlingi":
        data['title'] = "Sutami Wlingi 1 Optimization Data"
        data['column'] = [c['id'] for c in getSutamiWlingiOptPageData()['columns']]
        data['col_to_disp'] = [c['name'] for c in getSutamiWlingiOptPageData()['inputs']]
        data['area'] = 'sutami-wlingi'
    elif area == "sengguruh":
        data['title'] = "Sengguruh 1 Optimization Data"
        data['column'] = [c['id'] for c in getSengguruhOptPageData()['columns']]
        # data['col_to_disp'] = [c['name'] for c in getSengguruhOptPageData()['inputs']]
        data['col_to_disp'] = [c['name'] for c in getSengguruhOptPageData()['inputs']]
        data['area'] = 'sengguruh'
    
    if data != {}:
        data['column'] = data['col_to_disp'] + list(set(data['column']) - set(data['col_to_disp']))
        if area == "sengguruh":
            data['col_to_disp'] = data['column']
        data['js'] = 'data.js'
    return data

def getTableDataPageData():
    data = {}
    data['column'] = ['inflow_selorejo', 'elevasi_awal', 'elevasi_target', 'elevasi_akhir', 'outflow_selorejo', 'mw_selorejo', 'mwh_selorejo', 
    'limpas', 'inflow_outflow_mendalan', 'mw_mendalan_1', 'mw_mendalan_2', 'mw_mendalan_3', 'mw_mendalan_4', 'mw_mendalan', 'mwh_mendalan', 
    'suplesi_siman', 'inflow_siman', 'mw_siman_1', 'mw_siman_2', 'mw_siman_3', 'mw_siman', 'mwh_siman']
    data['col_to_disp'] = ['inflow_selorejo', 'elevasi_awal', 'elevasi_target', 'elevasi_akhir', 'outflow_selorejo','mw_selorejo', 'mwh_selorejo', 
    'limpas']
    data['js'] = 'data.js'
    return data