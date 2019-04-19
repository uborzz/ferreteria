
//$( '#myNavbar .navbar-nav a' ).on( 'click', function () {
//    console.log("CLICK")
//	$( '#myNavbar .navbar-nav' ).find( 'li.active' ).removeClass( 'active' );
//	$( this ).parent( 'li' ).addClass( 'active' );
//});

//// When the user scrolls the page, execute myFunction
//window.onscroll = function() {myFunction()};
//
//// Get the footer
//var footer = $( "#sticky" );
//
//// Get the offset position of the navbar
//var sticky = footer.offsetTop;
//
//// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
//function myFunction() {
//  if (window.pageYOffset >= sticky) {
//    footer.classList.add("fixed")
//    console.log(">>>")
//  } else {
//    footer.classList.remove("fixed");
//    console.log("<<<")
//  }
//}
//
//


// FORM Cool
//$(function () {
//
//    // init the validator
//    // validator files are included in the download package
//    // otherwise download from http://1000hz.github.io/bootstrap-validator
//
//    $('#contact-form').validator();
//
//
//    // when the form is submitted
//    $('#contact-form').on('submit', function (e) {
//
//        // if the validator does not prevent form submit
//        if (!e.isDefaultPrevented()) {
//            var url = "contact.php";
//
//            // POST values in the background the the script URL
//            $.ajax({
//                type: "POST",
//                url: url,
//                data: $(this).serialize(),
//                success: function (data)
//                {
//                    // data = JSON object that contact.php returns
//
//                    // we recieve the type of the message: success x danger and apply it to the
//                    var messageAlert = 'alert-' + data.type;
//                    var messageText = data.message;
//
//                    // let's compose Bootstrap alert box HTML
//                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
//
//                    // If we have messageAlert and messageText
//                    if (messageAlert && messageText) {
//                        // inject the alert to .messages div in our form
//                        $('#contact-form').find('.messages').html(alertBox);
//                        // empty the form
//                        $('#contact-form')[0].reset();
//                    }
//                }
//            });
//            return false;
//        }
//    })
//});
