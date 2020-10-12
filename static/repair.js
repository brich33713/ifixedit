$('#query').on('click', async function(e) {
	e.preventDefault();
	issues = await axios.get('/api/issues');

	if (issues.data.issues.includes($('#search').val())) {
		issue = $('#search').val();
		issue = issue.replaceAll(' ', '-');
		$('form').attr('action', `/fix/${issue}`);
		$('#go').trigger('click');
		console.log('test');
	}
});

$('#go').on('click');
