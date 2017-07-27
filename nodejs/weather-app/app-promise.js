const yargs = require('yargs');
const axios = require('axios');

var argv = yargs
.options({
    a: {
        demand: true,
        alias: 'address',
        describe: 'address to weather for',
        string: true
    }
})
.help()
.alias('help', 'h')
.argv;

encodedAddress = encodeURIComponent(argv.address);

url = `http://maps.googleapis.com/maps/api/geocode/json?address=${encodedAddress}`;

axios.get(url).then( (response) => {
    console.log(response.data.results[0].formatted_address);
    var lat = response.data.results[0].geometry.location.lat;
    var lng = response.data.results[0].geometry.location.lng;
    var weatherUrl = `https://api.darksky.net/forecast/108a24c94c0f1a800ae311dc19332a45/${lat},${lng}`;
    return axios.get(weatherUrl);
}).then((response) => {
    console.log(`Current temp ${response.data.currently.temperature} but feels like ${response.data.currqently.apparentTemperature}`);
}).catch((e) => {
    if( e.code === 'ENOTFOUND') {
        console.log('Unable to conenct to API servers');
    }else{
        console.log(e);
    }
});
