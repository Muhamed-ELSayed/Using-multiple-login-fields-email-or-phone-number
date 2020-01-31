$(document).ready(function () {

  // open modal login form templates/user/login
 $('.ajax-login').click(function(){
   $.ajax({
     type: "get",
     url: "/login/",
     dataType: "json",
     beforeSend : function(){
      $('#modal-login').modal('open')
     },
     success: function (response) {
       $('#modal-login .modal-content').html(response.html_form)
     }
   });
 });

  // create function for modal-login 
 $('#modal-login').on('submit', '.login-form', function(e){
   e.preventDefault();
   var form= $(this);
   $.ajax({
     type: form.attr('method'),
     url: form.attr('data-url'),
     data: form.serialize(),
     dataType: "json",
     success: function (data, status) {
      if (data.user) {
        console.log('Log In Form Successfuly Summited')
        $('#modal-login').modal('close')
      }
     },
     error: function(error){
       var er=error.responseJSON
       var div_error = $(form).find('.form-error');
       var msg = ""
       $.each(er, function (key, value) { 
          msg += value[0].message
          div_error.text(msg)
       });
     }
   });
   return false;
 });


//  open modal register form templates/users/register
$('.ajax-register').click(function(e){
  $.ajax({
    type: "get",
    url: "/register/",
    dataType: "json",
    beforeSend: function(){
      $('#modal-register').modal('open')
    },
    success: function (response) {
      $('#modal-register .modal-content').html(response.html_form)
    }
  });
});

// create function for modal-register
$('#modal-register').on('submit', '.register-form', function(e){
  e.preventDefault();
  var form= $(this);
  $.ajax({
    type: form.attr('method'),
    url: form.attr('data-url'),
    data: form.serialize(),
    dataType: "json",
    success: function (data, status) {
     if (data.user) {
       console.log('Register Form Successfuly Summited')
       $('#modal-register').modal('close')
     }
    },
    error: function(error){
      var er=error.responseJSON
      var div_error = $(form).find('.form-error');
      var msg = ""
      $.each(er, function (key, value) { 
         msg += value[0].message
         div_error.text(msg)
      });
    }
  });
  return false;
})



});