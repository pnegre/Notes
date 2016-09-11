
var app = angular.module('app', []);
// Canviem configuració per símbols per interpolar variables
// Si no, tenim conflictes amb les templates de django
// perquè també empren "{{" i "}}"
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//');
    $interpolateProvider.endSymbol('//');
});

// Això és per enviar el csrftoken a partir de la cookie o header
// amb cada petició ajax que fem amb angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller("notesController", function($scope, $http) {
    $scope.mostraLlista = true;
    $http.get('/notes/interCursos').then(function(response) {
        $scope.av = response.data;
    });

    $scope.showCurs = function(inter, grup, assig) {
        $http.get('/notes/alumnes/' + grup.id + '/' + inter.anyid).then(function(response) {
            $scope.grup = grup;
            $scope.assignatura = assig;
            $scope.alumnes = response.data;
            $scope.mostraLlista = false;
        });
    }

    $scope.changedAlumne = function() {
        console.log($scope.selectedAlumne);
        var al = $scope.selectedAlumne;
        var as = $scope.assignatura;
        var av = $scope.av;
        var gr = $scope.grup;
        $http.get('/notes/itemsAlumne/' + av.id +'/' + al.id + '/' + as.id + '/' + gr.id).then(function(response) {
            console.log(response);
            $scope.dadesAlumne = response.data;
        });
    }
});
