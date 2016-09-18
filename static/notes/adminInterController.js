

app.controller("adminInterController", function($scope, $http) {

    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
        console.log(response);
    });

    // $scope.anys = [
    //     { 'nom': '2015-2016', 'id': 1, 'inters': [
    //         {'nom': 'inter1', 'id': 1},
    //         {'nom': 'inter2', 'id': 2},
    //     ]},
    //     { 'nom': '2016-2017', 'id': 2, 'inters': [
    //         {'nom': 'inter11', 'id': 3},
    //         {'nom': 'inter22', 'id': 4},
    //     ]},
    // ];

    $scope.showInters = function() {
        console.log("Dins showInters");
        console.log($scope.selectedAny);
    }

});
