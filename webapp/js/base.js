
function login(){
	$('.login').slideToggle();
	return false;
}

$(function() {
	
	$('.login').hide();
	$('input[placeholder], textarea[placeholder]').placeholder();
	
	$( ".accordion" ).accordion();
	
	var availableTags = [
		"ActionScript",
		"AppleScript",
		"Asp",
		"BASIC",
		"C",
		"C++",
		"Clojure",
		"COBOL",
		"ColdFusion",
		"Erlang",
		"Fortran",
		"Groovy",
		"Haskell",
		"Java",
		"JavaScript",
		"Lisp",
		"Perl",
		"PHP",
		"Python",
		"Ruby",
		"Scala",
		"Scheme"
	];
	$( ".autocomplete" ).autocomplete({
		source: availableTags
	});
	

	
	$( ".button" ).button();
	$( ".radioset" ).buttonset();
	
	$( ".spinner" ).spinner({ min: 1 });
	$( ".item_menu" ).menu();
	
	$( ".tabs" ).tabs();
	

	
	$( ".dialog" ).dialog({
		autoOpen: false,
		width: 400,
		buttons: [
			{
				text: "Ok",
				click: function() {
					$( this ).dialog( "close" );
				}
			},
			{
				text: "Cancel",
				click: function() {
					$( this ).dialog( "close" );
				}
			}
		]
	});

	// Link to open the dialog
	$( ".dialog-link" ).click(function( event ) {
		$( ".dialog" ).dialog( "open" );
		event.preventDefault();
	});
	

	
	$( ".datepicker" ).datepicker({
		inline: true
	});
	

	
	$( ".slider" ).slider({
		range: true,
		values: [ 17, 67 ]
	});
	

	
	$( ".progressbar" ).progressbar({
		value: 20
	});
	

	// Hover states on the static widgets
	$( ".dialog-link, .icons li" ).hover(
		function() {
			$( this ).addClass( "ui-state-hover" );
		},
		function() {
			$( this ).removeClass( "ui-state-hover" );
		}
	);
});
