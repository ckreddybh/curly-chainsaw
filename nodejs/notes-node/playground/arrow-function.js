var square = x => x*x;
console.log(square(9));


var user ={
    name: 'CK',
    sayHi: () => {
        console.log(arguments);
        console.log(`Hi. I'm ${this.name}`);
    },
    sayHIAlt () {
        console.log(arguments);
        console.log(`Hi. I'm ${this.name}`);
    }
};

user.sayHi(1,2,3);
user.sayHIAlt(1,2,3);
