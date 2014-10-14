Date.prototype.timeNow = function () {
	return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}

function is_undefined(val) {
	return typeof val === 'undefined';
}

function has_parameter(field) {
	var url = window.location.href;
	if(url.indexOf('?' + field + '=') != -1)
		return true;
	else if(url.indexOf('&' + field + '=') != -1)
		return true;
	return false;
}

var is_debug_cache = has_parameter("debug");

function is_debug() {
	return is_debug_cache;
}	

function log(obj) {
	if (typeof(obj) === 'object') {
		console.log((new Date().timeNow()) + ":");
		console.log(obj);
	} else {
		str = (new Date().timeNow()) + " - " + obj;
		console.log(str);
	}
}

function defaultFor(arg, val) { return typeof arg !== 'undefined' ? arg : val; }