const request = require('request');

var gecodeAddress = (address) => {
    return new Promise((resolve, reject) => {
        encodedAddress = encodeURIComponent(address);

        request({
            url: `http://maps.googleapis.com/maps/api/geocode/json?address=${encodedAddress}`,
            json: true
        }, (error, response, body) => {
            if(error){
                reject('Unable to connect to Google servers');
            }else if (body.status === "ZERO_RESULTS") {
                reject('Unable to find that address');
            }else{
                resolve({
                    'address': body.results[0].formatted_address,
                    'lat': body.results[0].geometry.location.lat,
                    'lng': body.results[0].geometry.location.lng
                });
            }
        });
    });
};

gecodeAddress('bengaluru').then((res) => {
    console.log(JSON.stringify(res, undefined, 2));
}).catch((errorMessage) => {
    console.log(errorMessage);
});
