(function() {
    var app = angular.module('blast-ui', [])

    app.controller('BlastUIController', ['$http', function($http) {
        this.search = '';
        this.texts = {};
        this.images = {};
        this.videos = {};


        var store = this;
        this.search = function() {
            url = 'http://localhost:8000/blast/api/v1.0/text/openshift';
            $http.get(url).success(function(data){
                store.texts = data.items;
            });
        }

    }]);
})();
