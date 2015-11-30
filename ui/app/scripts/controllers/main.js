'use strict';

/**
 * @ngdoc function
 * @name attoUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the attoUiApp
 */
angular.module('attoUiApp')
  .controller('MainCtrl', function ($scope, backendFactory) {
    $scope.hosts = backendFactory.get_hosts();
    $scope.test = "Hello";
    $scope.buffer = {selected_data: {data: []}}

    $scope.selected = {
      host:"",
      time: 600
    }

    $scope.ranges = {
      "1 Minute": 60,
      "10 Minutes": 600,
      "15 Minutes": 900,
      "30 Minutes": 1800,
      "1 Hour": 3600
    }
    
    $scope.chartConfig = {
        options: {
            chart: {
                type: 'line',
                zoomType: 'x'
            },
            tooltip: {
                formatter: function() {
                    return  '<b>' + this.series.name +'</b><br/>' +
                        Highcharts.dateFormat('%m/%d/%Y - %H:%M:%S', new Date(this.x)) + ' ' + this.y + '%';
                }
            }
        },
        series: [],
        title: {
            text: ''
        },
        xAxis: { title: {text:''}, type: 'datetime'},
        yAxis: { title: {text:''} },
        loading: false
    }
  
    $scope.plot = function() {
      $scope.chartConfig.title.text = $scope.selected.host;
      backendFactory.get_cpu($scope.selected.host, $scope.selected.time, $scope.chartConfig);
    }

  });
