
function add_author(){
	var author = $('.author-input').clone();
	author.css('display', 'block');
	$('.authors').prepend(author);
	
	return false;
}
