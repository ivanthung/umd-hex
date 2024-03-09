# Installation and start-up
`` pip install -r requirements.txt
streamlit run app.py ``

# Development notes

### Architecture
This app uses a hexagonal architecture, also called 'ports and adapters'. The hexagonal architecture is a software design pattern that aims to decouple the core business logic of an application from external dependencies such as databases, user interfaces, and external services. It achieves this by dividing the application into three main layers: the core, the ports, and the adapters. In our instance.

- Domain.py defines all main classes to be used.
- The service class defines all the 'business logic', such as calculating KPIs, calculating results, etcetera. 
- UI Adapters (in the adapters folder), create the interface components. Each UI Adapter loads the Service as a class instance from the session state, and uses that to make calls to the database.

### Practical Design principles
- UI Adapters only use the Service. They never call the data adapters directly.
- Only the UI adapters, App.py and pages contain streamlit logic. 
- Adapters should be interchangeable in a later stage (e.g., exchanging the excel adapter to a database adapter)

### Streamlit implementation of this app.
- App.py is the main entry point to the app and loads the service in the the session state.
- Each python file in the pages folder represents a page of the streamlit app, and runs seperately everytime you click on the page. 
- Our service is stored in the st.session_state var which is persisted even as you switch pages. 


# Prototyping new functionalities. 
We can develop in a hacky way to quickly iterate on ideas, and to get the main concepts accorss, and in a 'solid' way that retains code quality and maintainability high for future use. First version is much faster but doesn't scale well. Second version has a bunch of overhead but makes the future a better place to be coding in. 

## A. Developing a new page & functionalities in the hacky way. (e.g.for MVP version)
Developing a new page the hacky way for quick prototyping involves creating all UI streamlit components directly on the page. You can also choose to load new data as you want directly on the page as you would normally do in python. Note that that data and changes done to it will not persist and not be saved to a file.  

1. Create a new page with the name of your page in the folder pages, e.g.:
``` touch pages/new_page.py```

2. Load the main basic functionalities to have access to the database, and giving it a title.
```
from app import load_service  
from utils import pages

page.set_page_title("Pas gebouwprofiel aand")

# Setting the page title and loading the logo. 

load_service()
session = st.session_state

# This loads the database and all main business logic we already developed before in the page.

df = session.service.get_all(domain.Resource.BuildingProject)

# This is an example of how to load the 'building project' data into a dataframe. 

--- go crazy here in prototyping new functaionalities, loading data, creating streamlit interface components, etc. 

```


## B. Develping new functionalities the right way 

## Creating a new UI functionality in the right UI Adapter.
In the hexagonal architecture, each adapter should be in theory be interchangeable for another on that use the same interface as defined in the domain. The app.py and pages should just load the adapters with the righ paramters. Adapters are grouped by function, e.g., at the moment I only have an interface for building project data. This adapter lives in **adapters/ui/building_profile_interface.py**. Let's say we want to add a functionality that displays a single project or profile. Then, to the class StreamlitBuildingProfileInterface, add a method called "pretty_show_single". 


``` 
def pretty_show_single(self, resource: domain.Resource, row_num: int) -> pd.DataFrame:
""" displaying a single instance according to the rownumber """
    
```
As the data is already loaded at init in the self.service variable, we can use ```self.service.get_building_data(domain.Resource)``` this is a method that is defined in core/service.py and takes the name of the resource as input, which is defined in the Enum in core/domain.py.

Then we can use any streamlit function to display it on the app, for example:
``` 
def pretty_show_single(self, resource: domain.Resource, row_num: int) -> pd.DataFrame:
""" displaying a single instance according to the rownumber """
    df = self.service.get_building_data(resource)
    st.write(df.iloc[row_num])

```
Now that this function exists, call it on your page, for example:

```
from app import load_service  
from utils import pages
from adapters.ui import StreamlitBuildingProfileInterface

# Setting the page title and loading the logo. 

page.set_page_title("Pas gebouwprofiel aand")

load_service()
session = st.session_state


# Initialize the service component with the service that is storred in session state.

interface = StreamlitBuildingProfileInterface(session.service)
interface.pretty_show_singe(domain.Resource.BuildingProject, 10)

```

## Adding functionalities to the Service.
Ideally, all our main business logic should exist in the Service class, in **core/service.py**. E.g., if we want to create the calculation of a new KPI add it here:

```
class Service(ports.Service):    
    def __init__(self, building_data_repository: ports.DataRepository):
        self.building_data_repository = building_data_repository

    def calculate_CO2_impact(self) -> pd.DataFrame:
        """ New function to calculate impact
        Here we can load data from the building_data_repository and calculate CO2 impact.
        """

        df = .... some logic here to calculate impacts
        return df
    
    def create_materials_MFA_data(self) -> df:
        """ Function to create the data of materials coming from building profiles. """"

        return df
```

After we create this function, it should be called in one of the UI Adapters and the return value can be displayed using any streamlit component.

## Adding a new adapter
For each adapter it is the case that it should should have a corresponding port that lives in the domain in **core/port.py**. The port acts as a 'template' for the adapter, meaning that the adapter should have all the functions defined in the class there.

E.g., we could create a new database adapter (e.g. one using Google Sheets and Authentication) using the port defined in the class ```DataRepository``` in core/ports.py as a template. If we correctly implements this template, we should be able to swap the current adapter we use for loading data, which is the ```BuildingDataRepositoryXls`` class living in ** adapters/data.py ** with this adapter without breaking any code. This way, our hexagonal architecture keeps our options open.

## Add a new local datasource (e.g. local excel file).
Any local datasource needs to be registered in the domain, and loaded through an adapter. It can then be laoded in the 
1. Add the name of your resource in **core/domain.py**

``` 
class Resource(Enum):
    BuildingProject = auto()
    BuildingProfile = auto()
    BuildingProfileSummary = auto()
    ConstructionProducts = auto()
    MaterialImpacts = auto()
    # add a name for your new  new resource here 
```

2. Load your resource in the service in **app.py**, using its filepath and the resource name that you just created. 

```
 building_repository = building_data_repository_xls.BuildingDataRepositoryXls(
            [building_data_repository_xls.PersistedData(filepath = DATA_DIR / "gebouwprofielen.xlsx", resource = domain.Resource.BuildingProfile),
            building_data_repository_xls.PersistedData(filepath = DATA_DIR / "bag" / "bag-ams-zuidoost-platdak-buurt.shp", resource = domain.Resource.BuildingProject),
            building_data_repository_xls.PersistedData(filepath = DATA_DIR / "YOUR NEW RESOURCE FILEPATH", resource = domain.Resource.YOURNEWRESOURCENAME),
            
            ]
            )
```

3. Define if your file will be handled as spatialdata, or just a regular files (e.g. excel) in the building_data_repository_xls.py file.

In case it is a shapefile, add it to the line that handles BuildingProjects (and uses geopandas)
```
for data in local_data:
            match data.resourc:
                case domain.Resource.BuildingProject || case domain..Resource.YOURRESOURCENAME:
```

In case it is an excel file, do the same, but add it the the line with:

``` case domain.Resource.BuildingProject || case domain.Resource.YOURFILENAME```



# Other notes


### ToDo:
* Create 'main philosophy' diagram.
* Implement a proof of concept for a google sheet connection.
* Fix a weird session state bug.

### Backlog
* Create a column config generator

## Datastructure profile
- region
- building_type
- cohort
- functionele_gebouwelementen
- elementen_groep
- element
- productcode
- product
- hoeveelheid_product
- eenheid_product
- m2bvo gebouwhoeveelheid_per_m2


