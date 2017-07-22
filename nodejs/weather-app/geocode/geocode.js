const request = require('request');

var gecodeAddress = (address, callback) =>{
    encodedAddress = encodeURIComponent(address);

    request({
        url: `http://maps.googleapis.com/maps/api/geocode/json?address=${encodedAddress}`,
        json: true
    }, (error, response, body) => {
        if(error){
            callback('Unable to connect to Google servers');
        }else if (body.status === "ZERO_RESULTS") {
            callback('Unable to find that address');
        }else{
            callback(undefined, {
                'address': body.results[0].formatted_address,
                'lat': body.results[0].geometry.location.lat,
                'lng': body.results[0].geometry.location.lng
            });
        }
    });
};

module.exports.gecodeAddress = gecodeAddress;
