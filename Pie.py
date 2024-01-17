import pyecharts.options as opts
from pyecharts.charts import Pie


def add_pie(file_name: str, path: str, bar_name: str, x_data: list, y_data: list):
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    (
        Pie(init_opts=opts.InitOpts(bg_color="#2c343c"))
        .add(
            series_name=bar_name,
            data_pair=data_pair,
            # rosetype="radius",
            # radius="55%",
            # center=["50%", "50%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=bar_name,
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render(f"{path}/{file_name}.html")
    )
    print(f'{file_name}-Pie图已生成')
