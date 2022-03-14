function pad_left(str, chr, width)
{
	str = `${str}`;
	while (str.length < width) str = chr + str;
	return str;
}

function get_short_month_name(month)
{
	switch (month)
	{
		case 0: return "Jan";
		case 1: return "Feb";
		case 2: return "Mar";
		case 3: return "Apr";
		case 4: return "May";
		case 5: return "Jun";
		case 6: return "Jul";
		case 7: return "Aug";
		case 8: return "Sep";
		case 9: return "Oct";
		case 10: return "Nov";
		case 11: return "Dec";
		default: return "Err";
	}
}

function get_long_month_name(month)
{
	switch (month)
	{
		case 0: return "January";
		case 1: return "February";
		case 2: return "March";
		case 3: return "April";
		case 4: return "May";
		case 5: return "June";
		case 6: return "July";
		case 7: return "August";
		case 8: return "September";
		case 9: return "October";
		case 10: return "November";
		case 11: return "December";
		default: return "Err";
	}
}

function format_date(timestamp, python_date_format)
{
	let date = new Date(timestamp);

	return python_date_format
		.replace("%a", "Err")
		.replace("%A", "Err")
		.replace("%w", "Err")
		.replace("%d", pad_left(date.getUTCDate(), "0", 2))
		.replace("%b", get_short_month_name(date.getUTCMonth()))
		.replace("%B", get_long_month_name(date.getUTCMonth()))
		.replace("%m", pad_left(date.getUTCMonth() + 1, "0", 2))
		.replace("%y", pad_left(date.getUTCFullYear() % 100, "0", 2))
		.replace("%Y", pad_left(date.getUTCFullYear(), "0", 4))
		.replace("%H", pad_left(date.getUTCHours(), "0", 2))
		.replace("%I", pad_left(((date.getUTCHours() % 12) === 0) ? 12 : (date.getUTCHours() % 12), "0", 2))
		.replace("%p", date.getUTCHours() >= 12 ? "PM" : "AM")
		.replace("%M", pad_left(date.getUTCMinutes(), "0", 2))
		.replace("%S", pad_left(date.getUTCSeconds(), "0", 2))
		.replace("%f", 0)
		.replace("%z", "+0000")
		.replace("%Z", "UTC")
		.replace("%j", "Err")
		.replace("%U", "Err")
		.replace("%W", "Err")
		.replace("%c", date.toLocaleString())
		.replace("%x", date.toLocaleDateString())
		.replace("%X", date.toLocaleTimeString())
		.replace("%%", "%");
}