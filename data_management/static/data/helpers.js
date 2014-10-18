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

function is_online_participant(party) {
	return party.participantType === participant_type.contestant ||
		   party.participantType === participant_type.out_of_competition;
}
