from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Validation failed!")
    # for err in exc.errors():
    #     loc = err["loc"]
    #     msg = err["msg"]
    #     type_ = loc[-1] if len(loc) > 0 else "unknown"
        # print(f"Message index {loc[2]} content failed validation for type {type_}: {msg}")
    print(exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
