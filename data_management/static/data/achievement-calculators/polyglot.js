need_submissions = true;

var language_groups = [
	['GNU C++', 'GNU C++0x', 'MS C++'],
	['Python 2', 'Python 3'],
	['Java 6', 'Java 7', 'Java 8'],
	['Mono C#', 'MS C#'],
];

var language_to_group_mapping = { };

function init_languages_map() {
	$.each(language_groups, function(gi, group) {
		_.each(group, function(language) { language_to_group_mapping[language] = gi; });
	});
}

function get_language_group_index(language) {
	if (is_undefined(language_to_group_mapping[language])) {
		language_to_group_mapping[language] = _.max(language_to_group_mapping) + 1;
	}
	
	return language_to_group_mapping[language];
}

function _distinct(list) {
	var counter = { };
	
	_.each(list, function(item) { counter[item] = true; });
	
	return Object.keys(counter);
}

function join_with_commas_and_and(list) {
	var result = "";
	var last_index = _.size(list) - 1;
	$.each(list, function (i, item) {
		if (i == last_index) result += " and ";
		else if (i > 0) result += ", ";
		result += item;
	});
	return result;
}

function achievement_calculator(callback) {
	init_languages_map();

	var filtered_submissions = _.filter(submissions, function (s) { return s.verdict == submission_verdict.ok &&
																		   s.author.participantType === participant_type.contestant &&
																		   s.programmingLanguage != "Mysterious Language"; });
	var grouped_submissions = _.groupBy(filtered_submissions, function (s) { return s.author.members[0].handle; });
	
	for (var user in grouped_submissions) {
		var languages = _distinct(_.map(grouped_submissions[user], function (s) { return s.programmingLanguage; }));
		var language_groups = _.map(languages, get_language_group_index);
		var different_languages = _.size(_distinct(language_groups));
		
		if (different_languages > 1) {
			var languages_string = join_with_commas_and_and(languages);
			add_achievement(user, "the usage of " + languages_string + " to solve problems in " + contest_tag(contestId), different_languages - 1);
		}
	}
	callback();
}