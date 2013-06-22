
function exportLink(){
	$('#export_dialog').dialog('open');
	return false;
}

function exportButton(){
	$('#export_form').submit();
	return false;
}

$(
	function () {
		$('.header .radioset #table').click();
		$('#export_dialog').dialog({ 
			autoOpen: false,
			modal: true,
			buttons: {
				"OK": function() {
					exportButton();
					$(this).dialog('close');
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});
	}
);
