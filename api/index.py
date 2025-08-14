from app import server as app


def handler(event, context):
    from werkzeug.wrappers import Request, Response

    @Request.application
    def application(request):
        return app(request.environ, lambda status, headers: None)

    return Response("OK")
