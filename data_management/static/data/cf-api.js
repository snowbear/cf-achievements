var cfapi_callbacks = {};

var submission_verdict = {
	ok: 'OK',
};

var participant_type = {
	 contestant: 'CONTESTANT', 
	 practice: 'PRACTICE', 
	 virtual: 'VIRTUAL',
	 manager: 'MANAGER',
	 out_of_competition: 'OUT_OF_COMPETITION',
};

var contest_phase = {
	before: 'BEFORE',
	coding: 'CODING',
	pending_system_test: 'PENDING_SYSTEM_TEST', 
	system_test: 'SYSTEM_TEST',
	finished: 'FINISHED',
};

var hack_verdict = {
	successful: 'HACK_SUCCESSFUL', 
	unsuccessful: 'HACK_UNSUCCESSFUL',
};

function make_api_call(method, parameters, callback) {
	var callerName = arguments.callee.caller.name;

	if (!is_undefined(callback)) cfapi_callbacks[callerName] = callback;
	callbackMethod = "cfapi_" + callerName + "Callback";
	url = "http://codeforces.com/api/" + method + "?jsonp=" + callbackMethod + "&lang=en&" + parameters;
	$.getScript(url);
}

function return_to_callback(res) {
	var callerName = arguments.callee.caller.name;
	callerName = callerName.substr('cfapi_'.length);
	callerName = callerName.substr(0, callerName.length - 'Callback'.length);
	
	var callback = cfapi_callbacks[callerName];
	
	delete cfapi_callbacks[callerName];
	callback(res);
}

function getContests(callback, include_gym_contests) {
	include_gym_contests = defaultFor(include_gym_contests, false);
	$.getScript("http://codeforces.com/api/contest.list?gym=" + include_gym_contests + "&jsonp=" + cfapi_getContestsCallback.name + "&lang=en");
	cfapi_callbacks.getContests = callback;
}

function cfapi_getContestsCallback(res) {
	var callback = cfapi_callbacks.getContests;
	delete cfapi_callbacks.getContests;
	if (res.status == "OK") {
		callback(res.result);
	} else alert('Error occured while loading Contests');
}

var submissions_progress;

function getSubmissions(callback, contestId) {
	submissions_progress = {
		result: [],
		callback: callback,
		contestId: contestId,
	}
	getSubmissionsInternal();
}

function getSubmissionsInternal() {
	var parameters = "contestId=" + submissions_progress.contestId +
					"&from=" + (submissions_progress.result.length + 1) +
					"&count=30000";
	make_api_call("contest.status", parameters);
}

function cfapi_getSubmissionsInternalCallback(res) {
	res = res.result;
	if (res.length === 0) {
		submissions_progress.callback(submissions_progress.result);
	} else {
		submissions_progress.result = 
				submissions_progress.result.concat(res);
		getSubmissionsInternal();
	}
}

var full_standings_loading_progress;

function getFullStandings(callback, contestId) {
	full_standings_loading_progress = {
		result: { standings: [] },
		callback: callback,
		contestId: contestId,
	};
	getFullStandingsInternal();
}

function getFullStandingsInternal() {
	var parameters = "contestId=" + full_standings_loading_progress.contestId +
					"&from=" + (full_standings_loading_progress.result.standings.length + 1) +
					"&count=10000" + 
					"&showUnofficial=true";
	make_api_call("contest.standings", parameters);
}

function cfapi_getFullStandingsInternalCallback(res) {
	res = res.result;
	full_standings_loading_progress.result.problems = res.problems;
	if (res.rows.length === 0) {
		full_standings_loading_progress.callback(full_standings_loading_progress.result);
	} else {
		full_standings_loading_progress.result.standings = 
				full_standings_loading_progress.result.standings.concat(res.rows);
		getFullStandingsInternal();
	}
}

function getHacks(callback, contestId) {
	make_api_call("contest.hacks", "contestId=" + contestId, callback);
}

function cfapi_getHacksCallback(res) {
	$.each(res.result, function (i, hack) {
		var tmp = hack.hacker;
		hack.hacker = hack.defender;
		hack.defender = tmp;
	});
	return_to_callback(res.result);
}

function getRatedUsers(callback, activeOnly) {
	activeOnly = defaultFor(activeOnly, false);
	make_api_call("user.ratedList", "activeOnly="+activeOnly, callback);
}

function cfapi_getRatedUsersCallback(res) {
	return_to_callback(res.result);
}