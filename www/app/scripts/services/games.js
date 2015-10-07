'use strict';

angular.module('wwwApp')
    .factory('Games', ['$http', '$q', 'ApiUrl', function($http, $q, ApiUrl) {
        var _manifestCache = {}, _gamesCache = {};
        return {
            list: function() {
                var deferred = $q.defer();
                var self = this;
                $http.get(ApiUrl + '/games').success(
                    function(data) {
                        data.map(function (game) {
                            _gamesCache[game.slug] = game;
                            self.loadManifest(game.slug);
                        });

                        deferred.resolve(_gamesCache);
                    }
                );
                return deferred.promise;
            },
            loadManifest: function(gameSlug) {
                var self = this;
                if (!_manifestCache[gameSlug]) {
                    $http.get('/game_resources/' + gameSlug + '/www/manifest.json').success(
                        function (manifest) {
                            _manifestCache[gameSlug] = self.postProcessManifest(gameSlug, manifest);
                            _gamesCache[gameSlug].manifest = manifest;
                        }
                    );
                } else {
                    _gamesCache[gameSlug].manifest = _manifestCache[gameSlug];
                }
            },
            postProcessManifest: function(gameSlug, manifest) {
                manifest.favicon = '/game_resources/' + gameSlug + '/www/' + manifest.favicon;
                return manifest;
            }
        };
    }]);