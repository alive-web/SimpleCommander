import json


class BaseView(object):

    def get(self, request, params=None):
        return json.dumps([]).encode('utf_8')

    def post(self, request, params=None):
        return json.dumps([]).encode('utf_8')

    def put(self, request, params=None):
        return json.dumps([]).encode('utf_8')

    def delete(self, request, params=None):
        return json.dumps([]).encode('utf_8')


ROUTES = {r'/': BaseView,
          r'/test': BaseView}