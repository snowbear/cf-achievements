need_submissions = true;

function _distinct(list) {
	var counter = { };
	
	_.each(list, function(item) { counter[item] = true; });
	
	return Object.keys(counter);
}

function achievement_calculator(callback) {
	var filtered_submissions = _.filter(submissions, function (s) { return s.verdict == submission_verdict.ok &&
																		   s.author.participantType === participant_type.contestant &&
																		   s.programmingLanguage != "Mysterious Language"; });
	var grouped_submissions = _.groupBy(filtered_submissions, get_main_handle);
	
	for (var user in grouped_submissions) {
		var languages = _distinct(_.map(grouped_submissions[user], function (s) { return s.programmingLanguage; }));
		var language_groups = _.map(languages, get_language_group);
		var different_languages = _.size(_distinct(language_groups));
		
		if (different_languages > 1) {
			var languages_string = join_with_commas_and_and(languages);
			add_achievement(user, "the usage of " + languages_string + " to solve problems in " + contest_tag(contestId), different_languages - 1);
		}
	}
	callback();
}