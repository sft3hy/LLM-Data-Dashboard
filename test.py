import json

sample = """
{
"name": "fatalities_isr_pse_conflict_2000_to_2023",
"dataset_description": "Fatalities in Israel and Palestine from 2000 to 2023",
"fields": [
{"column": "name", "properties": {"dtype": "string", "samples": ["Jihad 'Ata Suliman a-Daghameh", 'Muhammad Mahmoud Salim al-Maqadmeh', "'Alian Salem Alanbari"], "num_unique_values": 4480, "semantic_type": "name", "description": "Name of the person who died"}},
{"column": "date_of_event", "properties": {"dtype": "date", "min": "2000-10-19", "max": "2023-09-24", "samples": ['2002-11-06', '2018-05-14', '2007-05-17'], "num_unique_values": 1490, "semantic_type": "date", "description": "Date of the event that led to the person's death"}},
{"column": "age", "properties": {"dtype": "number", "std": 13.654874173507093, "min": 1.0, "max": 101.0, "samples": [34.0, 7.0, 4.0], "num_unique_values": 89, "semantic_type": "age", "description": "Age of the person who died"}},
{"column": "citizenship", "properties": {"dtype": "category", "samples": ['Israeli', 'Jordanian', 'Palestinian'], "num_unique_values": 4, "semantic_type": "nationality", "description": "Citizenship of the person who died"}},
{"column": "event_location", "properties": {"dtype": "category", "samples": ['Negohot', 'Jenin R.C.', "Ya'bad"], "num_unique_values": 372, "semantic_type": "location", "description": "Location where the event occurred"}},
{"column": "event_location_district", "properties": {"dtype": "category", "samples": ['Rafah', 'Salfit', 'al-Quds'], "num_unique_values": 20, "semantic_type": "location", "description": "District of the event location"}},
{"column": "event_location_region", "properties": {"dtype": "category", "samples": ['Gaza Strip', 'West Bank', 'Israel'], "num_unique_values": 3, "semantic_type": "location", "description": "Region of the event location"}},
{"column": "date_of_death", "properties": {"dtype": "date", "min": "2000-10-19", "max": "2023-09-24", "samples": ['2022-08-18', '2007-08-20', '2011-07-05'], "num_unique_values": 1571, "semantic_type": "date", "description": "Date of the person's death"}},
{"column": "gender", "properties": {"dtype": "category", "samples": ['F', 'M'], "num_unique_values": 2, "semantic_type": "gender", "description": "Gender of the person who died"}},
{"column": "took_part_in_the_hostilities", "properties": {"dtype": "category", "samples": ['Yes', 'Object of targeted killing'], "num_unique_values": 5, "semantic_type": "category", "description": "Whether the person took part in the hostilities"}},
{"column": "place_of_residence", "properties": {"dtype": "category", "samples": ['Evron', 'Halhul'], "num_unique_values": 404, "semantic_type": "location", "description": "Place of residence of the person who died"}},
{"column": "place_of_residence_district", "properties": {"dtype": "category", "samples": ['Rafah', 'Salfit'], "num_unique_values": 20, "semantic_type": "location", "description": "District of the person's place of residence"}},
{"column": "type_of_injury", "properties": {"dtype": "category", "samples": ['fire', 'explosion'], "num_unique_values": 10, "semantic_type": "category", "description": "Type of injury that led to the person's death"}},
{"column": "ammunition", "properties": {"dtype": "category", "samples": ['live ammunition', 'shell'], "num_unique_values": 18, "semantic_type": "category", "description": "Type of ammunition used"}},
{"column": "killed_by", "properties": {"dtype": "category", "samples": ['Israeli security forces', 'Palestinian civilians'], "num_unique_values": 3, "semantic_type": "category", "description": "Entity that killed the person"}},
{"column": "notes", "properties": {"dtype": "string", "samples": ['Killed next to al-Katibah Mosque.', 'Killed along with four members of his family when their home collapsed on them due to a strike.'], "num_unique_values": 3236, "semantic_type": "notes", "description": "Additional notes about the person's death"}}
]
}
"""

print(json.dumps(sample))
