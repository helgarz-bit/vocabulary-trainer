FIELDS = {
    "word": {
        "prompt": "слово", 
        "settings": {"validation": True, "required": True, "to_lower": True}},
          "translation": 
          {"prompt": "перевод", 
           "settings": {"validation": True, "required": True, "to_lower": True}},
          "example": {
              "prompt": "пример", 
              "settings": {"validation": False, "required": False, "to_lower": False}},
              "category": {
                            "prompt": "категория", 
                            "settings": {"validation": True, "required": True, "to_lower": True}}
              }

stats_fields = {
    "shows": "Общее число показов",
      "correct": "Всего правильных ответов",
        "streak": "Правильных ответов подряд",
          "status": "Статус изучения"
          }


WORD = "word"
TRANSLATION ="translation"
EXAMPLE = "example"
CATEGORY = "category"
PROMPT = "prompt"
SETTINGS = "settings"
VALIDATION = "validation"
REQUIRED=  "required"
TO_LOWER = "to_lower"
SHOWS = "shows"
CORRECT = "correct"
STREAK = "streak"
STATUS = "status"
LEARNED = "learned"
NOT_LEARNED = "not learned"
STREAK_THREE = "streak_three"
