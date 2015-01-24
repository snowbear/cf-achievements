need_standings = true;
need_submissions = true;

var group_required_for_achievement = {
	100: language_group.C,
	101: language_group.Cpp,
	102: language_group.CSharp,
	103: language_group.D,
	104: language_group.Go,
	105: language_group.Haskell,
	106: language_group.Java,
	107: language_group.Ocaml,
	109: language_group.Pascal,
	110: language_group.Perl,
	111: language_group.PHP,
	112: language_group.Python,
	113: language_group.Ruby,
	114: language_group.Scala,
	115: language_group.JavaScript,
};

function achievement_calculator(callback) {
	var required_group = group_required_for_achievement[achievementId];
	if(is_undefined(required_group)) throw "Group is undefined for achievement_id: " + achievementId;

	var matching_submissions =
					_.filter(submissions, function (s) { return s.author.participantType == participant_type.contestant &&
																s.verdict == submission_verdict.ok &&
																get_language_group(s.programmingLanguage) === required_group; });
	
	var grouped_by_users = _.groupBy(matching_submissions, get_main_handle);

	$.each(grouped_by_users, function (key, val) { 
		var lvl = _.size(_.groupBy(val, function (s) { return s.problem.index; }));
		add_achievement(key, undefined, lvl);
	});
	
	callback();
}