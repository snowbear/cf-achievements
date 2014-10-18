function groupBy(array, groupingFields) {
	var result = { };
	
	$.each(array, function (_, item) {
		var ptr = result;
		$.each(groupingFields, function (_, field) {
			var value = item[field];
			if (is_undefined(ptr[value]))
				ptr[value] = { };
			ptr = ptr[value];
		});
		if (is_undefined(ptr.items)) ptr.items = [];
		ptr.items.push(item);
	});
	
	return result;
}

function contest_tag(contestId) {
	return "[contest:" + contestId + "]";
}

function user_tag(handle) {
	return "[user:" + handle + "]";
}

function get_main_handle(party) {
	console.assert(party.members.length == 1);
	return party.members[0].handle;
}

function is_online_participant(party) {
	return party.participantType === participant_type.contestant ||
		   party.participantType === participant_type.out_of_competition;
}

function is_accepted(problem_result) {
	return !is_undefined(problem_result.bestSubmissionTimeSeconds);
}

function join_with_commas_and_and(list) {
	var result = "";
	var last_index = _.size(list) - 1;
	$.each(list, function (i, item) {
		if (i != 0 && i == last_index) result += " and ";
		else if (i > 0) result += ", ";
		result += item;
	});
	return result;
}
