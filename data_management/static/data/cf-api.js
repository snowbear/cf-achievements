var cfapi_callbacks = {};
var cfapi_data = {};

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

var languages = {
	GnuC: "GNU C",
	GnuCpp: "GNU C++",
	GnuCpp0x: "GNU C++0x",
	GnuCpp11: "GNU C++11",
	MsCpp: "MS C++",
	CSharpMs: "MS C#",
	CSharpMono: "Mono C#",
	D: "D",
	Go: "Go",
	Haskell: "Haskell",
	Java6: "Java 6",
	Java7: "Java 7",
	Java8: "Java 8",
	Ocaml: "Ocaml",
	Delphi: "Delphi",
	FreePascal: "FPC",
	Perl: "Perl",
	PHP: "PHP",
	Python2: "Python 2",
	Python3: "Python 3",
	Ruby: "Ruby",
	Scala: "Scala",
	JavaScript: "JavaScript",
	FSharp: "F#",
	
	Tcl: "Tcl",
	Io: "Io",
	Pike: "Pike",
	Befunge: "Befunge",
	Cobol: "Cobol",
	Ada: "Ada",
	Factor: "Factor",
	Roco: "Roco",
	FALSE: "FALSE",
	MysteriousLanguage: "Mysterious Language",
};

var language_group = {
	C: 'C',
	Cpp: 'C++',
	CSharp: 'C#',
	D: 'D',
	Go: 'Go',
	Haskell: 'Haskell',
	Java: 'Java',
	Ocaml: 'Ocaml',
	Delphi: 'Delphi',
	Pascal: 'Pascal',
	Perl: 'Perl',
	PHP: 'PHP',
	Python: 'Python',
	Ruby: 'Ruby',
	Scala: 'Scala',
	JavaScript: 'JavaScript',
	FSharp: 'F#',
	Esoteric: 'Esoteric',
};

var language_to_group_mapping;

function get_language_group(language) {
	if (is_undefined(language_to_group_mapping)) {
		language_to_group_mapping = { };
		language_to_group_mapping[languages.GnuC] = language_group.C;
		language_to_group_mapping[languages.GnuCpp] = language_group.Cpp;
		language_to_group_mapping[languages.GnuCpp0x] = language_group.Cpp;
		language_to_group_mapping[languages.GnuCpp11] = language_group.Cpp;
		language_to_group_mapping[languages.MsCpp] = language_group.Cpp;
		language_to_group_mapping[languages.CSharpMs] = language_group.CSharp;
		language_to_group_mapping[languages.CSharpMono] = language_group.CSharp;
		language_to_group_mapping[languages.D] = language_group.D;
		language_to_group_mapping[languages.Go] = language_group.Go;
		language_to_group_mapping[languages.Haskell] = language_group.Haskell;
		language_to_group_mapping[languages.Java6] = language_group.Java;
		language_to_group_mapping[languages.Java7] = language_group.Java;
		language_to_group_mapping[languages.Java8] = language_group.Java;
		language_to_group_mapping[languages.Ocaml] = language_group.Ocaml;
		language_to_group_mapping[languages.Delphi] = language_group.Pascal;
		language_to_group_mapping[languages.FreePascal] = language_group.Pascal;
		language_to_group_mapping[languages.Perl] = language_group.Perl;
		language_to_group_mapping[languages.PHP] = language_group.PHP;
		language_to_group_mapping[languages.Python2] = language_group.Python;
		language_to_group_mapping[languages.Python3] = language_group.Python;
		language_to_group_mapping[languages.Ruby] = language_group.Ruby;
		language_to_group_mapping[languages.Scala] = language_group.Scala;
		language_to_group_mapping[languages.JavaScript] = language_group.JavaScript;
		language_to_group_mapping[languages.FSharp] = language_group.FSharp;
		
		language_to_group_mapping[languages.Tcl] = language_group.Esoteric;
		language_to_group_mapping[languages.Io] = language_group.Esoteric;
		language_to_group_mapping[languages.Pike] = language_group.Esoteric;
		language_to_group_mapping[languages.Befunge] = language_group.Esoteric;
		language_to_group_mapping[languages.Cobol] = language_group.Esoteric;
		language_to_group_mapping[languages.Ada] = language_group.Esoteric;
		language_to_group_mapping[languages.Factor] = language_group.Esoteric;
		language_to_group_mapping[languages.Roco] = language_group.Esoteric;
		language_to_group_mapping[languages.FALSE] = language_group.Esoteric;
		language_to_group_mapping[languages.MysteriousLanguage] = language_group.Esoteric;
	}
	
	if (language.startsWith("Secret_")) return language_group.Esoteric;
	
	if (is_undefined(language_to_group_mapping[language])) {
		throw 'There is no group for language: ' + language;
	}

	return language_to_group_mapping[language];
}

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

function getContestInfo(callback, contestId) {
	cfapi_data.getContestInfo_contestId = contestId;
	cfapi_data.getContestInfo_callback = callback;
	getContests(cfapi_getContestInfoCallback, false);
}

function cfapi_getContestInfoCallback(contests) {
	var contestId = cfapi_data.getContestInfo_contestId;
	var callback = cfapi_data.getContestInfo_callback;
	var contest = _.find(contests, function (c) { return c.id == contestId; } );
	callback(contest);
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