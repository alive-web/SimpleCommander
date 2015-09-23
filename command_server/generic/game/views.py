from generic.base import JSONBaseView
from generic.game import REGISTERED_GAMES
from generic.routes import url_route


@url_route('/games')
class GameListView(JSONBaseView):

    def get(self, request):
        return REGISTERED_GAMES


@url_route('/game/{slug:\w+}')
class GameInfoView(JSONBaseView):

    def get(self, request, slug):
        return REGISTERED_GAMES[slug].info()