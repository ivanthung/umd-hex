#%%
import pandas as pd

from utils import google_helpers

URL_PRODUCTS = "https://docs.google.com/spreadsheets/d/18CAT02PSTzp-gkhHBMxDO5as2uNLTcZsFC8r3OExqsY/edit#gid=424436814"

URL_BUILDING_PROFILES = "https://docs.google.com/spreadsheets/d/1s42HBt2kxTiVUqvqOaUvC42qbtYPSh9FJErTL64bW8A/edit#gid=2121661472"

URL_METADATA = "https://docs.google.com/spreadsheets/d/1Z4rFo0C3PeTY9JAXLmIzRgmICLHSAZQ80z_nEsZPVpc/edit#gid=2121661472"

#%%
def preprocess_building_profiles(df, sheetname):
    """Preprocess the building profiles dataframe"""
    # Convert the typologies to the standard typologies
    
    if sheetname == "Gebouwprofielen Urban Mining":
        df = pd.melt(df, id_vars = ["building_type", "productcode"],
                     value_vars = ["<1945", ">1945 <1970", ">1970 <2000", ">2000 <2018", "2019"],
                     var_name = "cohort",
                     value_name = "units_per_m2")

        df['units_per_m2'] = df['units_per_m2'].astype(float)
        
        df['construction_type'] = "conventional"
    
    if sheetname == "Optopwoningen":
        df['construction_type'] = "conventional"
        df.loc[df["building_type"] == "Optopwoning_biobased", "construction_type"] = "biobased"
    
    if sheetname == "Biobased Gebouwprofielen Urban Mining":
        df.rename(columns = {"2019" : "units_per_m2"}, inplace = True)
        df['cohort'] = "2019"
        df['construction_type'] = "biobased"
        
    if sheetname == "Biobased utiliteitsgebouwen":
        df['construction_type'] = "biobased"
    
    return df

def load_building_profiles(sheet_name,
                            url_building_profiles = URL_BUILDING_PROFILES,
                            required_columns = ["construction_type", "building_type", "cohort", "productcode", "units_per_m2"]):
    
    profiles_df = google_helpers.load_google_sheet(url_building_profiles, sheet_name)
    
    profiles_df = preprocess_building_profiles(profiles_df, sheet_name)
    
    missing_columns = [col for col in required_columns if col not in profiles_df.columns]
    assert len(missing_columns) == 0, f"Missing columns in the building profiles dataframe: {missing_columns} \n Sheetname: {sheet_name}"
    
    profiles_df = profiles_df[required_columns]
    
    return profiles_df
    

    
# %%
def load_product_impacts(URL_PRODUCTS = URL_PRODUCTS, sheetname = "product_impacts"):
    impacts_df = google_helpers.load_google_sheet(URL_PRODUCTS, "product_impacts")
    
    # 1 preprocess columns
    impacts_df.columns = impacts_df.columns.str.lower().str.strip().str.replace(' ', '_')
    impacts_df['fase_a_tot'] = impacts_df['fase_a_prod'] + impacts_df['fase_a_constr']
    
    relevant_columns = ['productcode', 'fase_a_tot', 'indicator']
    
    impacts_df = impacts_df[relevant_columns]
    
    # 2 select relevant indicators
    gwp_impacts = impacts_df[impacts_df['indicator'].str.contains("gwp", case=False)].drop(columns = ['indicator'])
    mki_impacts = impacts_df[impacts_df['indicator'].str.contains("mki", case=False)].drop(columns = ['indicator'])
    
    # 3 merge back together for the final df
    impacts_df = pd.merge(gwp_impacts, mki_impacts, on = ['productcode'], suffixes = ('_gwp', '_mki'))
    
    return impacts_df

def load_product_mass():
    mass_df = google_helpers.load_google_sheet(URL_PRODUCTS, "product_materials")
    
    # load product material groupings
    
    # load the sbk specific materials ?
    
    # calculate weight per product

def load_metadata():
    # load element metadata
    
    # 
    
    pass

def create_dataset(output_name):
    # create UMB-std
    
    # create UMB-std-materials
    
    # create UMB-future
    
    # create UMB-future-materials
    pass

def convert_typologies(df):
    """The purpose of this function is to convert the typologies to the standard typologies""" # MR20231123: I know I've done it like this many times before as well, but I think it's better to have data such as this in a sheet somewhere that you load this data from. Now it's hidden away in this script and in the case that you want to change the building mapping in multiple scripts you have to change the individual files instead of one central sheet.
    building_type_dict = {
        "1.01 Woning, tussen, small (hellend dak) - electric": "single family dwellings",
        "4.01 Woning, vrij - electric": "detached houses",
        "3.01 Woning, hoek, medium - electric": "semi-detached houses",
        "6.01 Woongebouw, medium - electric": "multi-family dwellings",
        "8.01 Kantoorgebouw, medium - electric": "offices",
        "Winkelvastgoed; referentie Solitaire winkelunit, 2.000 m²": "wholesale and retail trade buildings",
        "Logiesgebouwen; referentie Logies, collectief 1500 m²": "hotels and restaurants",
        "woonzorgcentrum": "health care buildings",
        "brede school": "educational buildings"
    }

    # Replace the values in df['building_type'] according to the dictionary, only is key is in the dict
    df['building_type'] = df['building_type'].map(building_type_dict).fillna(df['building_type'])
    return df

sheetnames = ["Gebouwprofielen Urban Mining", "Optopwoningen", "Biobased Gebouwprofielen Urban Mining", "Biobased utiliteitsgebouwen"]

building_profiles = pd.concat([load_building_profiles(sheetname) for sheetname in sheetnames])

load_product_impacts()    
    
    


    

# %%
