from aiohttp import web

async def handle_post(request):
    data = await request.json()
    return web.json_response({"message": "Data received", "data": data})

app = web.Application()
app.add_routes([web.post('/submit', handle_post)])

if __name__ == '__main__':
    web.run_app(app)