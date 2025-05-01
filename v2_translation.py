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


### Todo - update Russian guidelines update traditional chinese guidelines
lang_specific_guidelines = {
    'Latin American Spanish':""" - Use informal tú-form - Prioritize friendly, casual verbs like juega, descubre, gana""",
    'Brazilian Portuguese': """ - Use informal você-form - Make copy energetic and emotionally expressive — Divirta-se!""",
    'Italian': """ -Use informal tone with playful verbs like Gioca, Scopri, Divertiti """,
    'Japanese': """ - Use casual-polite forms (e.g., ～しよう, ～が登場), - Match the upbeat, punchy tone of puzzle and gacha games """,
    'French':""" -Use informal tu-form -Make phrasing smooth, vivid, and naturally expressive """,
    'German': """ """,
    'Simplified Chinese': """ - Keep it brief, casual, and direct - Highlight excitement and rewards with punchy terms like 限时, 赢奖励 """, 
    'Traditional Chinese': """ - Use casual and lively language that fits mobile game audiences in Taiwan and Hong Kong
    -Favor clear, short sentences with a playful or promotional tone
    -Prioritize fluency and cultural appropriateness over literal phrasing
    -Terms like 表情符號 (emoji), 獎勵 (rewards), and 限時 (limited-time) are common in game copy
    -Avoid overly technical or overly simplified language — it should feel local and fun
    """, 
    'Korean': """ - Favor casual or semi-formal style depending on context - Keep copy concise, lively, and visually engaging """,
    'Russian': """ -Always use the formal second-person plural (вы) 
    -Do not capitalize вы — this is a neutral formal register, not overly honorific
    -All verbs and adjectives must match this formal second-person form
    -The tone should be polite but not stiff or bureaucratic
    -Make phrasing natural and suitable for a general gaming audience"""
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
                # add help for modifying char limit for some languages
                char_limit=row['char_limit']
                if (char_limit in [80,500] and lang in ['Simplified Chinese', 'Traditional Chinese','Korean','Japanese']):
                    char_limit = int(char_limit/2)
                prompt = build_translation_prompt(
                    game=row['Game'],
                    #char_limit=row['char_limit'],
                    char_limit = char_limit,
                    type_desc=row['type_desc'],
                    target_language=lang
                )
                record = {
                    # TODO, include group key and make sure to update inputs to always have this key
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
           
            