import pandas as pd
import utilities

# Universal data ####
# TODO: generate automatically from database
universal_tags = ['cult', 'ooze', 'demonic', 'mundane', 'secret', 'treasure']

# Element data ####
valid_element_types = ['Element', 'Interactable', 'NPC', 'SkillCheck', 'Treasure']
valid_sizes = ['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']
valid_dispositions = ['Hostile', 'Unfriendly', 'Indifferent', 'Friendly', 'Helpful']
valid_abilities = ['Strength', 'Constitution',
                   'Dexterity', 'Intelligence',
                   'Wisdom', 'Charisma']
valid_skills = ['None',
                'Athletics',
                'Acrobatics', 'Sleight of Hand', 'Stealth',
                'Arcana', 'History', 'Investigation', 'Nature', 'Religion',
                'Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival',
                'Deception', 'Intimidation', 'Performance', 'Persuasion']

element_df = pd.read_csv('../content/elements.csv')
element_df['xp'] = [utilities.calculate_xp(i) for i in element_df.cr]

# Room data ####
valid_challenges = ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly']
valid_safetys = ['Unsafe', 'Risky', 'Sheltered', 'Safe']

room_connection_types = ['heavy door', 'gate']
room_df = pd.read_csv('../content/rooms.csv')

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
