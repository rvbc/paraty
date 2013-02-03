
function add_author(){
	var author = $('.author-input:last').clone();
	var ind = parseInt(author.attr('name').substring('escritor_'.length)) + 1;
	author.css('display', 'inline-block');
	author.val('');
	author.attr('name', 'escritor_'+ind);
	
	$('.author-input').css('display', 'block');
	$('.authors .add-button').before(author);
	
	return false;
}

$(
	function(){
		$('.header .radioset #suggestion').click();
	}
);
