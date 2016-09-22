

app.controller("butlletinsController", function($scope, $http) {
    $http.get('/notes/inters').then(function(response) {
        $scope.anys = response.data;
    });

    $scope.baixa = function() {
        console.log("dins baixa");
    }
});
