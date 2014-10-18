need_hacks = true;
need_standings = true;
need_submissions = true;

function achievement_calculator(callback) {
	var hacks_filtered = [];
	$.each(hacks, function (i, hack) {
		if (hack.verdict === hack_verdict.successful) {
			var item = {	handle1: hack.hacker.members[0].handle,
							handle2: hack.defender.members[0].handle,
							problem: hack.problem.index,
							swapped: false,
							time: hack.creationTimeSeconds };
			
			if (item.handle1 > item.handle2) { var tmp = item.handle1; item.handle1 = item.handle2; item.handle2 = tmp; item.swapped = true; }
			hacks_filtered.push(item);
		}
	});
	
	log(hacks_filtered);
	
	var hacks_grouped = groupBy(hacks_filtered, ['handle1', 'handle2', 'problem']);
	var peresvet_final_results = [];
	
	var add_ach_helper = function(handle1, handle2, problem, contestId) {
		add_achievement(handle1, "the successful mutual hack with " + user_tag(handle2) + " on problem " + problem + " in " + contest_tag(contestId));
	};
	
	for (var handle1 in hacks_grouped)
		for (var handle2 in hacks_grouped[handle1])
			for (var problem in hacks_grouped[handle1][handle2]) {
				var t = hacks_grouped[handle1][handle2][problem].items[0].time;
				var hackedForward = false;
				var hackedBack = false;
				$.each(hacks_grouped[handle1][handle2][problem].items, function (_, item) {
					if (item.swapped) hackedBack = true;
					else hackedForward = true;
					t = Math.min(t, item.time);
				});
				
				if (!hackedBack || !hackedForward) continue;
				
				if (has_submissions_after(handle1, problem, t) ||
					has_submissions_after(handle2, problem, t)) continue;
				
				log(handle1 + " " + handle2 + " " + t);
				
				add_ach_helper(handle1, handle2, problem, contestId);
				add_ach_helper(handle2, handle1, problem, contestId);
			}
	callback();
}