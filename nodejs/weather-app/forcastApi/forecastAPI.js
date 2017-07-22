const request = require('request');

var forecast = (lat, lng, callback) => {
    forecastAPIUrl = `https://api.darksky.net/forecast/108a24c94c0f1a800ae311dc19332a45/${lat},${lng}`;
    request({
        url: forecastAPIUrl,
        json: true}, (error, response, body) => {
            if(error){
                callback('Unable to connect to forcastAPI servers');
            }else if (response.statusCode !== 200) {
                callback(response.body);
            }else{
                // console.log(body.currently);
                callback(undefined, {
                      'temperature': body.currently.temperature,
                      'apparentTemperature': body.currently.apparentTemperature
                });
            }
        });
};

module.exports.forecast = forecast;
