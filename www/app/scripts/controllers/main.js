'use strict';

/**
 * @ngdoc function
 * @name wwwApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the wwwApp
 */
angular.module('wwwApp')
  .controller('MainCtrl', function ($scope, Games) {
    Games.list().then(
      function(data) {
        $scope.games = data;
      }
    );
  });
