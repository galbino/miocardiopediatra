class AbroadException(BaseException):
    pass


class LackOfParameters(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "Falta(m) parâmetro(s)")])
        super().__init__(message)


class LoginIncorrect(AbroadException):
    def __init__(self):
        message = dict([("code", 404), ("message", "E-mail ou Senha incorreto(s)")])
        super().__init__(message)


class DuplicateCPFOrEmail(AbroadException):
    def __init__(self):
        message = dict([("code", 409), ("message", "CPF ou e-mail já cadastrados.")])
        super().__init__(message)


class SamePassword(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "A nova senha precisa ser diferente da antiga.")])
        super().__init__(message)


class WrongPassword(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "A senha antiga está incorreta.")])
        super().__init__(message)


class CRMMismatch(AbroadException):
    def __init__(self, hospital):
        message = dict([("code", 400), ("message", "Não há um CRM correspondente ao estado do hospital " + hospital)])
        super().__init__(message)


class BadRequest(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "Bad Request")])
        super().__init__(message)


class NotFound(AbroadException):
    def __init__(self):
        message = dict([("code", 404), ("message", "Nenhum resultado foi encontrado.")])
        super().__init__(message)


class InvalidParameter(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "Algum(s) dos parâmetro(s) estão inválidos.")])
        super().__init__(message)


class WeakPassword(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "A senha é fraca.")])
        super().__init__(message)


class InvalidCPF(AbroadException):
    def __init__(self):
        message = dict([("code", 400), ("message", "O CPF é inválido.")])
        super().__init__(message)


class Forbidden(AbroadException):
    def __init__(self):
        message = dict([("code", 403), ("message", "O usuário não tem permissão para realizar esta ação.")])
        super().__init__(message)


class InvalidToken(AbroadException):
    def __init__(self):
        message = dict([("code", 403), ("message", "Token expirado ou inválido.")])
        super().__init__(message)


class SignupPending(AbroadException):
    def __init__(self):
        message = dict([("code", 401), ("message", "O cadastro está pendente de validação.")])
        super().__init__(message)


class CommentWithoutDocument(AbroadException):
    def __init__(self):
        message = dict([("code", 403), ("message", "Não existe nenhum documento associado para comentar.")])
        super().__init__(message)

