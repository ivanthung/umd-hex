""" Configs for the different data types."""

profile_data = {
    "fields_edit" : {'fixed': ["building_type", "building_sub_type"], 'variable': ["impact_m2"]},
}

project_data = {
    "geo": {"location": (52.309033724116524, 4.967533318175478),
        "zoom": 13,
        "tiles": "Cartodb Positron",
        "popup_fields": ["fuuid", "bouwjaar", "gebruiksdo"],},
    "fields_edit" : {'fixed': ["bouwjaar", "oppervlakt", "aantal_ver"], 'variable': ["prof_now", "prof_fut"]}
}
