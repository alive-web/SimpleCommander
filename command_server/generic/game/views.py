import asyncio
from aiohttp.web_exceptions import HTTPNotFound

from generic.base import JSONBaseView, RedirectView, WebSocketView
from generic.game import REGISTERED_GAMES
from generic.game.rooms import Room, OPENED_ROOMS
from generic.routes import url_route


@url_route('/games')
class GameListView(JSONBaseView):

    @asyncio.coroutine
    def get(self, request):
        return [game.info() for game in REGISTERED_GAMES.values()]


@url_route('/games/{slug:\w+}')
class GameInfoView(JSONBaseView):

    @asyncio.coroutine
    def get(self, request, slug):
        if slug in REGISTERED_GAMES:
            return REGISTERED_GAMES[slug].info(True)
        else:
            raise HTTPNotFound


@url_route('/game/{slug:\w+}/start')
class GameStartView(RedirectView):

    @asyncio.coroutine
    def get(self, request, slug, *args, **kwargs):
        room = Room.start_new(slug)
        return '/r/{}'.format(room.id)


@url_route('/r/{room_id:[a-z,0-9,-]+}')
class RoomView(JSONBaseView):

    @asyncio.coroutine
    def get(self, request, room_id):
        return {'ws': '/r/{}/ws'.format(room_id)}


@url_route('/r/{room_id:[a-z,0-9,-]+}/ws')
class RoomWSView(WebSocketView):

    @asyncio.coroutine
    def dispatch(self, request, room_id, *args, **kwargs):
        if room_id in OPENED_ROOMS:
            self.room = OPENED_ROOMS[room_id]
            self.room.game.transport = self
            yield from super().dispatch(request, *args, **kwargs)
        else:
            raise HTTPNotFound

    def on_message(self, msg):
        self.send(msg)