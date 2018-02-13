# Universal data ####
universal_tags = ['boring', 'creepy']


# Element data ####
valid_element_types = ['Element', 'Interactable', 'NPC', 'SkillCheck']
valid_sizes = map(Size, ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan'])
valid_dispositions = map(Disposition, ['Hostile', 'Unfriendly', 'Indifferent', 'Friendly', 'Helpful'])
valid_abilities = map(Ability, ['Strength', 'Constitution',
                   'Dexterity', 'Intelligence',
                   'Wisdom', 'Charisma'])
valid_skills = map(Skill, ['None',
                'Athletics',
                'Acrobatics', 'Sleight of Hand', 'Stealth',
                'Arcana', 'History', 'Investigation', 'Nature', 'Religion',
                'Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival',
                'Deception', 'Intimidation', 'Performance', 'Persuasion'])

element_descriptions = ['A chair', 'A table']
element_gm_notes = ['You can sit on it', 'You can sit at it']

interaction_results = ['Nothing happened.', 'It blew up!']

npc_races = ['Orc', 'Troll']

check_successes = ['Stunning sucess']
check_failures = ['Remarkable failure']

# Room data ####
valid_challenges = map(Challenge, ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly'])
valid_safetys = map(Safety, ['Unsafe', 'Risky', 'Sheltered', 'Safe'])

room_connection_types = ['heavy door', 'gate']
room_flavours = ['A bright clean room.', 'A damp dungeon.']
