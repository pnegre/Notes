

app.controller("butlletinsController", function($scope, $http) {
    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.changeAny = function() {
        $scope.link = null;
        $scope.cursos = null;
        $scope.selectedInter = null;
        $scope.selectedCurs = null;
    }

    $scope.showCursos = function() {
        $http.get('/notes/interCursos/' + $scope.selectedInter.id).then(function(response) {
            $scope.cursos = response.data;
            $scope.link = null;
        });
    }

    $scope.prepareLink = function() {
        if ($scope.selectedInter != null && $scope.selectedCurs != null) {
            $scope.link = '/notes/butlletiPDF/' + $scope.selectedInter.id + '/' + $scope.selectedCurs.id;
        }
    }
});
