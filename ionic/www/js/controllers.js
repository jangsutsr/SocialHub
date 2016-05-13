var serverURL = 'http://ec2-54-173-9-169.compute-1.amazonaws.com:9090';

angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $ionicPopup, $http) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Form data for the login modal
  $scope.loginData = {};
  $scope.registerData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.loginmodal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.loginmodal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.loginmodal.show();
  };

  $scope.logout = function() {
     // A confirm dialog
     var confirmPopup = $ionicPopup.confirm({
       title: 'Confirm Logout',
       template: 'Are you sure you want to logout?'
     });

     confirmPopup.then(function(res) {
       if(res) {
        $http.get(serverURL+"/logout")
          .then(function(response) {
            $scope.IsLoggedIn = false;
        });  
       } 
     });
  }

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    $http({
      method: 'POST',
      url: serverURL+'/login',
      data: $scope.loginData
    }).then(function successCallback(response) {
        var alertPopup = $ionicPopup.alert({
           title: 'Success',
           template: 'Successfully Login!'
        });

        alertPopup.then(function(res) {
          $scope.closeLogin();
        });
        $scope.IsLoggedIn = true;

      }, function errorCallback(response) {
        var alertPopup = $ionicPopup.alert({
           title: 'Error',
           template: response.data
        });
      });

  };

  // Create the register modal
  $ionicModal.fromTemplateUrl('templates/newuser.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.registermodal = modal;
  });

  $scope.closeRegister = function() {
    $scope.registermodal.hide();
  };

  $scope.Register = function() {
    $scope.registermodal.show();
  };

  $scope.doRegister = function() {
    $http({
      method: 'POST',
      url: serverURL+'/register',
      data: $scope.registerData
    }).then(function successCallback(response) {
        var alertPopup = $ionicPopup.alert({
           title: 'Success',
           template: 'Successfully Create the New User!'
        });

        alertPopup.then(function(res) {
          $scope.closeRegister();
          $scope.login();
        });

      }, function errorCallback(response) {
        var alertPopup = $ionicPopup.alert({
           title: 'Error',
           template: response.data
        });
    });

  };
})

.controller('PlaylistsCtrl', function($scope, $http, $cordovaMedia, $ionicLoading, $location, pass, $state) {
    console.log($state.current.name);
    if ($state.current.name == 'app.playlists'){
      $http.get(serverURL+"/history/0")
        .then(function(response) {
            $scope.playlists = response.data;
            for (var i = $scope.playlists.length - 1; i >= 0; i--) {
              var msg = $scope.playlists[i].message;
              if (msg.indexOf("https://")!=-1){
                $scope.playlists[i].url = msg.substring(msg.indexOf("https://"));
                $scope.playlists[i].message = msg.substring(0, msg.indexOf("https://"));
                $scope.playlists[i].hasLink = true;
              }
              else
                $scope.playlists[i].hasLink = false;
            }
            console.log($scope.playlists);
      });  
    } else if ($state.current.name == 'app.newpost') {
      $http.get(serverURL+"/show")
        .then(function(response) {
            $scope.newposts = response.data;
            if ($scope.newposts.length>0) 
              $scope.HaveNewPost = true;
            else
              $scope.HaveNewPost = false;
            console.log($scope.HaveNewPost);
      });
    } else {
      $http.get(serverURL+"/favorite/0")
        .then(function(response) {
            $scope.favoposts = response.data;
      });  
    }

    $scope.options =  [{
        "name" : "Category Filter",
        "value": ""
      },
      {
        "name" : "Technology",
        "value": "Technology"
      },
      {
        "name" : "Sport",
        "value": "Sport"
      },
      {
        "name" : "Science",
        "value": "Science"
      },
      {
        "name" : "News",
        "value": "News"
      },
      {
        "name" : "Music",
        "value": "Music"
      },
      {
        "name" : "Other",
        "value": "Other"
      }];

    $scope.play = function(src) {
      console.log(src.message);
      url = serverURL+"/audio?data="+src.message;

    var fileTransfer = new FileTransfer();
    var uri = encodeURI(url);
    var fileURL = "cdvfile://localhost/temporary/" + "test.mp3"

    fileTransfer.download(
        uri, fileURL,
        function(entry) {
            console.log("download complete: " + entry.toURL());
              var media = new Media("cdvfile://localhost/temporary/test.mp3", null, null, mediaStatusCallback);
              $cordovaMedia.play(media);
        },
        function(error) {
            console.log("download error source " + error.source);
            console.log("download error target " + error.target);
            console.log("upload error code" + error.code);
        }, false,
        {
            headers: {
                "Authorization": "Basic dGVzdHVzZXJuYW1lOnRlc3RwYXNzd29yZA=="
            }
        }
    );

    }

    $scope.playall = function(all) {
      console.log(all);
      src = "";
      for (var i = 3; i <= Math.min(4, all.length-1); i++) {
        src = src + all[i].message + ". . . ";
      }
      console.log(src);
      $scope.play({'message':src});
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
.controller('ProfileCtrl', function($scope, $http, $window) {
  $scope.TwitterAttach = function() {
    $http.get(serverURL+"/attach/twitter")
      //$http.get("http://127.0.0.1:8000/" + "login")
        .then(function(response) {
          console.log(response.data);
          var url = 'https://api.twitter.com/oauth/authenticate?oauth_token='+response.data;
          //$window.location.href = 'http://localhost:5000/surround';
          //$http.get('http://www.google.com');
          window.cordova.InAppBrowser.open(url, "_blank", 'location=no');
    });
  };
})

.controller('FriendsCtrl', function($scope, $http, $ionicPopup, $state) {

    $scope.ttlist = [];
    $scope.fblist = [];
    $http.get(serverURL+"/friends")
        .then(function(response) {
          var friendslist = response.data;
          for (var i = friendslist.length - 1; i >= 0; i--) {
            if (friendslist[i].category=='twitter')
              $scope.ttlist.push(friendslist[i]);
            else
              $scope.fblist.push(friendslist[i]);
          }
          for (var i = $scope.ttlist.length - 1; i >= 0; i--) 
            $scope.ttlist[i].selected = !$scope.ttlist[i].is_favorite;
          for (var i = $scope.fblist.length - 1; i >= 0; i--) 
            $scope.fblist[i].selected = !$scope.fblist[i].is_favorite;
    });

    $scope.count = function() {
      var newfavo = [];
      for (var i = $scope.ttlist.length - 1; i >= 0; i--) {
        if ($scope.ttlist[i].selected){
          newfavo.push({'category':$scope.ttlist[i].category, 'social_id':$scope.ttlist[i].social_id});
        }
      }
      for (var i = $scope.fblist.length - 1; i >= 0; i--) {
        console.log($scope.fblist[i].selected);
        if ($scope.fblist[i].selected){
          newfavo.push({'category':$scope.fblist[i].category, 'social_id':$scope.fblist[i].social_id});
        }
      }
      console.log(newfavo);

      $http({
        method: 'POST',
        url: serverURL+'/friends',
        data: newfavo
      }).then(function successCallback(response) {
          var alertPopup = $ionicPopup.alert({
             title: 'Success',
             template: 'Successfully Update the Friends List!'
          });
        }, function errorCallback(response) {
          var alertPopup = $ionicPopup.alert({
             title: 'Error',
             template: response.data
          });
      });

    };
})

.controller('PlaylistCtrl', function($window, $scope, $stateParams, pass, $http, $cordovaMedia, $ionicLoading) {

    var obj = pass.get();

    $http.get(serverURL+"/sentiment?data="+obj.message)
      .then(function(response) {
      obj.img = response.data + Math.floor((Math.random() * 4) + 1).toString();
      $scope.obj = obj;
    });  

    $scope.play = function(src) {
      console.log($scope.obj.message);
      url = serverURL+"/audio?data="+$scope.obj.message;

      var fileTransfer = new FileTransfer();
      var uri = encodeURI(url);
      var fileURL = "cdvfile://localhost/temporary/" + "test.mp3"

      fileTransfer.download(
          uri, fileURL,
          function(entry) {
              console.log("download complete: " + entry.toURL());
                var media = new Media("cdvfile://localhost/temporary/test.mp3", null, null, mediaStatusCallback);
                $cordovaMedia.play(media);
          },
          function(error) {
              console.log("download error source " + error.source);
              console.log("download error target " + error.target);
              console.log("upload error code" + error.code);
          }, false,
          {
              headers: {
                  "Authorization": "Basic dGVzdHVzZXJuYW1lOnRlc3RwYXNzd29yZA=="
              }
          }
    );

      var mediaStatusCallback = function(status) {
          if(status == 1) {
              $ionicLoading.show({template: 'Loading...'});
          } else {
              $ionicLoading.hide();
          }
      }

    }

    $scope.readmore = function(obj) {
        console.log($scope.obj.url);
        window.cordova.InAppBrowser.open(obj.url, "_blank", 'location=no');
    }

});


document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
    console.log(FileTransfer);
    console.log("asdkjfkdsskfksfkjkj");
}


