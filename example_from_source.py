import time
from aphyt import omron
#PY_JUDGE_OK untuk kirim sinyal work OK ke PLC 1 artinya OK, 0 artinya tidak OK
#PY_Judge_NG untuk kirim sinyal work NG ke PLC 1 artinya NG, 0 artinya tidak NG
#dua variabel diatas tidak boleh on bersamaan, kalau off semua akan di anggap tidak ada hasil scann
#JUDGE_PYTHON_OK untuk membaca feedback sinyal ok dari PLC 1 artinya OK, 0 artinya tidak OK
#JUDGE_PYTHON_NG untuk membaca feedback sinyal NG dari PLC 1 artinya NG, 0 artinya tidak NG
#LS_START_TO_PYTHON untuk membaca status colek ls mesin ke PLC 1 artinya LS_ON, 0 artinya LS_OFF

#sample program read and write variabel di plc
if __name__ == '__main__':
    with omron.NSeries('192.168.250.1') as eip_conn:
        for i in range(10):
            eip_conn.write_variable('PY_JUDGE_OK', 1) 
            print(eip_conn.read_variable('JUDGE_PYTHON_OK'))
            time.sleep(1)
            eip_conn.write_variable('PY_JUDGE_OK', 0)
            print(eip_conn.read_variable('JUDGE_PYTHON_OK'))
            time.sleep(1)