from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.domain import DomainError, ExpenseNotFoundError, UserEmailExists, UserNameExists, UserNotFoundError, UserPhoneExists

DOMAIN_ERROR_HTTP_MAP = {
    UserNotFoundError: 404,
    ExpenseNotFoundError: 404,
    UserEmailExists: 409,
    UserNameExists: 409,
    UserPhoneExists: 409
}

def register_exceptions_handlers(app):

    @app.exception_handler(DomainError)
    def handler_global_exceptions(request: Request, exc: DomainError):
        status_code= DOMAIN_ERROR_HTTP_MAP.get(type(exc),500)

        payload={"message":str(exc)}

        extra_data = {k: v for k, v in vars(exc).items() if not k.startswith("_")}
        payload.update(extra_data)

        return JSONResponse(
            status_code=status_code,
            content=payload
        )
        
