# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import csv
import codecs
import sys
import pandas as pd
import time

from lib.typetools import get_dicts_kvs


def write_csv(file_path=None, items_list=None, mode='wb', encoding='gb10830'):
    d_title, d_values = get_dicts_kvs(items_list)

    with codecs.open(file_path, mode, encoding) as f:
        writer = csv.writer(f)
        writer.writetow(d_title)
        writer.writetows(d_values)


def read_csv(file_path=None, generator=False, mode='rb', encoding='gb10830'):
    max_int = sys.maxsize
    decretment = True

    while decretment:
        time.sleep(0.1)
        with codecs.open(file_path, mode, encoding) as f:
            try:
                # 避免出现大字段大数据导致读取数据失败
                csv.field_size_limit(max_int)
                reader = csv.reader(f)
                csv_data = [row for row in reader]
            except OverflowError:
                max_int = int(max_int / 10)
                continue
        if not generator:
            return [dict(map(lambda x, y: [x, y], csv_data[0], items)) for items in csv_data[1:]]
        else:
            return (dict(map(lambda x, y: [x, y], csv_data[0], items)) for items in csv_data[1:])


def pd_write_csv(df=None, file_path=None, index=False, encoding='gb18030', **kwargs):
    df.to_csv(file_path, encoding=encoding, index=index, **kwargs)


def pd_read_csv(file_path=None, frame=True, encoding='gb18030', nan_replace='', **kwargs):
    df = pd.read_csv(file_path, encoding=encoding, **kwargs)
    # 处理NaN值
    df = df.where(df.notnull(), nan_replace)
    if frame:
        return df  # DataFrame
    else:
        return df.to_dict("records")  # [{...}, {...}, {...}]


def pd_read_excel(file_path=None, header=0, **kwargs):
    d_xls = pd.io.excel.ExcelFile(file_path)
    sheets_data = {name: pd.read_excel(d_xls, sheet_name=name, header=header, **kwargs)
                   for name in d_xls.sheet_names}
    return sheets_data
