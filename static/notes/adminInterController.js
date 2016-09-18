

app.controller("adminInterController", function($scope, $http) {

    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.showCursos = function() {
        console.log($scope.selectedInter);
        if ($scope.selectedInter != null) {
            $http.get('/notes/grupsInter/' + $scope.selectedInter.id).then(function(response) {
                $scope.cursos = response.data;
            });
        } else {
            $scope.cursos = null;
        }
    }

    $scope.desaCursos = function() {
        var data = {'inter': $scope.selectedInter.id, 'cursos': $scope.cursos}
        $http.post('/notes/saveInter', data).then(function() {

        });
    }

});
