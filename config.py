
WORD = "word"
TRANSLATION = "translation"
EXAMPLE = "example"
CATEGORY = "category"
PROMPT = "prompt"
SETTINGS = "settings"
VALIDATION = "validation"
REQUIRED = "required"
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
    WORD: {
        PROMPT: "слово", 
        SETTINGS: {"validation": True, "required": True, "to_lower": True}},
          TRANSLATION: 
          {PROMPT: "перевод", 
           SETTINGS: {"validation": True, "required": True, "to_lower": True}},
          EXAMPLE: {
              PROMPT: "пример", 
              SETTINGS: {"validation": False, "required": False, "to_lower": False}},
              CATEGORY: {
                            PROMPT: "категория", 
                            SETTINGS: {"validation": True, "required": True, "to_lower": True}}
              }

stats_fields = {
    SHOWS: "Общее число показов",
      CORRECT: "Всего правильных ответов",
        STREAK: "Правильных ответов подряд",
          STATUS: "Статус изучения",
          NEXT_SHOW: "Дата следующего показа",
          INTERVAL: "Интервал повторения",
          LAST_WRONG: "Количество неверных ответов после последнего изменения статуса"
          }

STATUSES = {
    NEW: {
SCORE: 600,
TRANSITION_PARAMS: {
ACCURACY_THRESHOLD: 0.6,
MIN_SHOWS: 3},
        INTERVALS: [0, 1]}, 
            LEARNING: {
SCORE: 500,
TRANSITION_PARAMS: {
ACCURACY_THRESHOLD: 0.75,
MIN_SHOWS: 8,
MIN_STREAK: 5,
MIN_WRONGS: 2},
                INTERVALS: [1, 3, 5, 7]}, 
           CONSOLIDATING: {
SCORE: 300,
TRANSITION_PARAMS: {
ACCURACY_THRESHOLD: 0.85,
MIN_SHOWS: 15,
MIN_STREAK: 7,
MIN_WRONGS: 2},
           INTERVALS:  [7, 14, 21, 30]}, 
            REVIEWING:  {
SCORE: 100,
TRANSITION_PARAMS: {
    MIN_WRONGS: 2},
            INTERVALS: [30, 60, 90]}, 
            POSTPONED:  {
SCORE: 0,
            INTERVALS: []}
}

ACTIONS = {
    "add": {
        "prompt": "добавление",
        "ending": "о"
    },
    "edit": {
        "prompt": "редактирование",
        "ending": "о"
    },
    "delete":{
        "prompt": "удаление",
        "ending": "о"
    },
    "find": {
        "prompt": "поиск",
        "ending": ""
    },
    "find_by_cat": {
        "prompt": "поиск по категории",
        "ending": ""
    },
    "stats_word": {
        "prompt": "вывод статистики слова",
        "ending": ""
}
}


FIELDS_FOR_SAVE= [SHOWS, CORRECT, STATUS, STREAK,INTERVAL,  NEXT_SHOW, LAST_WRONG]
DIFFICULT_THRESHOLD   =0.6

DEFAULT_CATEGORY= "uncategorized"
