# widgets.py
from import_export.widgets import ForeignKeyWidget

class AgentEncadrementFullNameWidget(ForeignKeyWidget):
    def render(self, value, obj=None):
        if value:
            return f"{value.nom} {value.prenom}"
        return ""
