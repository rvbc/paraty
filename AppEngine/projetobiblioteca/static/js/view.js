
function exportButton(){
	$('#export_form').submit();
	return false;
}

function toggleSuggestions(){
	var id = $(this).attr('alt');
	var s = $('.ui-icon.'+id);
	
	if(s.hasClass('ui-icon-triangle-1-e')){
		s.removeClass('ui-icon-triangle-1-e');
		s.addClass('ui-icon-triangle-1-s');
		$('#'+id).slideDown();
	} else {
		s.removeClass('ui-icon-triangle-1-s');
		s.addClass('ui-icon-triangle-1-e');
		$('#'+id).slideUp();
	}
}

$(
	function () {
		$('.header .radioset #books').click();
		$('.suggestions .head').click(toggleSuggestions);
		$('.ui-accordion-content').css('height', 'auto');
	}
);
