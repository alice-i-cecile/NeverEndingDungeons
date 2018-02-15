from typing import List
from classes import *

# TODO: apply type hints
# TODO: add docstrings
# TODO: empty inventory and contents should be [], not ""
def import_element(e_series):
    # TODO: is there a way to automatically apply matching names?
    if e_series.element_type == 'Base':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "))
    elif e_series.element_type == 'Interactable':
        new_element = Interactable(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              interaction_result = e_series.interaction_result)
    elif e_series.element_type == 'NPC':
        if str(e_series.inventory) == 'nan':
            e_inventory = []
        else:
            e_inventory = e_series.inventory.split(sep=", ")
        new_element = NPC(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              race = e_series.race,
                              disposition = e_series.disposition,
                              inventory = e_inventory)
    elif e_series.element_type == 'AbilityCheck':
        new_element = AbilityCheck(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              ability = e_series.ability,
                              proficiency = e_series.proficiency,
                              difficulty = e_series.difficulty,
                              success = e_series.success,
                              failure = e_series.failure)
    elif e_series.element_type == 'Treasure':
        if str(e_series.content) == 'nan':
            e_content = []
        else:
            e_content = e_series.content.split(sep=", ")
        new_element = Treasure(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              contents = e_content)
    else:
        raise ValueError(f'Invalid element_type {e_series.element_type}')

    return new_element


def filter_by_tags(tags: str, valid_tags: List[str]):
    tags = tags.split(sep=', ')
    return any(i in tags for i in valid_tags)

def calculate_xp(cr: str):
    xp_by_cr = {'0': 0,
                '1/8': 25,
                '1/4': 50,
                '1/2': 100,
                '1': 200,
                '2': 450,
                '3': 700,
                '4': 1100,
                '5': 1800,
                '6': 2300,
                '7': 2900,
                '8': 3900,
                '9': 5000,
                '10': 5900,
                '11': 7200,
                '12': 8400,
                '13': 10000,
                '14': 11500,
                '15': 13000,
                '16': 15000,
                '17': 18000,
                '18': 20000,
                '19': 22000,
                '20': 25000,
                '21': 33000,
                '22': 41000,
                '23': 50000,
                '24': 62000,
                '25': 75000,
                '26': 90000,
                '27': 105000,
                '28': 120000,
                '29': 135000,
                '30': 155000}

    xp = xp_by_cr[cr]
    return xp
