angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $timeout) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('PlaylistsCtrl', function($scope, $http, $cordovaMedia, $ionicLoading, $location, pass) {
    //$http.get("http://dyn-160-39-203-93.dyn.columbia.edu:9090/show")
    $http.get("http://127.0.0.1:8000/" + "login")
      .then(function(response) {
          posts = response.data;
          $scope.playlists = [
           { author: 'Reggae', text: 1 },
           { author: 'Chill', text: 2 },
           { author: 'Dubstep', text: 3 },
           { author: 'Indie', text: 4 },
           { author: 'Rap', text: 5 },
           { author: 'Cowbell', text: 6 },
           { author: posts, text: 7 }
          ];
          //$scope.playlists = posts;

    });

    $scope.play = function(src) {
      //url = "http://ec2-54-173-9-169.compute-1.amazonaws.com:9090/audio"+"?data="+src;

    var fileTransfer = new FileTransfer();
    var uri = encodeURI("http://127.0.0.1:8000/" + "audio"+"?data="+src);
    //var fileURL = "cdvfile://localhost/persistent/path/to/downloads/tttaaaqqq.wav";
    var fileURL = "cdvfile://localhost/temporary/" + "test.mp3"

    fileTransfer.download(
        uri,
        fileURL,
        function(entry) {
            console.log("download complete: " + entry.toURL());
              var media = new Media("mp3/now.mp3", null, null, mediaStatusCallback);
              $cordovaMedia.play(media);
        },
        function(error) {
            console.log("download error source " + error.source);
            console.log("download error target " + error.target);
            console.log("upload error code" + error.code);
        },
        false,
        {
            headers: {
                "Authorization": "Basic dGVzdHVzZXJuYW1lOnRlc3RwYXNzd29yZA=="
            }
        }
    );




    //       $http.get(url)
    //         .then(function(response) {
    //           console.log(response.attachment);

    // var filePath = cordova.file.dataDirectory + 'test.wav'
    //           var fileContent = new Blob([response.data], { type : 'audio/x-wav' })
    // var options = {}

    // $cordovaFile.writeFile(filePath, fileContent, options).then(function (result) {
    //   console.log(result)
    // }, function (err) {
    //   console.error(err) // FileError { code: 5 }
    // })
    //         $cordovaFile.writeFile(cordova.file.dataDirectory, "aaa.wav", fileContent, true)
    //         .then(function (success) {
    //           console.log("aaa");
    //         }, function (error) {
    //           console.log(error);
    //         });

    //          // var media = new Media(src, null, null, mediaStatusCallback);
    //          // $cordovaMedia.play(media);
    //         });



    }

    $scope.detail = function(obj) {
        $location.path('/app/playlists/'+obj.text);
        pass.set(obj);
    }
 
    var mediaStatusCallback = function(status) {
        if(status == 1) {
            $ionicLoading.show({template: 'Loading...'});
        } else {
            $ionicLoading.hide();
        }
    }
})

.controller('PlaylistCtrl', function($scope, $stateParams, pass) {
    console.log(pass.get().text);
    $scope.obj = pass.get();
});

document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
    console.log(FileTransfer);
    console.log("asdkjfkdsskfksfkjkj");
}


