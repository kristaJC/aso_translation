from config import *

def get_game_description(game):
    if game in GAME_DESCRIPTION_MAP:
        phrase =  f""" - Game Context:
        {game}: {GAME_DESCRIPTION_MAP[game]}"""
        return phrase
    else:
        return

def build_translation_prompt(game, #phrase, 
                             char_limit, type_desc, target_language):
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
        f.write(json.dumps(record, ensure_ascii=False) + "\n")



def translate(df, target_languages, output_path):

    for idx, row in df.iterrows():
        for lang in target_languages:
            prompt = build_translation_prompt(
                game=row['Game'],
                #phrase=row['EN'],
                char_limit=row['char_limit'],
                type_desc=row['type_desc'],
                target_language=lang
            )
            append_to_jsonl(output_path, prompt, phrase)
            