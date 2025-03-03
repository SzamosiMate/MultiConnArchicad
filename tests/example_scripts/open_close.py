
from multiconn_archicad import MultiConn
from multiconn_archicad.dialog_handlers.win_dialog_handler import start_handling_dialogs
from multiconn_archicad.basic_types import TeamworkCredentials

m_conn = MultiConn()
m_conn.connect.all()
headers = m_conn.quit.all()

print(headers[0])

tw = TeamworkCredentials(username='szamosi.mate.iroda',
                         password='*******')

m_conn.open_project.with_teamwork_credentials(headers[0], teamwork_credentials=tw, dialog_handler=start_handling_dialogs)

