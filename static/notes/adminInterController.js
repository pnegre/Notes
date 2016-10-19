

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

            $http.get('/notes/tipnotesInter/' + $scope.selectedInter.id).then(function(response) {
                $scope.tipnotes = response.data;
                $scope.selectedTipNotes = [];
                for(var i=0; i<$scope.tipnotes.length; i++) {
                    if ($scope.tipnotes[i].selected == true) {
                        $scope.selectedTipNotes.push($scope.tipnotes[i]);
                    }
                }
            });

            $http.get('/notes/comentarisInter/' + $scope.selectedInter.id).then(function(response) {
                $scope.comgenerics = response.data;
                $scope.selectedComs = [];
                for(var i=0; i<$scope.comgenerics.length; i++) {
                    if ($scope.comgenerics[i].selected == true) {
                        $scope.selectedComs.push($scope.comgenerics[i]);
                    }
                }
            });
        } else {
            $scope.cursos = null;
        }
    }

    $scope.desaCursos = function() {
        var data = {'inter': $scope.selectedInter.id,
            'cursos': $scope.cursos,
            'tipnotes': $scope.selectedTipNotes,
            'comentaris': $scope.selectedComs
        }
        $http.post('/notes/saveInter', data).then(function() {
            alert("Ok, dades desades");
        });
    }

});
