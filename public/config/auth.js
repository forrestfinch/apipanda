app.factory('Auth', ['$sessionStorage', '$localStorage', 'Request', '$window', function($sessionStorage, $localStorage, Request, $window) {
    return {
        getAuth: function (auth) {
            // body...
            return $sessionStorage.get(auth);
        },
        $login: function (email, password) {
            // body...
            var endpoint = 'user/login';
            var payload = {
                email: email,
                password: password
            }
            Request.fetch(endpoint, payload)
                .then(function (status, result) {
                    console.log(status, result);
                }, function (code, err) {
                    // body...
                    console.log(code, err);
                });
        },
        $onAuth: function (cb) {
            // body...
            return !!cb;
        },
        $logout: function () {
            // body...
            var endpoint = 'user/logout';
            var payload = {};
            Request.fetch(endpoint, payload, method='get')
                .then(function (status, result) {
                    $localStorage.$reset();
                    $sessionStorage.$reset();
                    $window.location = '/';
                }, function (code, err) {
                    // body...
                    console.log(code, err);
                });
        }
    }
  }]);