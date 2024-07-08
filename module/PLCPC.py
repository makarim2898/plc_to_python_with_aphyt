'''
# hasil_check_ok() untuk kirim sinyal work ok dan tunggu konfirmasi dari PLC; returning true
# hasil_check_ng() untuk kirim sinyal work ng dan tunggu konfirmasi dari PLC; returning true
# tunggu_trigger_ls() menunggu ls start di colek operator; returning true
# mulai_inspeksi() untuk memberi sinyal ke plc bahwa python sudah mulai inspeksi; returning true
# selesai_inspeksi() untuk memberi sinyal ke plc bahwa python sudah selesai inspeksi; returning true
# tunggu_variabel(myvar, wait_value) untuk menunggu variabel tertentu dengan value tertentu; returning true
# baca_variabel(myvar) untuk membaca variabel; returning value
# tulis_variabel(myvar, myvalue) untuk menulis variabel; returning true

'''
import time
from aphyt import omron
#module time untuk memberi waktu tunggu
#module omron untuk mengakses variabel PLC

#plc ip address pastikan settingan di ethernet pc ip nya sudah sesuai 
plc_ip_address = '192.168.250.1'

#variabel yang akan di baca dan tulis oleh PLC (pastikan variabel nya global dan publish only)
var_ok = 'PY_JUDGE_OK'
feedback_var_ok = 'JUDGE_PYTHON_OK'
var_ng = 'PY_Judge_NG'
feedback_var_ng = 'JUDGE_PYTHON_NG'
ls_trigger = 'LS_START_TO_PYTHON'

mulai = 'WORK_IN_CONFIRMED'
selesai = 'PYTHON_DONE'

#fungsi untuk kirim sinyal deteksi OK
def hasil_check_ok():
    with omron.NSeries(plc_ip_address) as eip_conn:
        eip_conn.write_variable(var_ok, 1)
        eip_conn.write_variable(var_ng, 0)

        #kirim sinyal work ok dan tunggu konfirmasi dari PLC
        feedback = eip_conn.read_variable(feedback_var_ok)
        print(f'tunggu sinyal oke sampai ke PLC, variabel {feedback_var_ok} harus TRUE')
        while feedback != 1:
            feedback = eip_conn.read_variable(feedback_var_ok)
            time.sleep(0.1)
        eip_conn.write_variable(var_ok, 0)
        print(f'sinyal sudah sampai ke plc, variabel {feedback_var_ok} sudah TRUE')
    return True

#fungsi untuk kirim sinyal deteksi NG
def hasil_check_ng():
    with omron.NSeries(plc_ip_address) as eip_conn:
        eip_conn.write_variable(var_ng, 1)
        eip_conn.write_variable(var_ok, 0)

        #kirim sinyal work ng dan tunggu konfirmasi dari PLC
        feedback = eip_conn.read_variable(feedback_var_ng)
        print(f'tunggu sinyal oke sampai ke PLC, variabel {feedback_var_ng} harus TRUE')
        while feedback != 1:
            feedback = eip_conn.read_variable(feedback_var_ng)
            time.sleep(0.1)
        eip_conn.write_variable(var_ng, 0)
        print(f'sinyal sudah sampai ke plc, variabel {feedback_var_ng} sudah TRUE')
    return True

#fungsi untuk tunggu oprator colek LS
#akan di gunkan untuk mengirim hasil deteksi ke PLC
def tunggu_trigger_ls():
    with omron.NSeries(plc_ip_address) as eip_conn:
        data = eip_conn.read_variable(ls_trigger)
        while data != 1:
            data = eip_conn.read_variable(ls_trigger)
            time.sleep(0.1)
    return True

#fungsi untuk memulai program
#di trigger oleh ls work in
def mulai_inspeksi():
    with omron.NSeries(plc_ip_address) as eip_conn:
        #tunggu LS work in ke colek saat masukin work
        while eip_conn.read_variable(mulai) != 1:
            time.sleep(0.1)
        eip_conn.write_variable(var_ng, 0)
        eip_conn.write_variable(var_ok, 0)
        eip_conn.write_variable(selesai, 0)
        return True


#fungsi untuk menandai sudah selesai scanning dan kirim data
def selesai_inspeksi():
    #saat deteksi sudah selesai kirim data sudah oke panggil program ini untuk reset start scanning
    with omron.NSeries(plc_ip_address) as eip_conn:
        eip_conn.write_variable(var_ng, 0)
        eip_conn.write_variable(var_ok, 0)
        eip_conn.write_variable(selesai, 1)
        while eip_conn.read_variable(mulai) != 0:
            time.sleep(0.1)
        eip_conn.write_variable(selesai, 0)



def tunggu_variabel(myvar, wait_value):
    #myvar = variabel yang ingin di tunggu
    #wait_value = value yang ingin di tunggu
    print(f'waiting {myvar} to be {wait_value}')
    with omron.NSeries(plc_ip_address) as eip_conn:
        while eip_conn.read_variable(myvar) != wait_value:
            time.sleep(0.1)
    return True

def baca_variabel(myvar):
    data = 0
    print(f'membaca variabel {myvar}')
    with omron.NSeries(plc_ip_address) as eip_conn:
        data = eip_conn.read_variable(myvar)
        time.sleep(0.1)
    print(f'variabel {myvar} = {data}')
    return data

def tulis_variabel(myvar, value):
    print(f'tulis variabel {myvar} = {value}')
    with omron.NSeries(plc_ip_address) as eip_conn:
        while eip_conn.read_variable(myvar) != value:
            eip_conn.write_variable(myvar, value)
            time.sleep(0.1)
    print(f'sudah di tulis variabel {myvar} = {value}')
    return True

def test_modul_crot():
    print('ini modul plc python')
    return True