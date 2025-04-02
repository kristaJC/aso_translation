INPUT_TABLE = 'ds.aso_may_2025_unioned'

TARGET_LANGUAGES = ['Latin American Spanish','Brazilian Portuguese','Italian','Japanese','French','German']

TARGET_LANGUAGES_EXT = ['Chinese', 'Taiwanese','Korean','Russian']

LANG_MAP = dict(zip(TARGET_LANGUAGES, ['es_LA','pt_BR','it_IT','ja_JP','fr_FR','de_DE']))
LANG_MAP_EXT = dict(zip(TARGET_LANGUAGES_EXT, ['zh_CN','zh_TW','ko_KR','ru_RU']))

GAME_DESCRIPTION_MAP = {'CJ':'A match-3 game that features themes of baking, and a Chef Panda as the main character.','DEB':'A game that takes place in the Disney universe - so you may see some references to characters in the now scope of the Disney franchise. Please maintain consistency to the already established translations of Disney related content. ','PP':'A bubble shooter game that involves a Mama Panda and her numerous baby pandas.'}

MODEL = 'gpt-4o'