const yargs = require('yargs');
const geocode = require('./geocode/geocode.js');
const forecastAPI = require('./forcastApi/forecastAPI.js');

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

geocode.gecodeAddress(argv.a, (errorMessage, results) => {
    if(errorMessage){
        console.log(errorMessage);
    } else{
        console.log(results.address);
        forecastAPI.forecast(results.lat, results.lng, (errorMessage, weatherResults) => {
            if(errorMessage){
                console.log(errorMessage);
            } else{
                console.log(`It's currently ${weatherResults.temperature} but feels like ${weatherResults.apparentTemperature}`);
            }
        });
    }
});
