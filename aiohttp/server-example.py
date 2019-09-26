# Modified from https://aiohttp.readthedocs.io/en/stable/
from aiohttp import web
from jinja2 import Template


# aiohttp
app = web.Application()
routes = web.RouteTableDef()


@routes.get('/')
@routes.get('/{name}')
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = Template('Hello {{name}}!').render(name=name)
    return web.Response(text=text)


if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app)