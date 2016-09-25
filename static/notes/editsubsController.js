

app.controller("editsubsController", function($scope, $http) {
    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.changeAny = function() {
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

    $scope.showSubmateries = function() {
        $http.get('/notes/submatsInter/' + $scope.selectedInter.id + "/" + $scope.selectedCurs.id).then(function(response) {
            $scope.submats = response.data;
        });
    }

    $scope.desaSubmats = function() {
        $http.post('/notes/submatsPost', $scope.submats).then(function(response) {
            var i=0;
            for(i=0; i<$scope.submats.length; i++) {
                $scope.submats[i].changed = false;
            }
        });
    }
});
