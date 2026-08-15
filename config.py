
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
NEXT_SHOW = "next_show"
INTERVAL = "interval"
LAST_WRONG = "last_wrong"
INTERVALS = "intervals"
SCORE = "score"
ACCURACY_THRESHOLD = "accuracy threshold"
TRANSITION_PARAMS = "transition params"
MIN_SHOWS = "min shows"
MIN_STREAK = "min streak"
MIN_WRONGS = "min wrongs"
NEW = "new"
LEARNING = "learning"
CONSOLIDATING = "consolidating"
REVIEWING = "reviewing"
POSTPONED= "postponed"


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
          "status": "Статус изучения",
          "next_show": "Дата следующего показа",
          "interval": "Интервал повторения",
          "last_wrong": "Количество неверных ответов после последнего изменения статуса"
          }

STATUSES = {
    "new": {
"score": 600,
"transition params": {
"accuracy threshold": 0.6,
"min shows": 3},
        "intervals": [0, 1]}, 
            "learning": {
"score": 500,
"transition params": {
"accuracy threshold": 0.75,
"min shows": 8,
"min streak": 5,
"min wrongs": 2},
                "intervals": [1, 3, 5, 7]}, 
           "consolidating": {
"score": 300,
"transition params": {
"accuracy threshold": 0.85,
"min shows": 15,
"min streak": 7,
"min wrongs": 2},
           "intervals":  [7, 14, 21, 30]}, 
            "reviewing":  {
"score": 100,
"transition params": {
    "min wrongs": 2},
            "intervals": [30, 60, 90]}, 
            "postponed":  {
"score": 0,
            "intervals": []}
}

FIELDS_FOR_SAVE= [SHOWS, CORRECT, STATUS, STREAK,INTERVAL,  NEXT_SHOW, LAST_WRONG]


DEFAULT_CATEGORY= "uncategorized"
