from adapters.data.project_data_adapter import BAGProjectAdapter
from adapters.ui.project_interface import StreamlitProjectInterface


path = 'data/bag/bag-ams-zuidoost-platdak-buurt.shp'

bag_data_adapter = BAGProjectAdapter(path)
project_data = bag_data_adapter.load_project_data()
project_interface = StreamlitProjectInterface()
project_interface.create_pretty_display(project_data)
