'use strict';

/**
 * @ngdoc service
 * @name attoUiApp.backendFactory
 * @description
 * # backendFactory
 * Factory in the attoUiApp.
 */
angular.module('attoUiApp')
  .factory('backendFactory', function ($http) {
    var BACK_URL = "http://martyr:5001/"
    
    var reduce_cpu = function(list) {
      var res = [];
      var temp = {}
      list = list.reverse()
      for (var i = 0; i < list.length; i++) {
        for (var j = 0; j < list[i].CPU.length; j++) {
          if (!temp[j] ) {
            temp[j] = [[list[i].epoch_milli, list[i].CPU[j]]];
          } else {
            temp[j].push([list[i].epoch_milli, list[i].CPU[j]]);
          }
        }
        if (i == list.length - 1){
          for (var j = 0; j < list[i].CPU.length; j++) {
            res.push({data: temp[j], name: 'CPU ' + j});
          }
        }
      }
      return res;
    };

    // Public API here
    return {
      get_hosts: function () {
        var res = {data:{}}
        $http({
          method: 'GET',
          url: BACK_URL + 'hosts/'
        }).then(function successCallback(response) {
            console.log(response);
            res.data = response.data;
          }, function errorCallback(response) {
            //TODO error handling
          });
        return res;
      },
      get_cpu: function (host, num, config) {
        var res = {data: []};
        config.loading = true;
        $http({
          method: 'GET',
          url: BACK_URL + 'cpu/' + host,
          params: {limit: num}
        }).then(function successCallback(response) {
            console.log(response);
            res.data = reduce_cpu(response.data);
            console.log(res.data);
            config.series = res.data;
            config.xAxis.title.text = 'Time';
            config.yAxis.title.text = 'CPU Percent';
            config.loading = false;
          }, function errorCallback(response) {
            //TODO error handling
          });
        return res;
      }

    };
  });
