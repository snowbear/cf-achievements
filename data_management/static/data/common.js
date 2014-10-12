Date.prototype.timeNow = function () {
	return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}

function is_undefined(val) {
	return typeof val === 'undefined';
}

function log(obj) {
	if (typeof(obj) === 'object') {
		console.log((new Date().timeNow()) + ":");
		console.log(obj);
	} else {
		str = (new Date().timeNow()) + " - " + str;
		console.log(str);
	}
}

function defaultFor(arg, val) { return typeof arg !== 'undefined' ? arg : val; }