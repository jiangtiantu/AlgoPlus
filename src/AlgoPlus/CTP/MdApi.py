# encoding:utf-8

# AlgoPlus量化投资开源框架
# 微信公众号：AlgoPlus
# 官网：http://algo.plus

import os
import csv
from AlgoPlus.CTP.MdApiBase import MdApiBase
from AlgoPlus.CTP.FutureAccount import FutureAccount
from AlgoPlus.utils.base_field import to_str, to_bytes
from AlgoPlus.CTP.ApiStruct import DepthMarketDataField


class MdApi(MdApiBase):
    def __init__(self, broker_id, md_server, investor_id, password, app_id, auth_code, instrument_id_list, md_queue_list=None,
                 page_dir='', using_udp=False, multicast=False):
        pass

    def OnRtnDepthMarketData(self, pDepthMarketData):
        # 将行情放入共享队列
        for md_queue in self.md_queue_list:
            md_queue.put(pDepthMarketData)


class MdRecorder(MdApiBase):
    def __init__(self, broker_id, md_server, investor_id, password, app_id, auth_code, instrument_id_list, md_queue_list=None
                 , page_dir='', using_udp=False, multicast=False):
        pass

    def init_extra(self):
        self.csv_file_dict = {}
        self.csv_writer = {}
        # 深度行情结构体字段名列表
        header = list(DepthMarketDataField().to_dict())
        for instrument_id in self.instrument_id_list:
            instrument_id = to_str(instrument_id)
            # file object
            file_dir = os.path.join(self.page_dir, f'{instrument_id}-{to_str(self.GetTradingDay())}.csv')
            self.csv_file_dict[instrument_id] = open(file_dir, 'a', newline='')
            # writer object
            self.csv_writer[instrument_id] = csv.DictWriter(self.csv_file_dict[instrument_id], header)
            # 写入表头
            self.csv_writer[instrument_id].writeheader()
            self.csv_file_dict[instrument_id].flush()

    # ///深度行情通知
    def OnRtnDepthMarketData(self, pDepthMarketData):
        try:
            for key in pDepthMarketData.keys():
                pDepthMarketData[key] = to_str(pDepthMarketData[key])
            # 写入行情
            self.csv_writer[pDepthMarketData['InstrumentID']].writerow(pDepthMarketData)
            # 刷新缓冲区
            self.csv_file_dict[pDepthMarketData['InstrumentID']].flush()
        except Exception as err_msg:
            self.write_log(err_msg, pDepthMarketData)


def run_api(api_cls, account, md_queue_list=None):
    if isinstance(account, FutureAccount):
        tick_engine = api_cls(
            account.broker_id,
            account.server_dict['MDServer'],
            account.investor_id,
            account.password,
            account.app_id,
            account.auth_code,
            account.instrument_id_list,
            md_queue_list,
            account.md_page_dir
        )
        tick_engine.Join()


def run_mdapi(account, md_queue_list):
    run_api(MdApi, account, md_queue_list)


def run_mdrecorder(account):
    run_api(MdRecorder, account, None)
