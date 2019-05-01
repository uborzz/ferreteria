
//$( '#myNavbar .navbar-nav a' ).on( 'click', function () {
//    console.log("CLICK")
//	$( '#myNavbar .navbar-nav' ).find( 'li.active' ).removeClass( 'active' );
//	$( this ).parent( 'li' ).addClass( 'active' );
//});


// //// When the user scrolls the page, execute myFunction
window.onscroll = function() {ajusta_footer()};

// probando on resize.
window.onresize = function(){ajusta_footer()};

//on load
$(document).ready(function(){
    ajusta_footer();
    $('input[type="file"]').change(function(){
        console.log("Escondiendo imagen guardada.")
        $('#imagen-en-base-datos')[0].style.visibility = 'hidden'
    });
});

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function ajusta_footer() {
 // Get the footer
  var footer = $( "#footer" )[0];
  //Get window size
  var window_size = window.innerHeight

  //Get page size
  var page_size = $("body")[0].offsetHeight
  //Get footer size
  var footer_size = footer.clientHeight
  // Calcula espacio sin ocupar
  var espacio_libre = window_size - page_size
  
  // console.log("Window Height " + window_size)
  // console.log("Page Height " + page_size)
  // console.log("Footer Height " + footer_size)
  // console.log("Resta Window-Page = " + espacio_libre)

  footer.style.visibility = 'visible';

  if ((espacio_libre) >= (footer_size)) {
    footer.classList.add("autofixed")
    console.log(">>>")
  } else {
    footer.classList.remove("autofixed");
    console.log("<<<")
  }
}
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
