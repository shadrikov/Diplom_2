class URLs:

    MAIN_URL = 'https://stellarburgers.education-services.ru/'
    
    CREATE_USER = f'{MAIN_URL}api/auth/register'

    LOGIN_USER = f'{MAIN_URL}api/auth/login'

    DELETE_USER = f'{MAIN_URL}api/auth/user'

    CREATE_ORDER = f'{MAIN_URL}api/orders'

    GET_INGREDIENTS = f'{MAIN_URL}api/ingredients'

class ResponseMessages:
    # Ожидаемые сообщения в ответах API
    CREATE_USER_MISSING_REQUIRED_FIELDS = 'Email, password and name are required fields'
    CREATE_USER_WITH_REPEATING_EMAIL = 'User already exists'
    LOGIN_USER_WITH_INCORRECT_LOGPASSW = 'email or password are incorrect'
    CREATE_ORDER_WITHOUT_INGREDIENTS = 'Ingredient ids must be provided'
    CREATE_ORDER_WITH_INCORRECT_INGREDIENT_HASH = 'One or more ids provided are incorrect'

class Flags:
    # Флаги для проверки успешных операций
    USER_DATA = 'user'
    ACCESS_TOKEN = 'accessToken'
    REFRESH_TOKEN = 'refreshToken'
    ORDER_NAME = 'name'
    ORDER_DATA = 'order'
    ORDER_NUMBER = 'number'

