const array = [8, 2, 1, 3, 4, 0, 7, 9, 10, 5, 6].sort((a, b) => a - b);
console.log(array);
array.forEach((item) => console.log(item));
array.map((a) => console.log(`<li>${a}</li>`));
let greater_1 = array.filter((a) => a >= 5);
let out = array.reduce((total, value) => total + value, 0);
console.log(
  out,
  greater_1,
  Math.PI,
  Math.LN10,
  Math.LN2,
  Math.floor(Math.random() * 10)
);

const regx = /[0-9]/.test("0039dggs");
const date_format = /(\d\d-\d\d-\d\d\d\d) (\d\d:\d\d)/; // 01-30-2003 15:20
console.log(regx, date_format.test("01-30-2003 15:20"));
const email_regx = /^(\d\w\.){2,30}@(\w\.){2,7}(\w){2,4}/;
console.log(email_regx.test("daudnamayala@udom.ac.tz"));
