
function add_author(){
	var author = $('.author-input:first').clone();
	author.css('display', 'inline-block');
	author.val('');

	$('.author-input').css('display', 'block');
	$('.authors .add-button').before(author);
	
	return false;
}

$(
	function(){
		$('.body .radioset #suggestion').click();
	}
);