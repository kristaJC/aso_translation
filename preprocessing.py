







preprocessing_prompt = """
As a pre-processing step prior to future calls to a translation bot. 

The inputs are related to mobile gaming, the context of which is described as follows: 

{game_context}

You will receive English phrases as input. For each input phrase, you will perform the following steps and return the results as a JSON string.  You will return a *list* of JSON strings, one for each input phrase.  The list of JSON strings should be enclosed in square brackets.

For each input English phrase:

1.) Identify if there is any word play or puns. Indicate this in the 'word_play_flag' field with a True/False boolean.
2.) If there is word play, identify and describe the type of word play in the 'word_play_description' field. If there is no word play, the value should be None.
3.) If there is word play, please re-write the English sentence in a more simplified way that makes it easier to translate. If there is no word play, the 'basic_EN' field should contain the original English sentence. When rewriting, maintain the overall message of the phrase, keeping in mind that the content will be translated to Latin American Spanish, Brazilian Portuguese, Japanese, German, Italian, French, Russian, Korean, and Simplified Chinese for use in a light and playful mobile game.
4.) Identify any Disney-related references. If there is a Disney reference, please identify and describe in detail the words/phrases that reference Disney in the 'disney_reference' field. If there is no Disney reference, the value should be None.
5.) If there is an English-specific acronym, please identify the underlying meaning of the acronym in the 'english_acronym' field. If there is no English-specific acronym, the value should be None.

Your output MUST be a Python list of JSON strings. Each item in the list corresponds to one of the input phrases.  Each JSON string in the list should represent a dictionary with the keys: 'word_play_flag', 'word_play_description', 'basic_EN', 'disney_reference', and 'english_acronym'. The JSON strings should be directly parsable by a Python program using json.loads() without any errors or modifications. Ensure that all strings within the JSON are properly formatted, including the correct use of escape characters where necessary. Do not include any text or characters outside of the list of JSON strings.

For example, if the input phrases are ["Let it go!", "Hakuna Matata"], the output should be:

[
  {
    "word_play_flag": false,
    "word_play_description": null,
    "basic_EN": "Let it go!",
    "disney_reference": "This is a direct quote from the song 'Let It Go' in the Disney movie 'Frozen', signifying a theme of releasing inhibitions and moving forward.",
    "english_acronym": null
  },
  {
    "word_play_flag": false,
    "word_play_description": null,
    "basic_EN": "Hakuna Matata means no worries for the rest of your days!",
    "disney_reference": "'Hakuna Matata' is a Swahili phrase popularized by the Disney movie 'The Lion King'. It is sung in a famous song and represents a carefree approach to life.",
    "english_acronym": null
  }
]

You will receive a Python list of English phrases as the user's message.  Process each phrase in the list.  Do not include any text or explanation before or after the list of JSON strings.
"""


def build_translation_prompt(game, 
                             type_desc):
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
