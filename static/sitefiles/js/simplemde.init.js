function toHTML(markdown) {
    var rendered_html = null;
    $.ajax({
        url: '/simplemde/md2html/',
        type: 'POST',
        'async': false,
        data: {content: markdown, csrfmiddlewaretoken: csrftoken},
        success: function (response) {
            rendered_html = response;
        }
    });

    return rendered_html;
}

$('#imageUploadModal').on('click', '#imageUpload', function(){
    // when imageUpload button is clicked..
    var $img = $('#browseImage');

    // if there was no image selected to upload.
    if ($img.val() == ''){
        Materialize.toast('No image selected.', 2000);
        return;
    }

    // image exists, lets start uploading process
    Materialize.toast('Upoading image...', 2000);

    var imageForm = new FormData();
    imageForm.append('image', $img.prop('files')[0]);
    imageForm.append('csrfmiddlewaretoken', csrftoken);

    $.ajax({
        url: '/simplemde/upload/',
        type: 'POST',
        data: imageForm,
        processData: false,
        contentType: false,
        success: function (response){
            if (response.success){
                // image upload was successful.
                Materialize.toast('Image upload successful.', 2000);
                // insert image link to the input below upload button.
                $('#imageURL').val(response.imgURL);
                // clear file input
                $img.val('');
                $('#filePathInput').val('');
            } else {
                // server replied that Something is wrong with the image.
                Materialize.toast('Invalid image file.', 2000);
            }
        },
        error: function(){
            // Something is wrong with the server.
            Materialize.toast('Something went wrong', 2000);
        }
    });
});

$('#imageUploadModal').on('click', '#insertImageButton', function () {
    // when insert image button is clicked...
    var editor = simplemde;
    var cm = editor.codemirror;
    var options = editor.options;
    // get current text/url in imageURL input tag
    var imgURL = $('#imageURL').val();
    // insert image markdown tag into editor
    _insertImage(cm, options.insertTexts.image, imgURL);
    $('#imageUploadModal').closeModal();
    // remove stale url from input.
    $('#imageURL').val('');
});

function insertImage(editor) {
    // base function that handles image upload/insertion.
    var cm = editor.codemirror;

    // gets selected text when image button was clicked (if any)
    var selectedText = cm.getSelection();

    // if there was a selected text, it treats that text as url
    // and inserts a image markdown tag around it.
    if (selectedText) {
        _insertImage(cm, editor.options.insertTexts.image, selectedText);
    } else {
        // if there was no text, a modal is opened..
        // here user can either upload or directly insert image with link.
        $('#imageUploadModal').openModal();
    }

}

function _insertImage(cm, startEnd, imgURL) {
    // takes image url as text and returns a markdownded image text.
    // startEnd: begining and end of image markdown tag to wrap around url.
    // cm: CodeMirror instance (SimpleMDE works on CodeMirror)
    // this function is a sliced version of one of the functions in SMDE's js file.

    var start = startEnd[0];
    var end = startEnd[1];
    var startPoint = cm.getCursor("start");
    var endPoint = cm.getCursor("end");

    cm.replaceSelection(start + imgURL + end);

    startPoint.ch += start.length;
    if (startPoint !== endPoint) {
        endPoint.ch += start.length;
    }

    cm.setSelection(startPoint, endPoint);
    cm.focus();
}

var simplemde = new SimpleMDE({
    element: $('.simplemde-editor')[0],

    toolbar: [
    'bold', 'italic', 'strikethrough',
    '|',
    'table', 'link',
    {
        name: 'image',
        action: insertImage,
        className: 'fa fa-picture-o',
        title: 'Insert Image'
    },
    '|',
    'heading', 'heading-1', 'heading-2', 'heading-3',
    '|',
    'quote', 'unordered-list', 'ordered-list',
    '|',
    'preview', 'side-by-side', 'fullscreen',
    '|',
    'guide'],

    previewRender: function (plainText, preview) {
        setTimeout(function () {
            preview.innerHTML = toHTML(plainText);
        }, 250);

        return "Loading...";
    },

    insertTexts: {
        image: ["![](", ")"]
    }
});
