console.log('Hello world')

// alert('Yoo, IT')
// Amount input 
let amount1 = document.querySelector('#amount1');
let amount2 = document.querySelector('#amount2');
let amount3 = document.querySelector('#amount3');
let amount4 = document.querySelector('#amount4');
let amount5 = document.querySelector('#amount5');




// Total Amount 
let total = document.querySelector('#total');


// Line 1
let qty1 = document.querySelector('#qty1');
let rate1 = document.querySelector('#rate1');
rate1.addEventListener('keyup',multiply1,false);

function multiply1(e) {
    e.preventDefault();
    let multiplier = qty1.value * rate1.value;  
    
    amount1.value= multiplier;
    total.value = multiplier;
    console.log(total.value.toLocaleString());
    
}

qty1.addEventListener('keyup',multiply1inverse,false);

function multiply1inverse(e){
    e.preventDefault();

    let multiplierInverse =  rate1.value * qty1.value ;  
    
    amount1.value= multiplierInverse;
    total.value = multiplierInverse;

}


// Line 2
let qty2 = document.querySelector('#qty2');
let rate2 = document.querySelector('#rate2');
rate2.addEventListener('keyup',multiply2,false);

function multiply2(e) {
    e.preventDefault();
    let multiplier2 = qty2.value * rate2.value;    
    amount2.value = multiplier2;
    total.value = parseInt(amount1.value) + parseInt(amount2.value)   
    
}

qty2.addEventListener('keyup',multiply1inverse2,false);
function multiply1inverse2(e){
    e.preventDefault();
    let multiplierInverse2 =  rate2.value * qty2.value ;      
    amount2.value= multiplierInverse2;
    total.value = parseInt(amount2.value) + parseInt(amount1.value)
   
    
}


// Line 3
let qty3 = document.querySelector('#qty3');
let rate3 = document.querySelector('#rate3');
rate3.addEventListener('keyup',multiply3,false);

function multiply3(e) {
    e.preventDefault();
    let multiplier3 = qty3.value * rate3.value;    
    amount3.value = multiplier3;
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value);
    
}

qty3.addEventListener('keyup',multiply3,false);

function multiply3(e) {
    e.preventDefault();
    let multiplier3 = qty3.value * rate3.value;
    
    amount3.value = multiplier3;
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value);
    
}

// Line 4
let qty4 = document.querySelector('#qty4');
let rate4 = document.querySelector('#rate4');
rate4.addEventListener('keyup',multiply4,false);

function multiply4(e) {
    e.preventDefault();
    let multiplier4 = qty4.value * rate4.value;
    
    amount4.value = multiplier4;
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value) + parseInt(amount4.value);
    
}

qty4.addEventListener('keyup',multiply1inverse4,false);
function multiply1inverse4(e){
    e.preventDefault();
    let multiplierInverse4 =   qty4.value * rate4.value  ;      
    amount4.value= multiplierInverse4;
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value) + parseInt(amount4.value);
    
}

// Line 5 
let qty5 = document.querySelector('#qty5');
let rate5 = document.querySelector('#rate5');
rate5.addEventListener('keyup',multiply5,false);

function multiply5(e) {
    e.preventDefault();
    let multiplier5 = qty5.value * rate5.value;
    
    amount5.value = multiplier5;  
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value) + parseInt(amount4.value) + parseInt(amount5.value); 
    
}

qty5.addEventListener('keyup',multiply1inverse5,false);
function multiply1inverse5(e){
    e.preventDefault();
    let multiplierInverse5 = qty5.value * rate5.value;      
    amount5.value= multiplierInverse5;
    total.value = parseInt(amount1.value) + parseInt(amount2.value) + parseInt(amount3.value) + parseInt(amount4.value) + parseInt(amount5.value); 
    // total.value = total.toLocaleString('en-US')   
   
}



// NUMBER TO WORDS 
let amountInwords = document.querySelector('#amount_in_words');
let numInput = document.querySelector('#total')

numInput.addEventListener('keyup',inWords,false)


var a = ['','one ','two ','three ','four ', 'five ','six ','seven ','eight ','nine ','ten ','eleven ','twelve ','thirteen ','fourteen ','fifteen ','sixteen ','seventeen ','eighteen ','nineteen '];
var b = ['', '', 'twenty','thirty','forty','fifty', 'sixty','seventy','eighty','ninety'];

function inWords (num) {
    // e.preventDefault();
    if ((num = num.toString()).length > 9) return 'overflow';
    n = ('000000000' + num).substr(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
    if (!n) return; var str = '';
    str += (n[1] != 0) ? (a[Number(n[1])] || b[n[1][0]] + ' ' + a[n[1][1]]) + '' : '';
    str += (n[2] != 0) ? (a[Number(n[2])] || b[n[2][0]] + ' ' + a[n[2][1]]) + 'hundred ' : '';
    str += (n[3] != 0) ? (a[Number(n[3])] || b[n[3][0]] + ' ' + a[n[3][1]]) + 'thousand ' : '';
    str += (n[4] != 0) ? (a[Number(n[4])] || b[n[4][0]] + ' ' + a[n[4][1]]) + 'hundred ' : '';
    str += (n[5] != 0) ? ((str != '') ? 'and ' : '') + (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) + 'only ' : '';

    
    console.log(num)
    return str;
}

document.getElementById('amount_in_words').onmouseenter = function () {
    document.getElementById('amount_in_words').value = inWords(document.getElementById('total').value);
    
    
};


