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
    else if e_series.element_type == 'Interactable':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              interaction_result = e_series.interaction_result)
    else if e_series.element_type == 'NPC':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              race = e_series.race,
                              disposition = e_series.disposition,
                              inventory = e_series.inventory.split(sep=", "))
    else if e_series.element_type == 'SkillCheck':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              ability = e_series.ability,
                              proficiency = e_series.proficency,
                              difficulty = e_series.difficulty,
                              success = e_series.success,
                              failure = e_series.failure)
    else if e_series.element_type == 'Treasure':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              gold = e_series.gold,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              contents = e_series.content.split(sep=", "))
    else:
        raise ValueError(f'Invalid element_type {e_series.element_type}')

    return new_element


def filter_by_tags(tags: str):
    tags = tags.split(sep=', ')
    return any(i in tags for i in valid_tags)
