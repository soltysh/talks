(function() {
    var app = angular.module('blast-ui', [])

    app.controller('BlastUIController', ['$http', function($http) {
        this.searchText = '';
        this.texts = {};
        this.images = {};
        this.videos = {};


        var store = this;
        this.search = function() {
            textURL = 'http://localhost:8000/blast/api/v1.0/text/' + encodeURIComponent(store.searchText);
            $http.get(textURL).success(function(data){
                store.texts = data;
            });

            imagesURL = 'http://localhost:8000/blast/api/v1.0/image/' + encodeURIComponent(store.searchText);
            $http.get(imagesURL).success(function(data){
                store.images = data;
            });

            videosURL = 'http://localhost:8000/blast/api/v1.0/video/' + encodeURIComponent(store.searchText);
            $http.get(videosURL).success(function(data){
                store.videos = data;
            });

        }
        this.noResults = function() {
            return store.texts.length == 0 && store.images.length == 0 && store.videos.length == 0;
        }
    }]);
})();