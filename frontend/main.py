# main.py

import panel as pn
import crp_form
import model_interface
from theme_manager import theme_manager

pn.extension()

pn.state.theme = theme_manager.get_theme()

header = pn.Column(
    pn.Row(
        pn.HSpacer(),
        pn.pane.PNG("assets/changegenius+modus21-banner.png", width=800), 
        pn.HSpacer()
    ),
    pn.Spacer(height=50)
)

form_submission_tab = crp_form.get_layout()
database_query_tab = model_interface.get_layout()

tabs = pn.Tabs(
    ("Change Request Form", form_submission_tab),
    ("Database Query", database_query_tab)
)

layout = pn.Column(
    header,
    pn.Spacer(height=10),
    tabs,
    sizing_mode='stretch_width'
)

if __name__ == "__main__":
    layout.show()