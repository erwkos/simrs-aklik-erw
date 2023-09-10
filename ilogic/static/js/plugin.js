$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-data-klaim').modal('show');

			},
			success: function(data){
				$('#modal-register .modal-content').html(data.html_form);
			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		var data = new FormData(form.get(0));
		$.ajax({
			url: form.attr('data-url'),
			// data: form.serialize(),
			data : data,
			cache: false,
			processData: false,
			contentType: false,
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				// alert('sukses')
				// setInterval('location.reload()', 500);
				if(data.form_is_valid){
					$('#data-table tbody').html(data.tilik);
					$('#modal-register').modal('hide');
					setInterval('location.reload()', 500);
				} else {
					$('#modal-register .modal-content').html(data.html_form);
				}
			}
		})
		return false;
	}

// create
$(".show-form").click(ShowForm);
$("#modal-register").on("submit",".create-form",SaveForm);

//update
$('#modal-register').on("submit",".update-form",SaveForm);


});