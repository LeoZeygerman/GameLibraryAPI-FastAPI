class AppException(Exception):
    status_code = 500
    detail = 'Внутренняя ошибка'


class NotFoundError(AppException):
    status_code = 404
    detail = 'Объект не найден!'