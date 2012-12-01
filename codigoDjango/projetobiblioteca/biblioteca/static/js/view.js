
function accordion_change(pos){
	var margin = pos * 40;
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