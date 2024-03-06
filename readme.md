# Notes
Running: 
pip install -r requirements.txt
streamlit run app.py


## Notes
Experimenting with hexagonal architecture for building profiles in a Python Streamlit app.

ToDo next:
- Create dummy data to load standard data from a google sheets.
- Create a full-flow to display building profiles loaded from sheets, with a Streamlit UI Adapter.


## Each project has:
* Location data.
* Current building profile.
* New building profile.
* Other intervention

## Overall philosophy
* Each building profile is as a class, which can be enriched with additional data and methods.
* Session state (cache) handeling is done on the adapter level in order to maintain the option to switch interface methods. 


## Adapters
* Loading building profile data -> connects local summary table for now. Can be later updated to a DB connection / google sheets.
* Loading materials data  -> connects to Metabolic materials database.
                        -> connects to Metabolic impact table.

## Need for updated concept.
* How to address 'strategy consulting' vs building-based management.
