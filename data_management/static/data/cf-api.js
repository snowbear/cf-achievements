var cfapi_callbacks = {
};

var contest_phase = {
	before: 'BEFORE',
	coding: 'CODING',
	pending_system_test: 'PENDING_SYSTEM_TEST', 
	system_test: 'SYSTEM_TEST',
	finished: 'FINISHED',
};

function getContests(callback, include_gym_contests) {
	include_gym_contests = defaultFor(include_gym_contests, false);
	$.getScript("http://codeforces.com/api/contest.list?gym=" + include_gym_contests + "&jsonp=cfapi_getContestsCallback&lang=en");
	cfapi_callbacks.getContests = callback;
}

function cfapi_getContestsCallback(res) {
	var callback = cfapi_callbacks.getContests;
	delete cfapi_callbacks.getContests;
	if (res.status == "OK") {
		callback(res.result);
	} else alert('Error occured while loading Contests');
}