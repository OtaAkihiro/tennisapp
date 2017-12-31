//The javascript will submit the form via ajax when the user submits the form
//Before the page loads, we want to append the url that the user was previously at
	
$(document).ready(function(){

	alert('hi');
	//This function runs when the form is submitted
	$('#login_form').submit(function(event){

		event.preventDefault();
		$(".error").remove();
		//Get the data from the form and put it into an object
		var formData = {
			"username": $("#username_input").val(),
			"password": $("#password_input").val()
		};
		//Submit a post request using ajax
		$.ajax({
			type: 'POST',
			url: 'http://localhost:5000/api_login', //This is the url we want to send the data to
			contentType: "application/json", //We need to do this so api can parse the data
			data: JSON.stringify(formData), //^
			dataType: 'json', //We want to get json data back from the server
			
			//On success, reload the window
			success: function(data){

				window.location.href = 'http:localhost:5000/';
				return;
				}
			},
			/*
			error: function(data) {
				console.log(data);
				var obj = data['responseText'];
				var dict = JSON.parse(obj);
				//Iterate through all of the error messages and display them on the html page
				for (index in dict['errors']) {
					var insert = '<p class = "error">' + dict['errors'][index]['message'] + '</p>';
					$(document.body).append(insert);
				}
			}
			*/
		});
	});
});
