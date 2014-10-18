need_standings = true;

var unknown_language_round_ids = [64, 72, 100, 130, 153, 162, 188, 345, 470];

function contest_predicate() {
	return _.contains(unknown_language_round_ids, contestId);
}

function achievement_calculator(callback) {
	var filtered_standings = _.filter(standings.standings, function(s) { return is_online_participant(s.party); });
	var problems = standings.problems;
	log(filtered_standings);
	_.each(filtered_standings, function (standing) {
		var solved_problems = [];
		$.each(standing.problemResults, function(i, result) {
			if (is_accepted(result)) solved_problems.push(problems[i].index);
		});
		
		if (_.size(solved_problems) < 2) return true;
		var problems_string = join_with_commas_and_and(solved_problems);
		add_achievement(get_main_handle(standing.party), "the problems " + problems_string + " solved during " + contest_tag(contestId));
	});

	callback();
}