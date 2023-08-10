from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class SealAPIMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # TODO: Currently in development for logging system.
        res = await call_next(request)
        if res.headers.get("content-type") == "application/json":
            return res
        return res

    async def seal_json(self, res):
        print(type(res))
