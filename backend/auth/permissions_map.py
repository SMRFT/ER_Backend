


PAGE_MAPPING = {


    '/_b_a_c_k_e_n_d/ER/erbilling/': 'ER-P-ERB',
    '/_b_a_c_k_e_n_d/ER/erregister/': 'ER-P-ERREG',
    '/_b_a_c_k_e_n_d/ER/next-bill-number/': 'ER-P-ERNBN',
    r'^/_b_a_c_k_e_n_d/ER/erregisteredit/?(\?.*)?$': 'ER-P-ERRE',
    '/_b_a_c_k_e_n_d/ER/procedures/': 'ER-P-ERP',
    '/_b_a_c_k_e_n_d/ER/doctors/': 'ER-P-ERD',
    r'^/_b_a_c_k_e_n_d/ER/printbill/?(\?.*)?$': 'ER-P-ERPB',
    r'^/_b_a_c_k_e_n_d/ER/get_er_patients_by_date/?(\?.*)?$': 'ER-P-ERPD',
    
#Admin:

r'^/_b_a_c_k_e_n_d/ER/dashboard/?(\?.*)?$': 'ER-P-ERDSH',
r'^/_b_a_c_k_e_n_d/ER/erreports/?(\?.*)?$': 'ER-P-ERR',



    '/erbilling/': 'ER-P-ERB',
    '/erregister/': 'ER-P-ERREG',
    '/next-bill-number/': 'ER-P-ERNBN',
    '/dashboard/': 'ER-P-ERDSH',
    '/erregisteredit/': 'ER-P-ERRE',
    '/procedures/': 'ER-P-ERP',
    '/doctors/': 'ER-P-ERD',
    '/get_er_patients_by_date/':'ER-P-ERP',
    '/erreports/':'ER-P-ERR'
}



PAGE_ACTION_MAPPING = {
    'xxx': {
        'DELETE':'RWD',
    },
}

GEN_ACTION_MAPPING = {
    'POST': 'RW',
    'PUT': 'RW',
    'PATCH': 'RW',
    'DELETE': 'RW',
    'GET': 'R',
}



