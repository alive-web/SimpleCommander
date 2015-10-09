angular.module('wwwApp')
    .factory('Games', ['$http', 'ApiUrl', function($http, ApiUrl) {
        'use strict';
        return {
            list: function() {
                return $http.get(ApiUrl + '/games');
            }
        };
    }]);