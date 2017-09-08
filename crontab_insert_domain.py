#coding:utf-8

import shutil
import SqlManager
import datetime




if __name__ == '__main__':
    now = datetime.datetime.now()
    src_file = '/root/edm/result.txt'
    dst_file = '/root/edm/result.txt.%s'%(now.strftime('%Y%m%d%H'))
    shutil.move(src_file,dst_file)
    sql_manager = SqlManager.Sqlmanger()
    with open(dst_file) as f:
        all_domain_set = set()
        for line in f.readlines():
            line = line.strip()
            all_domain_set.add(line)
        sql_manager.insert_top_domains(all_domain_set)

    sql_manager.commit()


