from aiohttp import web

async def handle(request):
    name = request.rel_url.query.get('name', 'World')
    return web.Response(text=f"Hello, {name}!")

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app)