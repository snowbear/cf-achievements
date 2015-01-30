var need_hacks = true;

function achievement_calculator(callback) {
	var results = [];
	$.each(hacks, function (i, hack) {
		if (hack.hacker.members[0].handle == "tourist")
			if (hack.verdict === hack_verdict.unsuccessful || hack.verdict === hack_verdict.successful) {
				results.push( { defender: hack.defender.members[0].handle, 
								problem: hack.problem.index, 
								wasHacked: hack.verdict === hack_verdict.successful } );
			}
	});
	
	log(results);
	
	var groups = groupBy(results, ['defender', 'problem']);
	
	log(groups);
		
	for (var defender in groups) {
		for (var problem in groups[defender]) {
			var defended = false;
			$.each(groups[defender][problem].items, function (_, item) {
				if (item.wasHacked) {
					defended = false;
					return false;
				} else {
					defended = true;
				}
			});
			if (defended) {
				log(defender + " - " + problem);
				add_achievement(defender, "the successful defence of his problem " + problem + " from " + user_tag('tourist') +" during " + contest_tag(contestId));
			}
		}
	}
	callback();
}