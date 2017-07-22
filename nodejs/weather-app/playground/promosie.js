var asyncAdd = (a, b) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if(typeof a === 'number' && typeof b === 'number' ){
                resolve(a+b);
            } else {
                reject('Arguments must be number');
            }
        }, 1500);
    });
};

asyncAdd(5, '7').then((res) => {
    console.log('Result: ', res);
    return asyncAdd(res, 33);
}).then((res) => {
    console.log('Result 45: ', res);
}).catch((errorMessage) => {
    console.log(errorMessage);
});

// var somePrommise = new Promise((resolve, reject) => {
//     setTimeout(() => {
//         reject('BYE BYE!!')
//         resolve('Hey. It worked');
//     }, 2500);
//
//
// });
//
// somePrommise.then( (message) => {
//     console.log('Success: ', message);
// }, (errorMessage) => {
//     console.log("Error: ", errorMessage);
// });
