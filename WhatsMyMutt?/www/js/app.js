// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic'])

/**.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider
      .state('tabs', {
        url: "/tab",
        abstract: true,
        templateUrl: "templates/tabs.html"
      })
      .state('tabs.dogs', {
        url: "/dogs",
        views: {
          'dogs-tab': {
            templateUrl: "templates/dogs.html",
            controller: 'DogsTabCtrl'
          }
        }
      })
      .state('tabs.nondogs', {
        url: "/nondogs",
        views: {
          'non-dogs-tab': {
            templates: "templates/nondogs.html"
          }
        }
      });

      $urlRouterProvider.otherwise("/tab/dogs");
})**/

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
});

function takePicture() {
  //alert("in takePicture()");
  navigator.camera.getPicture(onSuccess, onFail, {quality: 70, destinationType: Camera.DestinationType.FILE_URI, correctOrientation: true});
  //alert("after navigator");
}

function selectPicture() {
  //alert("in selectPicture()");
  navigator.camera.getPicture(onSuccess, onFail, {quality: 70, destinationType: Camera.DestinationType.FILE_URI, sourceType: Camera.PictureSourceType.PHOTOLIBRARY, correctOrientation: true});
}

var imagesrc = "";

function analyzePicture(fname) {
  var fileURL = imagesrc;
  document.getElementById("buttonBar").style.display = "block";
  document.getElementById("response").innerHTML = "Analyzing image.  Please wait.";
  var options = new FileUploadOptions();
  options.fileKey = "imagefile";
  options.fileName = fileURL.substr(fileURL.lastIndexOf('/') + 1);
  options.mimeType = "text/plain";

  var params = {};
  params.value1 = "test";
  params.value2 = "param";

  options.params = params;
  var ft = new FileTransfer();
  ft.upload(fileURL, encodeURI("http://192.168.29.253:5000/"+fname), win, fail, options);
}

var win = function (r) {
    console.log("Code = " + r.responseCode);
    //document.getElementById("response").className= "item tabs tabs-secondary";
    document.getElementById("response").innerHTML= r.response;
    console.log("Sent = " + r.bytesSent);
}

var fail = function (error) {
    alert("An error has occurred: Code = " + error.code);
    console.log("upload error source " + error.source);
    console.log("upload error target " + error.target);
}

function onSuccess(imageURI) {
  var image = document.getElementById('image');
  image.src = imageURI;
  imagesrc = imageURI;
  image.style.display = 'block';
}

function onFail(message) {
  alert('Failed because: ' + message);
}


