import pandas as pd

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

element_df = pd.read_csv(../content/elements.csv)

# Room data ####
valid_challenges = map(Challenge, ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly'])
valid_safetys = map(Safety, ['Unsafe', 'Risky', 'Sheltered', 'Safe'])

room_connection_types = ['heavy door', 'gate']
element_df = pd.read_csv(../content/rooms.csv)

# Dungeon data ####
xp_scaling =   {'1': 50,
                '2': 100,
                '3': 150,
                '4': 250,
                '5': 500,
                '6': 600,
                '7': 750,
                '8': 900,
                '9': 1100,
                '10': 1200,
                '11': 1600,
                '12': 2000,
                '13': 2200,
                '14': 2500,
                '15': 2800,
                '16': 3200,
                '17': 3900,
                '18': 4200,
                '19': 4900}

# FIXME: challenge multipliers not exact for RAW for higher levels
challenge_multipliers = {'Trivial': 0,
                         'Easy': 0.5,
                         'Medium': 1,
                         'Hard': 1.5,
                         'Deadly': 2}
