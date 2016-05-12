$(function () {
    $('#postcomment').on('submit', function (event) {
        event.preventDefault();

        var $comment_val = $.trim($("#id_comment").val());
        if ($comment_val.length) {

            var $form = $('#postcomment');
            template = $('#comment-item').html();
            console.log($form);

            $.ajax({
                url: $form.attr('action'),
                type: 'POST',
                data: $form.serialize(),

                success: function (ajax_data) {
                    if (ajax_data.success) {
                        Materialize.toast(ajax_data.msg, 4000);
                        var rendered_html = Mustache.render(template, ajax_data.data);

                        var $comment_list = $('.user-comments');
                        $comment_list.prepend(rendered_html);

                        var tdl = $('li.c[data-comment-id=' + ajax_data.data.id + '] a.comment-datetime');
                        tdl.html(moment(ajax_data.data.created).format('LLL'));
                        tdl.attr('href', '#' + ajax_data.data.id);
                        var t = $('li.c[data-comment-id=' + ajax_data.data.id + ']');
                        if (t.length) {
                            event.preventDefault();
                            $offset = t.offset().top - 110;
                            $('html, body').animate({
                                scrollTop: $offset
                            }, 1000);
                        }
                        for (var ia = 0; ia < 3; ia++) {
                            t.fadeTo('slow', 0.2).fadeTo('slow', 1.0);
                        }
                        $.each($dt, function (i, datetime) {
                        });
                        $('.no-comment-string').fadeOut();
                    }
                    else {
                        Materialize.toast(ajax_data.msg, 4000, 'error');
                    }
                }

            })
        }
        else {
            Materialize.toast('Comment can\'t be empty', 4000, 'error');
        }


    });
});
