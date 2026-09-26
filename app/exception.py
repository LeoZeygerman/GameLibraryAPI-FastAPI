class AppException(Exception):
    status_code = 500
    detail = 'Внутренняя ошибка'

    def __init__(self, detail: str | None):
        if detail:
            self.detail = detail


class NotFoundError(AppException):
    status_code = 404
    detail = 'Объект не найден!'