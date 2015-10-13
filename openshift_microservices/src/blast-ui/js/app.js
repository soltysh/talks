(function() {
    var app = angular.module('blast-ui', [])

    app.controller('BlastUIController', ['$http', function($http) {
        this.searchText = '';
        this.texts = {};
        this.images = {};
        this.videos = {};


        var store = this;
        this.search = function() {
            store.texts = {};
            store.images = {};
            store.videos = {};

            textURL = 'http://blast-text.test.svc.cluster.local:8080/blast/api/v1.0/text/' + encodeURIComponent(store.searchText);
            $http.get(textURL).success(function(data){
                store.texts = data;
            });

            imagesURL = 'http://blast-image.test.svc.cluster.local:8080/blast/api/v1.0/image/' + encodeURIComponent(store.searchText);
            $http.get(imagesURL).success(function(data){
                store.images = data;
            });

            videosURL = 'http://blast-video.test.svc.cluster.local:8080/blast/api/v1.0/video/' + encodeURIComponent(store.searchText);
            $http.get(videosURL).success(function(data){
                store.videos = data;
            });

        }
        this.noResults = function() {
            return store.texts.length == 0 && store.images.length == 0 && store.videos.length == 0;
        }
    }]);
})();
