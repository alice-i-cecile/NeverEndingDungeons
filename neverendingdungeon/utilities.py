# TODO: apply type hints
# TODO: add docstrings
def import_element(e_series):
    # TODO: is there a way to automatically apply matching names?
    if e_series.element_type == 'Base':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "))
    else if e_series.element_type == 'Interactable':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              interaction_result = e_series.interaction_result)
    #TODO: add conversion of inventory to list
    else if e_series.element_type == 'NPC':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              race = e_series.race,
                              disposition = e_series.disposition,
                              inventory = e_series.inventory)
    else if e_series.element_type == 'SkillCheck':
        new_element = Element(name = e_series.name,
                              description = e_series.description,
                              gm_notes = e_series.gm_notes,
                              cr = e_series.cr,
                              size = e_series.size,
                              tags = e_series.tags.split(sep=", "),
                              ability = e_series.ability,
                              proficiency = e_series.proficency,
                              difficulty = e_series.difficulty,
                              success = e_series.success,
                              failure = e_series.failure)
    else:
        raise ValueError(f'Invalid element_type {e_series.element_type}')

    return new_element
