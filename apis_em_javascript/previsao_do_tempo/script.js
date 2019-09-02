
document.querySelector("body").onloadend = startMap();
var btn_visualizar = document.getElementById("btn_visualizar");
var text_field = document.getElementById("text_field");
const WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?';
const WEATHER_IMG_API_URL = 'http://openweathermap.org/img/w/';
const WEATHER_API_KEY = '&APPID=238185711cabcaded55edaf5cb55617a';
var marker;
var map;
var localInfo;

function startMap() {
    var mapProp = {
        center: new google.maps.LatLng(51.508742, -0.120850),
        zoom: 2,
    };
    map = new google.maps.Map(document.getElementById("map"), mapProp);
    
    marker = null

    google.maps.event.addListener(map, 'click', function (event) {
        
        placeMarker(map, event.latLng);
    });

   


}

function placeMarker(map, location) {
    
    if (marker)
        marker.setPosition(location);
     
    else{

        marker = new google.maps.Marker({
            position: location,
            map: map
        });
    }

    localInfo = location;
    checkWeather(location.lat(), location.lng())

}

function searchByCity(city){
    
    new google.maps.Geocoder().geocode( {'address': city}, function(results, status) {
        if (status == 'OK') {
            placeMarker(map, results[0].geometry.location);
        }
    });
    

}

function checkWeather(infoWindow, longitude, latitude){
    var metrics = '&units=metric';
    openWeatherReq("lat="+ Math.round(latitude)+"&lon=" + Math.round(longitude) + metrics, infoWindow)

}


function timeFormatter(timestamp){
    var date = new Date(timestamp * 1000)
    console.log(timestamp)
    return date.getHours() + "hr : " + date.getMinutes() + "min";
}
function setResponse(_infoWindow, jSonResponse){
  
    weatherImg = WEATHER_IMG_API_URL + jSonResponse["weather"][0]["icon"] + ".png";
    temp = jSonResponse["main"]["temp"]
    max = jSonResponse["main"]["temp_max"]
    min = jSonResponse["main"]["temp_min"]
    level = jSonResponse["main"]["grnd_level"]
    description = jSonResponse["weather"][0]["main"]
    sunrise = timeFormatter(jSonResponse["sys"]["sunrise"])
    sunset = timeFormatter(jSonResponse["sys"]["sunset"])

    _infowindow = new google.maps.InfoWindow({
        content: "Latitude: " + localInfo.lat() + 
            "<br>Longitude: " + localInfo.lng() +
            "<br>" + 

        
        "<div style='float:left'><img src='"+ weatherImg + "'>" + 
        "</div><div style='float:right; padding: 10px;'><b>"  + description + "</b>"+
        "<br/>Temperatura: " + temp + "ºC" +
        "<br/>Máxima: " + max + " ºC" +
        "<br/>Mínima: " + min + " ºC" +
        "<br><br>Nascer do sol: " + sunrise +
        "<br>Pôr do sol: " + sunset +
        "</div>"
        
        

    });
 
    _infowindow.open(map, marker);

}
function openWeatherReq(parameter, output){
    var req = new XMLHttpRequest();
    
    req.onreadystatechange = function(){
        if (req.readyState == XMLHttpRequest.DONE ){
            resp = JSON.parse(req.responseText);
            
            setResponse(output, resp)
        }
    }
    req.open('GET', WEATHER_API_URL + parameter + WEATHER_API_KEY);

    req.send(null);

   
}

btn_visualizar.onclick = function () {

    searchByCity(text_field.value);


}


