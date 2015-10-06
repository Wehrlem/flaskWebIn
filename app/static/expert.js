 $(function() {

      $('.jaja').on('click',function (){
            //Get the username
             var user = username;
            //Get the current input value
             var feature = $(this).attr('id');
             var option = $('input[type="radio"]:checked', '.'+feature).val();
             console.log(option);
             console.log(username);

             console.log(feature);

             $.ajax({
                 url: '/expertssave',
                 data: {selected:option, user:user, feature:feature },
                 type: 'POST',
                 cache: false,
                 success: function (response) {
                     $('#'+feature+'first').text(option);
                     $('#modal'+feature).closeModal();
                     console.log(response);
                 },
                 error: function (error) {
                     console.log(error);
                 }
             });
         });
  });