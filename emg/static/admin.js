$("#showModal").click(function () {
  $("#modal-form").addClass("is-active");
});

$(".modal-close").click(function () {
  $("#modal-form").removeClass("is-active");
});

$("#showModalCrop").click(function (e) {
  e.preventDefault()
  var zIndex = 1040 + (10 * $('.modal:visible').length);
  $(this).css('z-index', zIndex);
  setTimeout(function() {
      $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
  }, 0);

  $("#modal-crop").addClass("is-active");
});

$(".modal-crop-close").click(function () {
  $("#modal-crop").removeClass("is-active");
});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#img_display').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#img_person").change(function (e) {
  readURL(this);
});


//  $(document).ready(function(){
//    alert("ready");
//  })