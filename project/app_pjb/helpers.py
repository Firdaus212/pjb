from flask import url_for

def getSMSOpt1PageData():
    data = {}
    data['title'] = 'Cascade SMS Opt 1'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'h0', 'type': 'text' },
        { 'label': "Inflow Selorejo", 'name': 'q_in', 'type': 'text' },
        { 'label': "Outflow Selorejo", 'name': 'Qout', 'type': 'text' },
        { 'label': "Suplesi Siman", 'name': 'suplesi', 'type': 'text' },
        { 'label': "Time Frame", 'name': 't', 'type': 'text' }
    ]
    data['columns'] = [
        { 'label': 'Inflow', 'id': 'inflow' },
        { 'label': 'Elevasi Awal', 'id': 'elevasi_awal' },
        { 'label': 'Elevasi Akhir', 'id': 'elevasi_akhir' },
        { 'label': 'Outflow Selorejo', 'id': 'outflow_selorejo' },
        { 'label': 'Daya Output Selorejo', 'id': 'daya_output_selorejo' },
        { 'label': 'Energi Output Selorejo', 'id': 'energi_output_selorejo' },
        { 'label': 'Inflow Mendalan', 'id': 'inflow_mendalan' },
        { 'label': 'Daya Output Mendalan #1', 'id': 'daya_output_mendalan_1' },
        { 'label': 'Daya Output Mendalan #2', 'id': 'daya_output_mendalan_2' },
        { 'label': 'Daya Output Mendalan #3', 'id': 'daya_output_mendalan_3' },
        { 'label': 'Daya Output Mendalan #4', 'id': 'daya_output_mendalan_4' },
        { 'label': 'Total Daya Output Mendalan', 'id': 'total_daya_output_mendalan' },
        { 'label': 'Energi Output Mendalan', 'id': 'energi_output_mendalan' },
        { 'label': 'Suplesi', 'id': 'suplesi' },
        { 'label': 'Inflow Siman', 'id': 'inflow_siman' },
        { 'label': 'Daya Output Siman #1', 'id': 'daya_output_siman_1' },
        { 'label': 'Daya Output Siman #2', 'id': 'daya_output_siman_2' },
        { 'label': 'Daya Output Siman #3', 'id': 'daya_output_siman_3' },
        { 'label': 'Total Daya Output Siman', 'id': 'total_daya_output_siman' },
        { 'label': 'Energi Output Siman', 'id': 'energi_output_siman' }
    ]
    data['hidden_input_value'] = 'sms'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getSMSOpt2PageData():
    data = {}
    data['title'] = 'Cascade SMS Opt 2'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'h0', 'type': 'text' },
        { 'label': "Elevasi Akhir", 'name': 'ht', 'type': 'text' },
        { 'label': "Inflow Selorejo", 'name': 'q_in', 'type': 'text' },
        { 'label': "Suplesi Siman", 'name': 'suplesi', 'type': 'text' },
        { 'label': "Time Frame", 'name': 't', 'type': 'text' }
    ]
    data['columns'] = [
        { 'label': 'Inflow', 'id': 'inflow' },
        { 'label': 'Elevasi Awal', 'id': 'elevasi_awal' },
        { 'label': 'Elevasi Akhir', 'id': 'elevasi_akhir' },
        { 'label': 'Outflow Selorejo', 'id': 'outflow_selorejo' },
        { 'label': 'Daya Output Selorejo', 'id': 'daya_output_selorejo' },
        { 'label': 'Energi Output Selorejo', 'id': 'energi_output_selorejo' },
        { 'label': 'Inflow Mendalan', 'id': 'inflow_mendalan' },
        { 'label': 'Daya Output Mendalan #1', 'id': 'daya_output_mendalan_1' },
        { 'label': 'Daya Output Mendalan #2', 'id': 'daya_output_mendalan_2' },
        { 'label': 'Daya Output Mendalan #3', 'id': 'daya_output_mendalan_3' },
        { 'label': 'Daya Output Mendalan #4', 'id': 'daya_output_mendalan_4' },
        { 'label': 'Total Daya Output Mendalan', 'id': 'total_daya_output_mendalan' },
        { 'label': 'Energi Output Mendalan', 'id': 'energi_output_mendalan' },
        { 'label': 'Suplesi', 'id': 'suplesi' },
        { 'label': 'Inflow Siman', 'id': 'inflow_siman' },
        { 'label': 'Daya Output Siman #1', 'id': 'daya_output_siman_1' },
        { 'label': 'Daya Output Siman #2', 'id': 'daya_output_siman_2' },
        { 'label': 'Daya Output Siman #3', 'id': 'daya_output_siman_3' },
        { 'label': 'Total Daya Output Siman', 'id': 'total_daya_output_siman' },
        { 'label': 'Energi Output Siman', 'id': 'energi_output_siman' }
    ]
    data['hidden_input_value'] = 'sms_m'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getSutamiWlingiOptPageData():
    data = {}
    data['title'] = 'Cascade Sutami-Wlingi Opt'
    data['inputs'] = [
        { 'label': "Elevasi Awal", 'name': 'elevasi_awal', 'type': 'text' },
        { 'label': "Elevasi Akhir", 'name': 'elevasi_akhir', 'type': 'text' },
        { 'label': "Inflow", 'name': 'inflow', 'type': 'text' },
        { 'label': "Beban Wlingi", 'name': 'beban_wlingi', 'type': 'text' },
        { 'label': "Elevasi Real Wlingi", 'name': 'elevasi_real_wlingi', 'type': 'text' },
        { 'label': "Elevasi Target Wlingi", 'name': 'elevasi_target_wlingi', 'type': 'text' },
        { 'label': "Q Wlingi Yesterday", 'name': 'q_wlingi_yesterday', 'type': 'text' },
        { 'label': "Jam Mati Wlingi Kemarin", 'name': 'jam_mati_wlingi_kemarin', 'type': 'text' }
    ]
    data['columns'] = [
        { 'label': 'Vol Tersedia', 'id': 'vol_tersedia' },
        { 'label': 'Vol Used', 'id': 'vol_used' },
        { 'label': 'Volume Sisa', 'id': 'volume_sisa' },
        { 'label': 'Mean Beban Sutami #1', 'id': 'mean_beban_sutami_1' },
        { 'label': 'Mean Beban Sutami #2', 'id': 'mean_beban_sutami_2' },
        { 'label': 'Mean Beban Sutami #3', 'id': 'mean_beban_sutami_3' },
        { 'label': 'Sum Beban Sutami #1', 'id': 'sum_beban_sutami_1' },
        { 'label': 'Sum Beban Sutami #2', 'id': 'sum_beban_sutami_2' },
        { 'label': 'Sum Beban Sutami #3', 'id': 'sum_beban_sutami_3' },
        { 'label': 'Beban Total Sutami', 'id': 'beban_total_sutami' },
        { 'label': 'Beban Total Wlingi', 'id': 'beban_total_wlingi' },
        { 'label': 'Jam Mulai Operasi Today', 'id': 'jam_mulai_operasi_today' },
        { 'label': 'Jam Mati Operasi Wlingi', 'id': 'jam_mati_operasi_wlingi' },
        { 'label': 'Waktu Operasi Wlingi', 'id': 'waktu_operasi_wlingi' },
        { 'label': 'Energi Cascade', 'id': 'energi_cascade' },
       
    ]
    data['hidden_input_value'] = 'sutami-wlingi'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
    return data

def getSengguruhOptPageData():
    data = {}
    data['title'] = 'Cascade Sengguruh Opt'
    data['inputs'] = [
        { 'label': "Inflow Sengguruh", 'name': 'inflow_sengguruh', 'type': 'text' }
    ]
    data['columns'] = [
        { 'label': 'Daya Output Sengguruh #1', 'id': 'beban_1' },
        { 'label': 'Daya Output Sengguruh #2', 'id': 'beban_2' },
        { 'label': 'Energi Output Sengguruh #1', 'id': 'energi_1' },
        { 'label': 'Energi Output Sengguruh #2', 'id': 'energi_2' },
        { 'label': 'Total Daya Output Sengguruh', 'id': 'total_beban' },
        { 'label': 'Total Energi Output Sengguruh', 'id': 'total_energi' }
    ]
    data['hidden_input_value'] = 'sengguruh'
    data['js'] = 'optimize.js'
    data['data_url'] = url_for('main.optimize')
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