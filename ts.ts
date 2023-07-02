const array = [8, 2, 1, 3, 4, 0, 7, 9, 10, 5, 6].sort((a, b) => a - b);
console.log(array);
array.forEach((item) => console.log(item));
array.map((a) => console.log(`<li>${a}</li>`));
let greater_1 = array.filter((a) => a >= 5);
let out: number = array.reduce((total, value) => total + value, 0);
console.log(
  out,
  greater_1,
  Math.PI,
  Math.LN10,
  Math.LN2,
  Math.floor(Math.random() * 10)
);
