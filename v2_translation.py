from config import *
import json
import string
import random

general_guidelines = f""" General Translation Guidelines:


The tone should be:

-Fun, playful, and energetic

-Casual and approachable

-Clear, concise, and engaging for players

You must:

- Use natural, idiomatic language for the target audience

- Prioritize clarity and emotional appeal over literal translation

- Maintain consistent tone and phrasing across all content

- Stay within any provided character limits

If the English text includes puns, idioms, or culturally specific phrases:

- Adapt them to something that feels native and engaging in the target language

- It's okay to rephrase for clarity or punch — fun and fluid is better than literal

Avoid:

- Overly formal or technical phrasing

- Translating idioms or jokes literally if they don’t work in the target language
"""

lang_specific_guidelines = {
    'Latin American Spanish':""" - Use informal tú-form - Prioritize friendly, casual verbs like juega, descubre, gana""",
    'Brazilian Portuguese': """ - Use informal você-form - Make copy energetic and emotionally expressive — Divirta-se!""",
    'Italian': """ -Use informal tone with playful verbs like Gioca, Scopri, Divertiti """,
    'Japanese': """ - Use casual-polite forms (e.g., ～しよう, ～が登場), - Match the upbeat, punchy tone of puzzle and gacha games """,
    'French':""" -Use informal tu-form -Make phrasing smooth, vivid, and naturally expressive """,
    'German': """ """,
    'Chinese': """ - Keep it brief, casual, and direct - Highlight excitement and rewards with punchy terms like 限时, 赢奖励 """, 
    'Korean': """ - Favor casual or semi-formal style depending on context - Keep copy concise, lively, and visually engaging """,
    'Russian': """ - Use less formal phrasing when appropriate (e.g., Собери награды!) - Focus on clear, engaging language with light personality"""
}

def get_language_specific_guidelines(target_language):
    return lang_specific_guidelines[target_language]

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
    language_specific = get_language_specific_guidelines(target_language)
    
    return f"""
You are translating app store marketing copy for a mobile game for localization. Translate the following English phrase into {target_language}.

Input format:
- Game: {game}
- Type: {type_desc}
- Character limit: {char_limit}
{game_description}

{general_guidelines}

{language_specific}

- Use the Game Context to apply appropriate reasoning if provided above. 

Return only the translated phrase, no explanation.
"""

## TODO: (maybe not) separate the batch files by language, then we union them back later after post processing.keep track of row number always so we can union by index

def convert_df_to_jsonl(df, target_languages, output_path):
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            for lang in target_languages:
                prompt = build_translation_prompt(
                    game=row['Game'],
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
           
            