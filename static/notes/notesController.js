

app.controller("notesController", function($scope, $http) {
    $scope.mostraLlista = true;
    $http.get('/notes/interActivaCursos').then(function(response) {
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
        var al = $scope.selectedAlumne;
        var as = $scope.assignatura;
        var av = $scope.av;
        var gr = $scope.grup;
        $http.get('/notes/itemsAlumne/' + av.id +'/' + al.id + '/' + as.id + '/' + gr.id).then(function(response) {
            $scope.dadesAlumne = response.data;
            $scope.desaMsg = "Desa les dades";
        });
    }

    $scope.desa = function() {
        var al = $scope.selectedAlumne;
        var as = $scope.assignatura;
        var av = $scope.av;
        var gr = $scope.grup;
        var dades = $scope.dadesAlumne;

        // console.log(dades);
        var notes = []
        var index = 0;
        for (index=0; index < dades.notes.length; ++index) {
            var nota = dades.notes[index];
            var notaSelected = nota.notaSelected;
            if (notaSelected == null) {
                notes.push({'tipnota': nota.tipnota.id, 'nota': null});
            } else {
                notes.push({'tipnota': nota.tipnota.id, 'nota': notaSelected.id});
            }
        }

        var data = {
            'comentari': dades.comentari,
            'inter': av.id,
            'assignatura': as.id,
            'alumne': al.id,
            'notes': notes,
        }

        // console.log(data);

        $scope.showWait = true;

        $http.post("/notes/postNotes", data).then(function(response) {
            // alert("Notes desades");
            $scope.desaMsg = "Dades DESADES!";
            $scope.showWait = false;
        });
    }

    $scope.clear = function() {
        $scope.dadesAlumne.comentari = "";
        var index = 0;
        for(index=0; index < $scope.dadesAlumne.notes.length; index++) {
            $scope.dadesAlumne.notes[index].notaSelected = null;
        }
        $scope.desaMsg = "Desa les dades";
    }

    $scope.chg = function() {
        // console.log("Dins chg");
        $scope.desaMsg = "Desa les dades";
    }

    $scope.insereixComentari = function() {
        $scope.dadesAlumne.comentari += $scope.comentariGeneric + ". ";
    }
});
