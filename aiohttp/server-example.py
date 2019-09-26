# Modified from https://aiohttp.readthedocs.io/en/stable/
from aiohttp import web


# aiohttp
app = web.Application()
routes = web.RouteTableDef()

@routes.get('/')
@routes.get('/{name}')
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = 'Hello ' + name + '!'
    return web.Response(text=text)


if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app)