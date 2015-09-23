import asyncio
from aiohttp.web_exceptions import HTTPNotFound

from generic.base import JSONBaseView, RedirectView
from generic.game import REGISTERED_GAMES
from generic.game.rooms import Room
from generic.routes import url_route


@url_route('/games')
class GameListView(JSONBaseView):

    @asyncio.coroutine
    def get(self, request):
        return [game.info() for game in REGISTERED_GAMES.values()]


@url_route('/game/{slug:\w+}')
class GameInfoView(JSONBaseView):

    @asyncio.coroutine
    def get(self, request, slug):
        if slug in REGISTERED_GAMES:
            return REGISTERED_GAMES[slug].info()
        else:
            raise HTTPNotFound


@url_route('/game/{slug:\w+}/start')
class GameStartView(RedirectView):

    @asyncio.coroutine
    def get(self, request, slug, *args, **kwargs):
        room = Room.start_new(slug)
        return '/r/{}'.format(room.id)
