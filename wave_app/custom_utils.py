
from h2o_wave import Q, main, app, ui
import pandas as pd


def ui_table_from_df(
        df: pd.DataFrame,
        name: str = 'table',
        sortables: list = None,
        filterables: list = None,
        searchables: list = None,
        min_widths: dict = None,
        max_widths: dict = None,
        multiple: bool = False,
        groupable: bool = False,
        downloadable: bool = False,
        link_col: str = None,
        height: str = '100%') -> ui.table:

    """ pandas.DataFrameを表示形式（ui.table）に変換
    """

    #print(df.head())

    if not sortables:
        sortables = []
    if not filterables:
        filterables = []
    if not searchables:
        searchables = []
    if not min_widths:
        min_widths = {}
    if not max_widths:
        max_widths = {}

    columns = [ui.table_column(
        name=str(x),
        label=str(x),
        sortable=True if x in sortables else False,
        filterable=True if x in filterables else False,
        searchable=True if x in searchables else False,
        min_width=min_widths[x] if x in min_widths.keys() else None,
        max_width=max_widths[x] if x in max_widths.keys() else None,
        link=True if x == link_col else False
    ) for x in df.columns.values]

    try:
        table = ui.table(
            name=name,
            columns=columns,
            rows=[
                ui.table_row(
                    name=str(i),
                    cells=[str(df[col].values[i]) for col in df.columns.values]
                ) for i in range(df.shape[0])
            ],
            multiple=multiple,
            groupable=groupable,
            downloadable=downloadable,
            height=height
        )
    except Exception:
        print(Exception)
        table = ui.table(
            name=name,
            columns=[ui.table_column('x', 'x')],
            rows=[ui.table_row(name='ndf', cells=[str('No data found')])]
        )

    return table



