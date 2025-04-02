from config import *
import json
import string
import random


def get_game_description(game):
    if game in GAME_DESCRIPTION_MAP:
        phrase =  f""" - Game Context:
        {game}: {GAME_DESCRIPTION_MAP[game]}"""
        return phrase
    else:
        return

def build_translation_prompt(game, 
                             #phrase, 
                             char_limit,
                             type_desc, 
                             target_language):
    game_description = get_game_description(game)
    
    return f"""
You are translating game content for localization. Translate the following English phrase into {target_language}.

Input format:
- Game: {game}
- Type: {type_desc}
- Character limit: {char_limit}
{game_description}

Your translation must:
- Be fully natural and fluent in {target_language}
- Stay within {char_limit} characters
- Use the Game Context to apply appropriate reasoning if provided above. 

Return only the translated phrase, no explanation.
"""

#
"""
def call_gpt_api(prompt):
    
    messages = [
        {"role": "user", "content": prompt},
    ]
def append_to_jsonl(output_path, prompt, phrase)
    with open(output_path, 'w', encoding='utf-8') as f:
        record = {
            "custom_id": f"row_{i}",
            "method":"POST",
            "url": "/v1/chat/completions", 
            "body": {"model": MODEL,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps(phrase)}
                ]
            }
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")"""

#TODO: separate the batch files by language, then we union them back later after post processing.keep track of row number always so we can union by index

def convert_df_to_jsonl(df, target_languages, output_path):
    #row_identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            #row_identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            for lang in target_languages:
                #row_identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                prompt = build_translation_prompt(
                    game=row['Game'],
                    #phrase=row['EN'],
                    char_limit=row['char_limit'],
                    type_desc=row['type_desc'],
                    target_language=lang
                )
                record = {
                    "custom_id": f"{lang}_row_{idx}",
                    "method":"POST",
                    "url": "/v1/chat/completions", 
                    "body": {"model": MODEL,
                        "messages": [
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": json.dumps(row['EN'])}
                        ]
                    }
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
           
            