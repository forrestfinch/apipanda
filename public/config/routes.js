app.config(["$routeProvider", '$locationProvider', function ($routeProvider, $locationProvider) {
    "use strict";
    $locationProvider.html5Mode(true);

    $routeProvider.when('/', {
        controller: 'HomeController',
        controllerAs: 'vm',
        templateUrl: '../home/'
    })
        .when('/hubs', {
            controller: 'HubsController',
            controllerAs: 'vm',
            templateUrl: '../hubs/'
        })
        .when('/login', {
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '../login/'
        })
        .when('/signup', {
            controller: 'RegisterController',
            controllerAs: 'vm',
            templateUrl: '../register/'
        })
        .when('/reset', {
            controller: 'ResetController',
            controllerAs: 'vm',
            templateUrl: '../reset/'
        })

        .whenAuthenticated('/dashboard', {
            controller: 'DashController',
            controllerAs: 'vm',
            templateUrl: '../dashboard/'
        })

        .whenAuthenticated('/dashboard/hubs/:hubId', {
            controller: 'HubController',
            controllerAs: 'vm',
            templateUrl: '../hub/'
        })

        .whenAuthenticated('/dashboard/orgs/:ordId', {
            controller: 'OrgController',
            controllerAs: 'vm',
            templateUrl: '../orgs/'
        })

        .whenAuthenticated('/dashboard/workspaces/:workspaceId', {
            controller: 'WorkspaceController',
            controllerAs: 'vm',
            templateUrl: '../workspaces/'
        })

        .whenAuthenticated('/dashboard/plugins', {
            controller: 'PluginController',
            controllerAs: 'vm',
            templateUrl: '../plugins/'
        })

        .whenAuthenticated('/profile', {
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: '../profile/'
        })

        .otherwise({redirectTo: '/'});
}])
    .config(['$httpProvider', function ($httpProvider) {
        "use strict";
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])
    .config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = false;
    }])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        "use strict";
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }])
    .config(['$localStorageProvider', function ($localStorageProvider) {
        "use strict";
        $localStorageProvider.setKeyPrefix('panda');
    }]);