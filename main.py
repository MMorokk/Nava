import fabric
from fabric import Application
from fabric.widgets.wayland import WaylandWindow
from fabric.widgets.datetime import DateTime
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.centerbox import CenterBox
from fabric.hyprland.widgets import (
    WorkspaceButton,
    Workspaces,
    Language,
)
from fabric.hyprland.service import Hyprland
from fabric.utils import (
    FormattedString,
    bulk_replace,
    get_relative_path,
)
# import gi
# gi.require_version("Gray", "0.1")
# from gi.repository import Gray, Gtk


class MyStatusBar(WaylandWindow):
    def __init__(self, **kwargs):
        super().__init__(
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            **kwargs
        )
        
        self.workspaces = Workspaces(
            name="workspaces",
            spacing=4,
            buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=f"{ws_id}"),
        )
        
        # Add time widget
        self.time = DateTime(('%H:%M', '%I:%M %p'), interval=5000) 
        self.date = DateTime(('%d/%m/%Y', '%d %B %Y, %A'), interval=3600000)
        self.sep = Label(" | ")

        # Right-Side
        self.language = Language(
            formatter=FormattedString(
                "{replace_lang(language)}",
                replace_lang=lambda lang: bulk_replace(
                    lang,
                    (r".*Eng.*", r".*Ukr.*", r".*Pol.*"),
                    ("EN", "UA", "PL"),
                    regex=True,
                ),
            ),
            )
        
        self.system_label = Label("Tray PlaceHolder")
        
        self.tray = ""

        # Set children
        self.children = CenterBox(start_children=[self.workspaces], 
                                  center_children=[self.time, self.sep, self.date], 
                                  end_children=[self.system_label, self.language])

def main():
    bar = MyStatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()

if __name__ == "__main__":
    main()