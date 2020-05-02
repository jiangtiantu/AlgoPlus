```
如无必要，勿增实体
```

# 简介
AlgoPlus是上期技术CTP API的Python封装，具有以下特点：
* **易使用**：Python语言，结构清晰，注释完整，文档详尽。
* **低延时**：基于Cython释放GIL；支持多路行情源；无需主事件引擎，实现去中心化。
* **忠实于CTP官方特性**：充分利用CTP的异步、多线程特性。

# AlgoPlus文档
<http://algo.plus>

# 安装
首先配置[Anaconda环境](http://algo.plus/python/install-anaconda.html)，然后使用pip命令安装：
```
pip install AlgoPlus
```

# 从两个例子开始

## 订阅行情并落地为CSV文件
补充账户密码之后运行，可以订阅行情，并将接收到的数据写入csv文件中。
```python
from AlgoPlus.CTP.MdApi import run_mdrecorder
from AlgoPlus.CTP.FutureAccount import FutureAccount, get_simnow_account

if __name__ == '__main__':
    # 账户配置
    instrument_id_list = [b'rb2010']  # 需要订阅的合约列表
    future_account = get_simnow_account(
        investor_id=b'',  # SimNow账户
        password=b'',  # SimNow账户密码
        instrument_id_list=instrument_id_list,  # 合约列表
        server_name='TEST'  # 电信1、电信2、移动、TEST
    )

    #
    run_mdrecorder(future_account)
```
## 监控账户成交
```python
from multiprocessing import Process, Queue
from AlgoPlus.CTP.MdApi import run_tick_engine
from AlgoPlus.CTP.TraderApi import run_traderapi
from AlgoPlus.CTP.FutureAccount import FutureAccount, get_simnow_account

if __name__ == '__main__':

    # 止盈止损参数
    pl_parameter = {
        'StrategyID': 9,
        'ProfitLossParameter': {
            b'rb2010': {'0': [2], '1': [2]},   # '0'代表止盈, '1'代表止损
            b'ni2007': {'0': [20], '1': [20]},   # '0'代表止盈, '1'代表止损
        },
    }

    # 账户配置
    instrument_id_list = []
    for instrument_id in pl_parameter['ProfitLossParameter']:
        instrument_id_list.append(instrument_id)
    future_account = get_simnow_account(
        investor_id='',                         # SimNow账户
        password='',                            # SimNow账户密码
        instrument_id_list=instrument_id_list,  # 合约列表
        server_name='TEST'                    # 电信1、电信2、移动、TEST
    )

    # 共享队列
    share_queue = Queue(maxsize=100)
    share_queue.put(pl_parameter)

    # 行情进程
    md_process = Process(target=run_tick_engine, args=(future_account, [share_queue]))
    # 交易进程
    trader_process = Process(target=run_traderapi, args=(future_account, share_queue))

    #
    md_process.start()
    trader_process.start()

    #
    md_process.join()
    trader_process.join()
```

# 开源地址
1. 码云：<https://gitee.com/AlgoPlus/>
2. GitHub：<https://github.com/CTPPlus/AlgoPlus>

### QQ群与微信公众号
 * QQ群：**866469866**
 
![](./img/QQ群866469866.png)

 * 微信公众号：**AlgoPlus**
 
![](./img/微信公众号AlgoPlus.jpg)

# 版权
MIT