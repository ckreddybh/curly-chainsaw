const utils = require('./utils.js');
const expect = require('expect');

it('Should add two numbers', () => {
    var res = utils.add(33, 11);
    expect(res).toBe(44).toBeA('number');
});

it('Should square the number', () => {
    var res = utils.square(10);

    expect(res).toBe(100).toBeA('number');
});


it('Should async add two numbers', (done) => {
    utils.asyncAdd(33, 11, (sum) => {
        expect(sum).toBe(44).toBeA('number');
        done();
    });

});


it('Should async sqrt', (done) => {
    utils.asyncSqrt(10, (sqrt) => {
        expect(sqrt).toBe(100).toBeA('number');
        done();
    });
});
