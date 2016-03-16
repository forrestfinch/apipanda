/**
* resource Module
*
* Description
*/
app.service('Request', ['$http', 'API_URL', '$q', '$localStorage', 'promiseTracker', function ($http, API_URL, $q, $localStorage, promiseTracker) {

        this.fetch = function (endpoint, obj, method, headers) {
            // body...
            var url = API_URL + endpoint;
            var data = obj || {};
            $.extend(true, data, {
                source: 'web'
            });
            $.extend(true, headers, {
                    tracker: this.estimatingTracker
                });

            var req = {
                method: method || 'post',
                url: url,
                data: angular.toJson(data, true),
                headers: headers
            };
            var defer = $q.defer();
            $http(req).then(function (res) {
                defer.resolve(res.data);
            });
            return defer.promise;
        };
}]);