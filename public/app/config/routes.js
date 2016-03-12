app.config(["$routeProvider", function ($routeProvider) {
    "use strict";
    $routeProvider.when('/welcome', {
        controller: 'HomeController',
        controllerAs: 'vm',
        templateUrl: '../app/views/home.html',
        resolve: {}
    })
        .otherwise({redirectTo: '/welcome'});
}])
    .config(['$httpProvider', function ($httpProvider) {
        "use strict";
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        "use strict";
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);