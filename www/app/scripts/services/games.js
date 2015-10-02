angular.module('wwwApp')
    .factory('Games', ['$http', 'ApiUrl', function($http, ApiUrl) {
        return {
            list: function() {
                return $http.get(ApiUrl + '/games')
            }
        }
    }]);