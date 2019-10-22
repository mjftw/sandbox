import argparse
import os
from aiohttp import web

# aiohttp
app = web.Application()
routes = web.RouteTableDef()

root_dir = ''

@routes.get('/')
@routes.get('/{tail:.*}')
async def handle(request):
    file = request.match_info.get('tail', None)
    file = file or 'index.html'
    file = os.path.join(root_dir, file)

    try:
        response = web.FileResponse(file)
    except FileNotFoundError:
        response = web.Response(status=404)

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--hostip', action='store',
        default=None,
        help='Host IP address')
    parser.add_argument(
        '-p', '--port', action='store',
        default=None,
        help='Host port')
    parser.add_argument(
        '-d', '--dir', action='store',
        default=None,
        help='Dir to serve pages from')
    args = parser.parse_args()

    root_dir = args.dir or '.'

    app.add_routes(routes)
    web.run_app(app, host=args.hostip, port=args.port)
