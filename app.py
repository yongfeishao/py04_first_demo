import os

# 商品进销存系统

# 用一个字典来存储账户和密码
user = {
    'admin':[
        {
            'uname':'admin',
            'upasswd':'123456'
        },
        {    'uname':'solder',
            'upasswd':'123456'
        },
        {   'uname':'buyer',
            'upasswd':'123456'
        }
    ]
}
# 菜单管理界面,用于不同管理的程序入口
def menu():
    print('**************************')
    print('*1.登录药品采购平台         ')
    print('*2.采购药品                ')
    print('*3.药品入库                ')
    print('*4.药品销售                ')
    print('*5.药品统计                ')
    print('*6.退出                    ')
    print('**************************')

# 判断用户身份，验证用户名密码
# 返回状态 True or False
def check_access(uname,upasswd):
    # 从字典user里面取出admin的值遍历
    for item in user['admin']:
        print(item)
        # 如果账户输入正确
        if uname == item['uname']:
            flag = (upasswd == item['upasswd'])
            break
        else:
            flag = False
    return flag
'''
function:采购商品记录
parameter:
return:None
description:将采购的商品进行序列化，并将结果保存到采购字典中
'''
buy_dict = {}
def buy_record(buy_time,**kw):
    buy_dict[buy_time] = kw

'''
function:入库商品记录
parameter:
return:none
description:将采购的商品进行入库，并将结果保存到库存字典中,如果当前库存
'''
stock_dict = {}
def stock_record(buy_time,stocker,stocker_time):
    if buy_time in buy_dict.keys():
        kw = buy_dict[buy_time].copy()
        # 入库记录是以药品编号作为记录
        m_id = kw.pop('m_id')
        kw['stocker'] = stocker
        kw['stockertime'] = stocker_time
        stock_dict[m_id] = kw
    else:
        print('输入采购时间有误！！！！！！')
'''
function:获取所有的商品编号和名称
'''
def all_m_id():
    if len(stock_dict.keys()) > 0:
        for key in stock_dict.keys():
            item = stock_dict[key]
            print('%s:%s:%s' % (key,item['m_name'],item['m_number']))
    else:
        print('仓库的库存为0 请先录入商品。')
'''
function:记录销售商品
'''
sale_dict = {}
def sale_record(**kw):
    kw_dict = kw
    if kw_dict['m_id'] in stock_dict.keys():
        if kw_dict['sale_time'] not in sale_dict.keys():
            sale_dict[kw_dict['sale_time']] = []
        item_dict = {}
        item_dict['m_id'] = kw_dict['m_id']
        item_dict['m_name'] = stock_dict[kw_dict['m_id']]['m_name']
        item_dict['number'] = kw_dict['number']
        item_dict['buyer'] = kw_dict['buyer']
        sale_dict[kw_dict['sale_time']].append(item_dict)
        print(sale_dict)
    else:
        print('输入商品编号不存在 请重新输入：')
'''
function:统计商品的个数
'''
def count_m(m_id):
    res = {
        'buy':0,
        'stock':0,
        'sale':0
    }
    # 首先统计采购的数量
    for key in buy_dict.keys():
        item = buy_dict[key]
        if item['m_id'] == m_id:
            res['buy'] += int(item['m_number'])
        else:
            print('输入药品编号不存在')
    # 统计库存数量
    if m_id in stock_dict.keys():
        res['stock'] = stock_dict[m_id]['m_number']

    # 统计销售数量
    for key in sale_dict.keys():
        item = sale_dict[key]
        for dic in item:
            if dic['m_id'] == m_id:
                res['sale'] += int(dic['number'])
            else:
                print('输入药品编号不存在')
    return res


def main():
    while True:
        menu()
        user_input = input('请输入你的选择：')
        if '1' == user_input:
            user_name = input('请输入用户名：')
            user_passwd = input('请输入密码')
            #判断用户名、密码是否正确
            results = check_access(user_name,user_passwd)
            if results:
                print('登录成功，请继续其他操作')
            else:
                print('用户名或密码错误，请重新登录')
        elif '2' == user_input:
            buy_time = input('请输入采购时间，按照YYYYMMDD格式输入：')
            m_name = input('请输入药品名：')
            m_id = input('请输入药品编号：')
            m_price = input('请输入药品单价：')
            m_buyer = input('请输入药品的采购者：')
            m_type = input('请输入药品的分类：')
            m_number = input('请输入药品采购的数量：')
            buy_record(buy_time,m_name = m_name,m_id = m_id,m_price = m_price,m_buyer = m_buyer,m_type = m_type,m_number = m_number)
            print(buy_dict)
        elif '3' == user_input:
            buy_time = input('请输入采购时间，按照YYYYMMDD格式输入：')
            # 库存管理员
            stocker = input('请输入入库管理员：')
            # 入库时间
            stocker_time = input('请输入入库时间，按照YYYYMMDD格式输入：')
            stock_record(buy_time,stocker,stocker_time)
            print(stock_dict)
        elif '4' == user_input:
            # 销售是按照 某一天中销售商品的记录  
            sale_time = input('请输入销售日期，按照YYYYMMDD格式输入：')
            # 如何获取当前 日期下 仓库目录下所有的药品编号
            all_m_id()
            m_id = input('请输入药品编号：')
            # 谁买
            buyer = input('请输入购买者：')
            # 购买数量
            number = input('请输入销售数量：')
            if m_id in stock_dict.keys():
                res = int(stock_dict[m_id]['m_number']) - int(number)
                if res < 0:
                    print('库存不足')
                else :
                    stock_dict[m_id]['m_number'] = str(res)
                    # 将销售信息进行记录
                    sale_record(sale_time = sale_time,m_id = m_id,buyer = buyer,number = number)
            else:
                print('商品编号有误')
        elif '5' == user_input:
            print('当前库存药品')
            for key in stock_dict.keys():
                print('编号：%s:药品种类：%s'% (key,stock_dict[key]['m_name']))
            m_id = input('请输入药品编号：')
            # 采购数量，库存数量，销售数量
            a = count_m(m_id)
            print(a)
        elif '6' == user_input:
            msg = input('按下Qorq退出系统：')
            if msg == 'q'or msg == 'Q':
                os._exit(0)
            else:print('按键错误请重新选择。。。。')

        else:
            pass

if __name__ == "__main__":
    main()
