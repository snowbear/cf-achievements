var need_hacks = true;
var need_submissions = true;

function achievement_calculator(callback) {
	if (hacks.length == 0) {
		callback();
		return;
	}
	
	var matching_submissions = submissions;
	matching_submissions = _.filter(matching_submissions, function (s) { return s.verdict !== submission_verdict.ok && s.verdict !== submission_verdict.challenged; });
	matching_submissions = _.filter(matching_submissions, function (s) { return is_online_participant(s.author); });
	matching_submissions = _.filter(matching_submissions, function (s) { return s.testset === submission_testset.tests; });
	
	var results = { };
	
	_.each(matching_submissions, function (s) {
		var h = get_main_handle(s);
		if (is_undefined(results[h])) results[h] = { };
		results[h][s.problem.index] = 1;
	});
	
	var matching_hacks = hacks;
	matching_hacks = _.filter(matching_hacks, function (h) { return h.verdict == hack_verdict.successful; });
	matching_hacks = _.filter(matching_hacks, function (h) { return !is_undefined(results[get_main_handle(h.hacker)]) &&
																	!is_undefined(results[get_main_handle(h.hacker)][h.problem.index]); });
	
	_.each(matching_hacks, function (h) { results[get_main_handle(h.hacker)][h.problem.index] |= 2; });
	
	$.each(results, function (handle, problems) {
		$.each(problems, function (problem, result) {
			if (result == 3) {
				add_achievement(handle, "successful challenge on problem " + problem + " during " + contest_tag(contestId) + " while his/her own code was not perfect either");
				log(handle + " - " + problem);
			}
		});
	});

	callback();
}