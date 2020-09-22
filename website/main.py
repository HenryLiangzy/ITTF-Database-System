import web


urls = (
    '/', 'index',
    '/index', 'index',
    '/hello', 'hello',
    '/helloW', 'hello',
    '/search', 'search',
    '/result', 'result',
)


render = web.template.render('templates/')

class index:
    def GET(self):
        return render.search()


if __name__ == '__main__':
    app = web.application(urls, globals(), True)
    app.run()
