from DrissionPage import ChromiumPage, ChromiumOptions
import time
import datetime
from threading import Thread
import multiprocessing


# 各版本强制提交地址，这里主要是找到商品的skuid
url1="https://m.vmall.com/order/confirm?skuIdAndQtys=10086904219753:1"#HUAWEI Mate XT 非凡大师 16GB+1TB 瑞红
url2="https://m.vmall.com/order/confirm?skuIdAndQtys=10086403120488:1"#HUAWEI Mate XT 非凡大师 16GB+512GB 瑞红
url3="https://m.vmall.com/order/confirm?skuIdAndQtys=10086404418822:1"#HUAWEI Mate XT 非凡大师 16GB+256GB 瑞红
url4="https://m.vmall.com/order/confirm?skuIdAndQtys=10086071511795:1"#HUAWEI Mate XT 非凡大师 16GB+1TB 玄黑
url5="https://m.vmall.com/order/confirm?skuIdAndQtys=10086251688629:1"#HUAWEI Mate XT 非凡大师 16GB+512GB 玄黑
url6="https://m.vmall.com/order/confirm?skuIdAndQtys=10086489521680:1"#HUAWEI Mate XT 非凡大师 16GB+256GB 玄黑

dict_skuid={
    '16GB+1TB 瑞红':url1,
    '16GB+512GB 瑞红':url2,
    '16GB+256GB 瑞红':url3,
    '16GB+1TB 玄黑':url4,
    '16GB+512GB 玄黑':url5,
    '16GB+256GB 玄黑':url6,
}



# 订单提交，提交频率0.1s
def buy(tab,buyTimeStr,advance_ms):

    curTime = time.time()
    buyTime = time.mktime(time.strptime(buyTimeStr, "%Y-%m-%d %H:%M:%S"))-advance_ms/1000
    while curTime < buyTime:
        curTime = time.time()
    tab.ele('@id=confirmSubmit').click(by_js=True)
    for i in range(999):
        time.sleep(0.1)
        tab.refresh()
        tab.ele('@id=confirmSubmit').click(by_js=True)

# 创建多个标签页，使用多线程执行购买
def creat_tabs(index,phones,path,buyTimeStr,advance_ms):
    co = ChromiumOptions(read_file=False)
    co.set_browser_path(path)
    co.set_local_port(9222 + index)
    page = ChromiumPage(co)
    page.get(dict_skuid.get(phones[0]))
    tab1 = page.get_tab()
    Thread(target=buy, args=(tab1, buyTimeStr, advance_ms)).start()
    for phone in phones[1:]:
        tab=page.new_tab(dict_skuid.get(phone))
        Thread(target=buy, args=(tab,buyTimeStr,advance_ms)).start()



# 登录，传入浏览器路径和同时启动浏览器数
def login(path,n):
    for i in range(n):
        co = ChromiumOptions(read_file=False)
        co.set_browser_path(path)
        co.set_local_port(9222 + i) #固定浏览器端口方便后续接管操作
        page = ChromiumPage(co)
        page.get(url1)


# 主程序入口，多进程实现多浏览器任务
def main(path,n,buytime,advance_ms,phones):
    today = datetime.date.today()
    buyTimeStr = str(today)+' '+buytime
    processes = []
    for i in range(n):
        process = multiprocessing.Process(target=creat_tabs, args=(i,phones,path,buyTimeStr,advance_ms))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()



if __name__ == '__main__':
    # 浏览器路径
    path='C:\Program Files\Google\Chrome\Application\chrome.exe'
    # 同时启动浏览器数
    n=3
    # 启动浏览器
    login(path,n)

    # 购买时间
    buytime='10:08:00'
    # 时间提前量
    advance_ms=100
    # 抢购手机版本
    phones=['16GB+1TB 瑞红','16GB+512GB 瑞红','16GB+256GB 瑞红','16GB+1TB 玄黑','16GB+512GB 玄黑','16GB+256GB 玄黑']

    # 开始抢购
    main(path,n,buytime,advance_ms,phones)