// marenee74

var tag = [];

$(document).ready(function() {

	$('#post').click(function() {
		
		$('#tmpl-bin').show();
	});

	$('.mk-nudle').click(function() {
		
		$('#tmpl-bin').show();
	});

	$('#add-Tag').click(function() {
		var tag = $('#tag');
		
		if ( tag.val().length !== 0 ) {
			
			$('#tag-bin').append("<p id='formatted-tag'>/"+ tag.val() +"</p>");	
		}
		tag.val('');
		
		$('#add-Tag').hide();
		$('#tag').hide();
	});
	
	$('#bin-post').click(function() {
		
		alert('posted your nudle');
		
		// var data = {
		// 	'title': $('#title').val(),
		// 	'info': $('#description').val(),
		// 	'text': $('#article').val(),
		// 	'coverPhoto': $('#pic').val(),
		// 	'tags': [ document.getElementById('formatted-tag').textContent.split('/').join('') ]
		// };
		
		// console.log( data );
		$.ajax({
			typ: 'POST',
			url: '/nudle/post_nudle/?ttl=' + $('#title').val() + '&info=' + $('#description').val() + '&text=' + $('#article').val() + '&coverPhoto=' + $('#pic').val() + '&tag='+ document.getElementById('formatted-tag').textContent.split('/').join(''),
			success: function ( resp ) {

				console.log('POST-ting nudle tag, ' + document.getElementById('formatted-tag').textContent.split('/').join('') );
				
				window.open( resp.url_path, '_self' );
			}
		});
	});

	$('#bin-exit').click(function() {
			
		var resp = confirm('are you sure?');

		if ( resp ) {
			$('#tmpl-bin').hide();
		}
	});

	$('#query').keydown(function( e ) {
		if( e.which === 13 ) {
			$.ajax({
				typ: 'GET',
				url: '/nudle/'+ $('#query').val() + '?i=form-box',
				success: function ( resp ) {
					console.log('GET-ting nudle tag, ' + $('#query').val() );
					window.open( resp.url_path, '_self' );
				}
			});
		}
	});

});
