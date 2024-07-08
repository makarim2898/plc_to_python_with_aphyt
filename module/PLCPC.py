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
    with omron.NSeries('192.168.250.1') as eip_conn:
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
    with omron.NSeries('192.168.250.1') as eip_conn:
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
    with omron.NSeries('192.168.250.1') as eip_conn:
        data = eip_conn.read_variable(ls_trigger)
        while data != 1:
            data = eip_conn.read_variable(ls_trigger)
            time.sleep(0.1)
    return True

#fungsi untuk memulai program
#di trigger oleh ls work in
def mulai_program():
    with omron.NSeries('192.168.250.1') as eip_conn:
        #tunggu LS work in ke colek saat masukin work
        while eip_conn.read_variable(mulai) != 1:
            time.sleep(0.1)
        eip_conn.write_variable(var_ng, 0)
        eip_conn.write_variable(var_ok, 0)
        eip_conn.write_variable(selesai, 0)
        return True


#fungsi untuk menandai sudah selesai scanning dan kirim data
def sudah_selesai():
    #saat deteksi sudah selesai kirim data sudah oke panggil program ini untuk reset start scanning
    with omron.NSeries('192.168.250.1') as eip_conn:
        eip_conn.write_variable(var_ng, 0)
        eip_conn.write_variable(var_ok, 0)
        eip_conn.write_variable(selesai, 1)
        while eip_conn.read_variable(mulai) != 0:
            time.sleep(0.1)
        eip_conn.write_variable(selesai, 0)



def tunggu_variabel(myvar, wait_value):
    #myvar = variabel yang ingin di tunggu
    #wait_value = value yang ingin di tunggu
    #myvar bertipe string, dan wait_value bertipe biner 0 dan 1
    while myvar != wait_value:
        time.sleep(0.1)
    return True