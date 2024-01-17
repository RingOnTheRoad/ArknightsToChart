import sys

from Bar import add_bar
from pyecharts.charts import Timeline
from pyecharts.options import *


def add_timeline(file_name: str, path: str, chart_data: list, time_data: list, line_rewind=False, line_interval=1):
    """
    生成时间线
    :param file_name: 文件名字 (已自动补全格式后缀)
    :param path: 生成文件存放路径 (结尾可不含/)
    :param chart_data: 图表数据 (type: list (chart); element_num: no_limit)
    :param time_data: 时间数据 (type: list (int,float,str); element_num: no_limit)
    :param line_rewind: True: 倒带播放 False: 正常播放 (默认: False)
    :param line_interval: 几秒切换一次对象 (默认: 1)
    :return: None
    """
    # 判断传入数据是否为空
    if file_name != '' and path != '' and chart_data != '' and time_data != {}:
        # 判断数据类型是否正确
        if type(chart_data) is list and type(time_data) is list:

            # 初始化时间线并设置属性
            timeline = Timeline(
                {"theme": "dark",
                 "page_title": f"{file_name}",
                 "width": "100%",
                 "height": "800px"
                 }
            )

            # 添加数据
            try:
                n = 0
                for single_bar in chart_data:
                    for _single_time in time_data:
                        timeline.add(single_bar, time_data[n])
                        break
                    n += 1
            except AttributeError:
                print("'chart_data' contains element except 'chart',or 'time_data' contains element except 'num' ('chart_data'包含图表外的元素或'time_data'包含数字外的元素)")
                sys.exit(0)

            # 自动播放设置
            timeline.add_schema(
                is_auto_play=True,
                is_rewind_play=line_rewind,
                play_interval=line_interval * 1000,
                orient="",
                control_position="right",
                pos_top="4%",
                pos_left="60%",
                height="1",
                width="500",
                linestyle_opts=LineStyleOpts(
                    color={
                        'type': 'linear',
                        'x': 0,
                        'y': 0,
                        'x2': 1,
                        'y2': 1,
                        'colorStops': [
                            {'offset': 0, 'color': '#66CCFF'},
                            {'offset': 1, 'color': '#8470FF'}],
                        'global': False
                    }
                ), checkpointstyle_opts=TimelineCheckPointerStyle(
                    color="#43CD80",
                    border_width=3,
                    border_color="rgba(0,0,0,0.5)"
                )
            )
            # 生成时间线 返回提示信息
            try:
                timeline.render(f"{path}/{file_name}.html")
                print(
                    f"已生成名为{file_name}.html的时间线，存放在{path}")
            except OSError:
                print("Illegal path format or naming (非法路径格式或命名)")
            except Exception as e:
                print(type(e))
                print(e, "\nAn unexpected error occurs,bring the information output from the console and "
                               "contact the project manager Ring please (发生意料外的错误，请携带控制台输出的信息，联系该项目管理者Ring)")

        else:
            print("Chart and time data type is wrong,use 'list' type please (图表和时间数据类型错误，请使用列表类型)")

    else:
        print("Empty data exists (存在空数据)")


# 测试方法健壮性
if __name__ == '__main__':
    # 模拟正常数据生成时间线
    n_x_data = {"成绩": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "零花钱": [7, 1, -9, 5, 53, 12, -57, 3, 2, 67, 34, -86]}
    n_x_data_1 = {"成绩": [9, 62, 83, 44, 35, 46, 75, 84, 3, 120, 151, 1672],
                  "零花钱": [7, 1, -9, 9, 63, 12, -7, 3, 2, 97, 54, -6]}
    n_x_data_2 = {"成绩": [11, 62, 83, 44, 35, 46, 75, 84, 3, 120, 151, 1672],
                  "零花钱": [7, 1, -9, 9, 63, 12, -7, 3, 2, 97, 54, -6]}
    n_x_data_3 = {"成绩": [15, 62, 83, 44, 35, 46, 75, 84, 3, 120, 151, 1672],
                  "零花钱": [7, 1, -9, 9, 63, 12, -7, 3, 2, 97, 54, -6]}
    n_y_data = {"name": ["小米", "小孩", "雷军", "周杰伦", "陶喆", "王家卫", "陈睿", "林俊杰", "张杰", "南拳妈妈", "阿米娅", "博士", ]}

    bar = add_bar('4', 'D:/Mis/json/stock', '1', n_x_data, n_y_data)
    bar_1 = add_bar('4', 'D:/Mis/json/stock', '2', n_x_data_1, n_y_data)
    bar_2 = add_bar('4', 'D:/Mis/json/stock', '3', n_x_data_2, n_y_data)
    bar_3 = add_bar('4', 'D:/Mis/json/stock', '4', n_x_data_3, n_y_data)
    b_list = [bar, bar_1, bar_2, bar_3]
    t_list = [1, 2, 3, 4]
    add_timeline("4", "D:/Mis/json/stock", b_list, t_list)

    print("-------------------------𝕯𝖎𝖛𝖎𝖉𝖎𝖓𝖌 𝖑𝖎𝖓𝖊-------------------------")

    # 模拟数据缺省
    add_timeline("", "", b_list, t_list)

    print("-------------------------𝕯𝖎𝖛𝖎𝖉𝖎𝖓𝖌 𝖑𝖎𝖓𝖊-------------------------")

    # 模拟数据格式/类型错误
    b_list_1 = [1, 2, 3]
    t_list_1 = ['1', 2, 3, 4]
    add_timeline("4", ":/Mis/json/stock", b_list, t_list)
    add_timeline("?", "D:/Mis/json/stock", b_list, t_list)
    # add_timeline("4", "D:/Mis/json/stock", 9, t_list)
    add_timeline("4", "D:/Mis/json/stock", b_list_1, t_list)
    add_timeline("4", "D:/Mis/json/stock", b_list, t_list_1)
