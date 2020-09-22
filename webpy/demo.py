import web
from web import form
import HeadtoHead
import readData


urls = (
    '/', 'index',
    '/index', 'index',
    '/hello', 'hello',
    '/helloW', 'hello',
    '/search', 'search',
    '/result', 'result',
    '/testB', 'testB',
    '/contact', 'contact',
    '/rank', 'rank',
    '/head', 'head',
)


render = web.template.render('templates/')

input_value = form.Form(
    form.Textbox('Word'),
    form.Button('Search')
)


class search:
    def GET(self):
        i = web.input(model=None, word=None)
        if i.model == '1':
            player_name = i.word
            result_list = readData.read_by_name(player_name)
            return render.resultP(result_list)

        if i.model == '2':
            player_id = i.word
            result_list = readData.read_by_id(player_id)
            return render.resultP(result_list)

        else:
            return render.search()


class hello:
    def GET(self):
        i = web.input(name=None)
        return render.test(i.name)


class index:
    def GET(self):
        return render.index()


class testB:
    def GET(self):
        return render.TestB()


class contact:
    def GET(self):
        return render.contact()


class rank:
    def GET(self):
        i = web.input(model=None)
        if i.model == '1':
            result_list = readData.get_male_rank()
            return render.ranklist(result_list, 1)

        if i.model == '2':
            result_list = readData.get_female_rank()
            return render.ranklist(result_list, 2)

        if i.model == '3':
            result_list = readData.get_team_rank(1)
            return render.ranklistT(result_list, 1)

        if i.model == '4':
            result_list = readData.get_team_rank(2)
            return render.ranklistT(result_list, 2)

        else:
            return render.rank()


class head:
    def GET(self):
        i = web.input(playerA=None, playerB=None)

        if i.playerA is None or i.playerB is None:
            return render.head()

        else:
            data_list = HeadtoHead.head2head(i.playerA, i.playerB)
            return render.headresult(data_list)


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    app.run()

