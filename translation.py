from config import *

def get_game_description(game):
    if game in GAME_DESCRIPTION_MAP:
        phrase =  f""" Game Context:
        {game}: {GAME_DESCRIPTION_MAP[game]}"""
        return phrase
    else:
        return

### EDIT THIS BC WE WANT TO INCLUDE THE GAME DESCRIPTION AS A STANDALONE

def build_translation_prompt(game, phrase, char_limit, type_desc, target_language):
    game_description = get_game_description(game)
    
    return f"""
You are translating game content for localization. Translate the following English phrase into {target_language}.

Input format:
- Game: {game}
- Type: {type_desc}
- Character limit: {char_limit}

{game_description}

Phrase:
"{phrase}"

Your translation must:
- Be fully natural and fluent in {target_language}
- Stay within {char_limit} characters
- Match the tone and gameplay context of the original (e.g. event, character, reward)
- Use known franchise translations if from Disney (for DEB)
- Use food/pastry-themed tone for CJ
- Use panda rescue/bubble pop themes for PP

Return only the translated phrase, no explanation.
"""


def translate(df, target_languages):

    for idx, row in df.iterrows():
        for lang in target_languages:
            prompt = build_translation_prompt(
                game=row['Game'],
                phrase=row['EN'],
                char_limit=row['char_limit'],
                type_desc=row['type_desc'],
                target_language=lang
            )
            translation = call_gpt_api(prompt)
            df.at[idx, lang] = translation
