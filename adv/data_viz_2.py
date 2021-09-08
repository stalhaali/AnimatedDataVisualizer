import pandas_alive
import pandas as pd
import bar_chart_race as bcr
from IPython.display import HTML


def create_bar1(doc, kind, title, sort='asc', n_visible=4, orientation='h'):
    """
    Returns the html5 code to display animated graph.

    conditions:
        Kinds of graphs include bar, line, pie, scatter, and bubble
        Sort, n_visible, and orientation parameters only passed if kind is bar
    """
    df = pd.read_csv(doc)
    df = df.set_index(df.columns[0])
    df = df.loc[df.first_valid_index():df.last_valid_index()]
    
    if kind == "bar":
        html = bcr.bar_chart_race(df = df, title = title, n_bars=n_visible,
                               sort=sort, orientation=orientation)
    else:
        html = df.plot_animated(kind=kind, title=title).get_html5_video()

    return html


