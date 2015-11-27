var app = angular
	.module('StarterApp', ['ngMaterial'])
	.config(function($mdThemingProvider) {
	  $mdThemingProvider.theme('default')
	    .primaryPalette('teal', {'hue-3':'50'})
	    .accentPalette('indigo');
	});

app.controller('AppCtrl', ['$scope', '$mdSidenav', '$mdDialog', function($scope, $mdSidenav, $mdDialog){
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  $scope.showDetails = function(e, id, pic){
  	var tgt = angular.element(document.body);
    $mdDialog.show({
      parent      : tgt,
      targetEvent : e,
      controller  : LoopDetailsController,
      templateUrl : "./app/details.html",
      clickOutsideToClose: true,
      locals: {
        details: {picture:pic, houseid:id}
      }
    })
    .then(function() {
      console.log();
    }, function() {/*If cancel*/});
  }

  $scope.housing = [
    {id:1541706, title:"Castle", picture:"castle-1541706.jpg", price:80000, rooms:8, rating:4, description:"", type:"castle"},
    {id:1229278, title:"Culzean Castle", picture:"culzean-castle-1229278.jpg", price:80000, rooms:8, rating:4, description:"", type:"castle"},
    {id:1541706, title:"English Cottage", picture:"english-cottage-1515517.jpg", price:80000, rooms:8, rating:4, description:"", type:"cottage"},
    {id:1541706, title:"Brick Cottage", picture:"english-cottage-1530299.jpg", price:80000, rooms:8, rating:4, description:"", type:"cottage"},
    {id:1541706, title:"Gamwell House", picture:"gamwell-house-1-1522150.jpg", price:80000, rooms:8, rating:4, description:"", type:"mansion"},
    {id:1541706, title:"Suburb house", picture:"house-2-1232910.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Manoir", picture:"house-1568654.jpg", price:80000, rooms:8, rating:4, description:"", type:"mansion"},
    {id:1541706, title:"American house", picture:"house-i-1491881.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Irish House", picture:"irish-house-1230601.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Japanese Wooden", picture:"japanese-wooden-construction-1-1221461.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Kanazawa Castle", picture:"kanazawa-castle-1228651.jpg", price:80000, rooms:8, rating:4, description:"", type:"castle"},
    {id:1541706, title:"Old house", picture:"old-house-1234407.jpg", price:80000, rooms:8, rating:4, description:"", type:"mansion"},
    {id:1541706, title:"Nice house", picture:"no_pic.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"The Big House", picture:"the-big-house-1528919.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Victorian House", picture:"victorian-houses-4-1233917.jpg", price:80000, rooms:8, rating:4, description:"", type:"house"},
    {id:1541706, title:"Woodland cottage", picture:"woodland-cottage-1223028.jpg", price:80000, rooms:8, rating:4, description:"", type:"castle"}
  ];

  $scope.filterHC = function(item){
    return (item.type == 'cottage' || item.type == 'house');
  }
 
}]);


function LoopDetailsController($scope, $mdDialog, details) {
  $scope.details = details;
  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
}