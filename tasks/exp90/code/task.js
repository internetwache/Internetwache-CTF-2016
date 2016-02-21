var readline = require('readline');
var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});
console.log('Welcome and have fun!');
process.stdout.write('$');

function reverse(s){
    return s.split("").reverse().join("");
}

rl.on('line', function(line){
    var blacklist = /(eval|require|flag)/
    line = reverse(line);
    if(line.match(blacklist)) {
        console.log('Blacklisted commands');
        process.stdout.write('$');
        return;
    }

    if(line.length <= 10) {
        line = line.replace(/.(.)?/g, '$1');
    } else if(line.length <= 20) {
        line = line.replace(/..(.)?/g, '$1');
    } else if(line.length <= 30) {
        line = line.replace(/...(.)?/g, '$1');
    } else if(line.length <= 40) {
        line = line.replace(/....(.)?/g, '$1');
    } else {
        line = line.replace(/.....(.)?/g, '$1');
    }

    
    try {
    	console.log(eval(line));
	}catch(e) {
		console.log(e);
	}

    process.stdout.write('$');
})