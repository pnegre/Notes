

app.controller("adminInterController", function($scope, $http) {

    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.showCursos = function() {
        $http.get('/notes/grupsInter/' + $scope.selectedInter.id).then(function(response) {
            $scope.cursos = response.data;
            console.log($scope.cursos);
        });

    }

});
