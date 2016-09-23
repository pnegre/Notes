

app.controller("butlletinsController", function($scope, $http) {
    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.showCursos = function() {
        $http.get('/notes/interCursos/' + $scope.selectedInter.id).then(function(response) {
            $scope.cursos = response.data;
        });
    }

    $scope.prepareLink = function() {
        $scope.link = '/notes/butlletiPDF/' + $scope.selectedInter.id + '/' + $scope.selectedCurs.id;
    }

    $scope.baixa = function() {
        console.log("dins baixa");
    }
});
