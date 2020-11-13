var code = "c26131";

var mymap = L.map('mapid').setView([42.579, -76.1], 7);
var geojson;

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibGlob25neXUwODA3IiwiYSI6ImNqbTg3b2JjaDRvM2UzcHA0N3JtazAzbGkifQ.7tx-hdtzk-BWPjAjyjfKWQ'
}).addTo(mymap);

function getColor(d) {
    return d == undefined ? '#808080' :
        d > 0.7 ? '#fee8c8' :
        d > 0.4 ? '#fdbb84' :
        '#e34a33';
}

function readValue(zipcode) {
    var ans = null;
    $.ajax({
        url: `http://127.0.0.1:8000/${code}.json`,
        dataType: 'json',
        async: false,
        success: function(data) {
            ans = data[0][parseInt(zipcode)];
        }
    });
    return getColor(ans);
}

function style(feature) {
    return {
        fillColor: readValue(feature.properties.ZIP_CODE),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.9
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    mymap.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

// $.getJSON("http://127.0.0.1:8000/ny.geojson", function(data) {
//     geojson = L.geoJSON(data, {
//         style: style,
//         onEachFeature: onEachFeature
//     });
//     geojson.addTo(mymap);
// });

// var info = L.control();

// info.onAdd = function(map) {
//     this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
//     this.update();
//     return this._div;
// };

// // method that we will use to update the control based on feature properties passed
// info.update = function(props) {
//     this._div.innerHTML = (props ?
//         '<b>' + props.ZIP_CODE + '</b><br />' + '<b>' + props.PO_NAME + '</b>' : '');
// };

// info.addTo(mymap);

// $('#mapModal').on('show.bs.modal', function() {
//     setTimeout(function() {
//         mymap.invalidateSize();
//     }, 1000);
// });