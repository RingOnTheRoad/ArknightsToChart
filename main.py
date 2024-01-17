import json

import TimeLine
import Bar
import Pie

filename = 'ArknightsData'
save_path = r'D:/BilibiliUps/工程/2024.1/明日方舟时装系列2024/save'
target_path = r'D:/BilibiliUps/工程/2024.1/明日方舟时装系列2024/原始文件'
original_filename = '干员时装.json'
operator_count_list = []
operator_name_list = []
bar_list = []
time_list = []
operator_list = []
date_list = []
key_list = []
value_list = []
same_flag = False
special_flag = False
date_temp = '2019/5/1'
last_flag = '主修领域'
special_title = ['百炼', '承曦', '纯烬', '淬羽', '涤火', '归溟', '寒芒', '火龙S', '假日威龙',
                 '缄默', '琳琅', '麒麟R', '圣约', '焰影', '炎狱', '耀骑士', '濯尘', '浊心']


# 刷新干员出现次数
def refresh_operator(item):
    global same_flag, special_flag
    # 循环干员名单
    for name in operator_name_list:
        # 同名干员
        if item['干员名称'] == name:
            index = operator_name_list.index(name)
            operator_count_list[index] = item['干员积累次数']
            same_flag = True
        # 不同名
        else:
            # 异格筛选
            for title in special_title:
                if title in item['干员名称']:
                    name_temp = item['干员名称'].replace(title, '')
                    # 变为同名干员后添加到列表
                    try:
                        index = operator_name_list.index(name_temp)
                        operator_count_list[index] = item['干员积累次数']
                        same_flag = True
                    except ValueError:
                        operator_count_list.append('1')
                        operator_name_list.append(name_temp)
                        special_flag = True
                    break


# 获得时间线的Bar数据
def export_bar():
    global date_temp, same_flag, special_flag

    # 打开json文件获取数据
    with open(target_path + '/' + original_filename, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 循环遍历json
    for item in json_data:
        # 同一组日期
        if item['实装日期'] == date_temp:
            # 干员名称重合则刷新干员积累次数,异格则单独添加
            refresh_operator(item)
            # 新干员直接添加(不存在重复和异格时)
            if not same_flag | special_flag:
                operator_count_list.append(item['干员积累次数'])
                operator_name_list.append(item['干员名称'])
            else:
                same_flag = False
                special_flag = False

            # 最后提交
            if item['服装名称'] == last_flag:
                bar = Bar.add_bar(date_temp.replace('/', '.'), save_path + '/Bar', date_temp,
                                  {"次数": operator_count_list},
                                  {"名字": operator_name_list}, sorted_amount=20)
                bar_list.append(bar)

        # 不同日期组
        else:
            # 先提交上一组的Bar,用局部变量bar保存到bar_list
            bar = Bar.add_bar(date_temp.replace('/', '.'), save_path + '/Bar', date_temp, {"次数": operator_count_list},
                              {"名字": operator_name_list}, sorted_amount=20)
            bar_list.append(bar)
            # 修改日期缓存
            date_temp = item['实装日期']
            # 干员名称重合则刷新干员积累次数
            refresh_operator(item)
            # 新干员直接添加(不存在重复时)
            if not same_flag:
                operator_count_list.append(item['干员积累次数'])
                operator_name_list.append(item['干员名称'])
            else:
                same_flag = False


# 获得单独的时间
def get_single_date():
    global date_list
    # 打开json文件获取数据
    with open(target_path + '/' + original_filename, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    temp = ''
    for item in json_data:
        if item['实装日期'] != temp:
            date_list.append(item['实装日期'])
            temp = item['实装日期']


# 导出Timeline文件
def export_timeline():
    get_single_date()
    TimeLine.add_timeline('ArknightsTimeline', save_path + '/' + 'Timeline', bar_list, date_list, line_interval=0.5)


# 导出pie图
def export_pie(name: str):
    key_list.clear()
    value_list.clear()
    with open(target_path + '/' + name + '.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for key in json_data[0]:
            key_list.append(key)
            value_list.append(json_data[0][key])
        Pie.add_pie(name, save_path + '/' + 'Bar', '', key_list, value_list)


if __name__ == '__main__':
    export_bar()
    export_timeline()
    export_pie('出身地')
    export_pie('近远战')
    export_pie('星级')
    export_pie('性别')
    export_pie('职业')