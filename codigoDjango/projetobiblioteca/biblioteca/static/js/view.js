
function accordion_change(pos){
	var h = parseInt($('.main_content .accordion h3').height());
	h = h + parseInt($('.main_content .accordion h3').css('margin-top').replace('px', ''));
	h = h + parseInt($('.main_content .accordion h3').css('margin-bottom').replace('px', ''));
	h = h + parseInt($('.main_content .accordion h3').css('padding-bottom').replace('px', ''));
	h = h + parseInt($('.main_content .accordion h3').css('padding-top').replace('px', ''));
	h = h + parseInt($('.main_content .accordion h3').css('border-top-width').replace('px', ''));
	h = h + parseInt($('.main_content .accordion h3').css('border-bottom-width').replace('px', ''));
	
	var margin = pos * h;
	$('.side_menu').css('margin-top', margin+'px');
}

$(
	function () {
		$('.header .radioset #books').click();
		
		$('.accordion h3').click(function (e) {
			accordion_change(parseInt(this.id.substring('ui-accordion-1-header-'.length)));
		});
	}
);