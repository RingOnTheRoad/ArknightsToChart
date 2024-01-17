from pyecharts.charts import Bar
from pyecharts.options import *


def add_bar(file_name: str, path: str, bar_name: str, x_data: dict, y_data: dict, sorted_index=1, sorted_amount=10,
            sorted_reverse: bool = True, data_level=10):
    """
    生成柱状图
    :param file_name: 文件名字 (已自动补全格式后缀)
    :param path: 生成文件存放路径 (结尾可不含/)
    :param bar_name: 柱状图名字
    :param x_data: X轴数据 (type: dict_list; element_num: no_limit)
    :param y_data: Y轴数据 (type: dict_list "KEY: y-axis_name_data, VALUE: list_data"; element_num: 1)
    :param sorted_index: 排序根据的下标 下标顺序为Y轴数据到X轴数据 (默认: 1)
    :param sorted_amount: 排序后显示排位靠前/后的数量 （默认: 10）
    :param sorted_reverse: True: 数据从大到小排序 False: 数据从小到达排序 (默认: True)
    :param data_level: 数据数量级 (默认: 10,建议为 数据的最大值/10 且为10的倍数)
    :return: Bar
    """
    # 判断传入数据是否为空
    if file_name != '' and path != '' and bar_name != '' and x_data != {} and y_data != {}:

        # 判断Y轴元素个数是否为1
        if len(y_data) == 1:

            # 判断数据类型是否正确
            if type(x_data) is dict and type(y_data) is dict:
                x_data_inside = []
                y_data_inside = []
                for i, v in x_data.items():
                    x_data_inside = type(v)
                for i, v in y_data.items():
                    y_data_inside = type(v)
                if x_data_inside is list and y_data_inside is list:
                    if type(sorted_index) is int and type(sorted_amount) is int and type(sorted_reverse) is bool:

                        # 初始化柱状图并设置属性
                        bar = Bar(
                            {"theme": "dark",
                             "page_title": f"{file_name}",
                             "width": "100%",
                             "height": "800px",
                             "bg_color": "#2c343c"
                             }
                        )

                        # 数据绑定成列表
                        data_list = []
                        data_collection = []
                        i = 0
                        n = 0
                        for key, value in y_data.items():
                            for single_value in value:
                                data_collection.append(single_value)
                                for k, v in x_data.items():
                                    for n in v:
                                        data_collection.append(v[i])
                                        break
                                data_list.append(data_collection)
                                data_collection = []
                                i += 1
                                n = int(n)
                                n += 1
                        # print(f"数据绑定后:{data_list}")

                        # 数据条件排序/筛选
                        data_list.sort(key=lambda element: element[sorted_index], reverse=sorted_reverse)
                        data_list = data_list[:sorted_amount]
                        # print(f"数据条件排序/筛选后:{data_list}")

                        # 添加数据到X轴 Y轴

                        # 获取Y轴名字
                        y_name = ''
                        for key, value in y_data.items():
                            y_name = key
                        # print(f"Y轴名字:{y_name}")

                        # 添加Y轴数据
                        sorted_name = []
                        for single_name in data_list:
                            sorted_name.append(single_name[0])
                        sorted_name.reverse()
                        bar.add_xaxis(sorted_name)
                        # print(f"Y轴数据:{sorted_name}")

                        # X轴组装数据
                        x_list = []
                        x_all_list = []
                        s = 1
                        element_num = len(data_list[0])
                        while s < element_num:
                            for single_value in data_list:
                                for _n in single_value:
                                    x_list.append(single_value[s])
                                    break
                            x_all_list.append(x_list)
                            x_list = []
                            s += 1
                        # print(f"X轴组装数据后:{x_all_list}")

                        # X轴组装数据名称
                        name_collection = []
                        for s_name in x_data.keys():
                            name_collection.append(s_name)
                        # print(f"X轴组装数据名称后:{name_collection}")

                        # 添加X轴数据
                        s = 0
                        for single_value in x_all_list:
                            for _single_name in name_collection:
                                single_value.reverse()
                                bar.add_yaxis(name_collection[s], single_value, label_opts=LabelOpts(position="right"))
                                # print(f"X轴数据:{single_value}")
                                break
                            s += 1

                        # 设置全局配置项
                        bar.set_global_opts(
                            # 标题
                            title_opts=TitleOpts(
                                title=f"{bar_name}",
                                pos_left="center",
                                pos_bottom='1%'
                            ),
                            # 图例
                            legend_opts=LegendOpts(
                                pos_top="3%",
                                pos_left="25%"
                            ),
                            # 工具箱
                            toolbox_opts=ToolboxOpts(
                                is_show=True,
                                orient='vertical',
                                pos_left="95%",
                                pos_bottom='89.5%',
                                feature={
                                    "saveAsImage": {"pixelRatio": 2, "title": " "},
                                    "restore": {"title": " "},
                                    "dataView": {
                                        "textareaColor": "#333",
                                        "textColor": "#fff",
                                        "backgroundColor": "#3b3f42",
                                        "buttonColor": "#b0b1b5",
                                        "title": " "
                                    },
                                    "magicType": {"type": ["stack", "tiled"], "title": " "}
                                }
                            ),
                            # Y轴
                            yaxis_opts=AxisOpts(
                                name=f"{y_name}",

                            ),
                            # 视觉映射
                            visualmap_opts=VisualMapOpts(
                                min_=-data_level,
                                max_=data_level,
                                range_text=["High", "Low"],
                                pos_left="1%",
                                pos_bottom="2%",
                                background_color="#363636",
                                border_width=1,
                                border_color="#A4D3EE"
                            )
                        )

                        # 反转坐标轴
                        bar.reversal_axis()

                        # 生成柱状图 返回提示信息
                        try:
                            # bar.render(f"{path}/{file_name}.html")
                            # print(
                            #     f"Bar named '{file_name}.html' is already generated,located at {path} (已生成名为{file_name}.html的柱状图，存放在{path})")
                            return bar
                        except OSError:
                            print("Illegal path format or naming (非法路径格式或命名)")
                        except Exception as e:
                            print(type(e))
                            print(e, "\nAn unexpected error occurs,bring the information output from the console and "
                                           "contact the project manager Ring please (发生意料外的错误，请携带控制台输出的信息，联系该项目管理者Ring)")

                    else:
                        print("Make sure 'sorted_index' and 'sorted_amount' is 'int' type,and 'sorted_reverse' is 'bool' type (请确保'sorted_index'和'sorted_amount'为整数类型,'sorted_reverse'为布尔类型")

                else:
                    print("Dict's subclass type is wrong,use 'list' type please (字典中子类数据类型错误，请使用列表类型)")

            else:
                print("Axis data type is wrong,use 'dict' type please (轴数据类型错误，请使用字典类型)")

        else:
            print("Y-axis has more than 1 element (Y轴存在的元素个数大于1)")

    else:
        print("Empty data exists (存在空数据)")


# 测试方法健壮性
if __name__ == '__main__':
    # 模拟正常数据生成折线图
    n_x_data = {"成绩": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "零花钱": [7, 1, -9, 5, 53, 12, -57, 3, 2, 67, 34, -86]}
    n_y_data = {"name": ["小米", "小孩", "雷军", "周杰伦", "陶喆", "王家卫", "陈睿", "林俊杰", "张杰", "南拳妈妈", "阿米娅", "博士", ]}
    add_bar('3', 'D:/Mis/json/stock', '3', n_x_data, n_y_data)

    print("-------------------------𝕯𝖎𝖛𝖎𝖉𝖎𝖓𝖌 𝖑𝖎𝖓𝖊-------------------------")

    # 模拟数据缺省
    m_x_data = {}
    m_y_data = {}
    add_bar('', '', '', m_x_data, m_y_data)

    print("-------------------------𝕯𝖎𝖛𝖎𝖉𝖎𝖓𝖌 𝖑𝖎𝖓𝖊-------------------------")

    # 模拟数据格式/类型错误
    mut_y_data = {"name": ["洪金宝", "李嘉诚"], "country": ["china", "china"]}
    w_x_data = {"score": ("99", "99"), "age": ("123", "987")}
    add_bar('3', 'D:/Mis/json/stock', '3', n_x_data, mut_y_data)
    add_bar('3', ':/Mis/json/stock', '3', n_x_data, n_y_data)
    add_bar('?', ':/Mis/json/stock', '/', n_x_data, n_y_data)
    add_bar('?', ':/Mis/json/stock', '/', n_x_data, n_y_data)
    # add_bar('?', ':/Mis/json/stock', '/', [n_x_data], [n_y_data])
    add_bar('?', ':/Mis/json/stock', '/', w_x_data, n_y_data)
    # add_bar('3', 'D:/Mis/json/stock', '3', n_x_data, n_y_data, sorted_index='')
