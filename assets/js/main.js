(function($) {
	
	// loader
	var loader = function() {
		setTimeout(function() { 
			if($('#ftco-loader').length > 0) {
				$('#ftco-loader').removeClass('show');
			}
		}, 1);
	};
	loader();

	// Code for logos carousel
	$('.logos').slick({
		arrows: false,
		autoplay: true,
		autoplaySpeed: 2000,
		infinite: true,
		slidesToShow: 7,
		slidesToScroll: 1,
		responsive: [
			{
				breakpoint: 920,
				settings: {
					slidesToShow: 5,
					slidesToScroll: 1,
				}
			},
			{
				breakpoint: 670,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 1,
				}
			}
		]
	});

	// Code for input animation
	let contactInputs = document.querySelectorAll('.in')

	function inputUp(e){
		e.target.parentElement.classList.add('active')
	}
	function inputDown(e){
		if(e.target.value.length < 1){
			e.target.parentElement.classList.remove('active')
		}
	}

	contactInputs.forEach(i=>{
		i.addEventListener('focus', inputUp)
		i.addEventListener('blur', inputDown)
	})

	// Code for magnific popup on project page
	try{
		$(".gallery .contents").magnificPopup({
			delegate: "a",
			type: "image",
			gallery: {
				enabled: true
			}
		});
	} catch(e){
		console.log(e);
	}

	// Code for making nav titles unclickable
	let disableA = document.querySelectorAll('.disableA')
	disableA.forEach(i => {
		i.addEventListener('click', killScroll);
	})
	function killScroll(e){
		e.preventDefault();
	}

	// Code for quote forms, changing of forms per level verification with ajax post
	let quoteform = document.querySelector('#quote-form .form-container')
	try{
		quoteform.addEventListener('submit', callJs)
	} catch(e){
		console.log(e);
	}

	function callJs(e) {
		e.preventDefault()
		let verified = false
		let form = e.target.parentElement		// ... perform ajax submission and verification
		// ... if verified move to next section else stay and display errors
		if(verified){
			let nextform = form.nextElementSibling
			// Check for positions and change active positions
			let positions = document.querySelectorAll('#quote-form .position span')
			positions.forEach(p=>{
				if (p.getAttribute('mark') == form.getAttribute('mark')){
					p.classList.toggle('active')
				} else if(p.getAttribute('mark') == nextform.getAttribute('mark')){
					p.classList.toggle('active')
				}
			})
			form.classList.toggle('active')
			nextform.classList.toggle('active')
		} else {
			form.classList.toggle('error')
		}
	}

	// try{
	// } catch(e){
	// 	console.log(e);
	// }

	// Code to make blog cards hover more dope
	let blogcard = document.querySelectorAll('.main-blog .posts .contents .card')
	try{
		blogcard.forEach(i=>{
			i.addEventListener('mouseenter',clipHover)
			i.addEventListener('mouseleave',clipRemove)
		})
	} catch(e){
		console.log(e);
	}
	function clipHover(e) {
		e.target.querySelector('.circle').style.clipPath='circle(700px at '+e.offsetX+'px '+e.offsetY+'px)'
	}
	function clipRemove(e) {
		let x = e.offsetX-16
		let y = e.offsetY-16
		e.target.querySelector('.circle').style.clipPath='circle(0px at '+x+'px '+y+'px)'
	}

	// Code to support radio buttons in contact page
	let radios = document.querySelectorAll('.direct .radio')
	try{
		radios.forEach(i=>{
			i.addEventListener('click', rotateClicked)
		}) 
	} catch(e){
		console.log(e);
	}
	function makeHidden(a) {
		a.forEach(i=>{
			let elem = document.getElementById(i)
			elem.style.display='none'
			if (i=='N'){
				Array.from(elem.children[1].children).forEach(x=>{
					x.children[0].checked=false
				})
			} else {
				elem.children[1].value = ''
				elem.classList.remove('active')
			}
		})
	}
	function rotateClicked(e) {
		let sender = e.target
		Array.from(e.path[2].children).forEach(x=>{
			let input = x.children[0]
			let label = x.children[1]
			try{
				if (input.isSameNode(sender) || label.isSameNode(sender)){
					input.checked = true
					// Make other display block
					let value = input.value
					let next = document.getElementById(value)
					console.log(next)
					try{
						next.style.display='block'
					} catch(e){			
					}
					if (value == 'E'){
						makeHidden(['N','G','R','O'])
					} else if (value == 'G'){
						makeHidden(['R','O'])
					} else if (value == 'R'){
						makeHidden(['G','O'])
					} else if (value == 'O'){
						makeHidden(['G','R'])
					}
				} else {
					input.checked = false
				}
			} catch(TypeError){
				
			}
		})
	}

	// Codes for focusing inputs with values
	let f_inputs = document.querySelectorAll('form .in')
	f_inputs.forEach(i=>{
		if (i.value){
			i.focus()
		}
	})

	// Code to remove alert
	$('.alert span').click(function() {
		$(this.parentElement).remove()
	})

	// Code to automate liking of posts
	$('.like .likes').click(function() {
		$('.like .likes').toggleClass('active')
		// Setting and sending ajax request
		var $thisURL = window.location.href // or set your own url
		var $data = {'sender':'likes'}
		$.ajax({
        method: "POST",
        url: $thisURL,
        data: $data,
        success: handleFormSuccess,
        error: handleFormError,
    	})
	})

	// Codes for Ajax
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function callComo(data, textStatus, jqXHR) {
        destroyLoader()
    }

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)
        let nlikes = parseInt($('.like .likes~p').html())
        if (data['action']=='+') {
        	nlikes++
        	$('.like .likes~p').html(nlikes)
        } else{
        	nlikes--
        	$('.like .likes~p').html(nlikes)
        }
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR)
        console.log(textStatus)
        console.log(errorThrown)
    }



})(jQuery);