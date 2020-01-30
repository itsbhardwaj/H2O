function submitFeedback() {
    var Name = $("#name").val();
    var Feedback = $("#feedback").val();
    if (Name == '' || Feedback.trim() == '') {
        $("#error-toast").toast('show');
        return;
    }
    $.ajax({
        type: 'POST',
        url: 'feedback',
        data: { name: Name, feedback: Feedback },
        error: function (response) {},
        success: function (response) {
            $("#success-toast").toast('show');
            $("#name").val('');
            $("#feedback").val('');
            updateFeedbacks();
        }
    });
}

function updateFeedbacks() {
    $.ajax({
        type: 'GET',
        url: 'feedback',
        data: {},
        error: function (response) {},
        success: function (response) {
            response = JSON.parse(response);
            var text = '';
            if (response['data'].length == 0) {
                text = '<li>No Feedbacks yet!</li>'
            } else {
                for (var i = 0; i < response['data'].length; i++) {
                    text += '<li>'
                        + '<div class="container-fluid" >'
                        + '<div class="row feedback-datetime">'
                        + response['data'][i]['created_date']
                        + '</div>'
                        + '<div class="row feedback-text">'
                        + '<p>' + response['data'][i]['feedback'].replace(/\n/g, "<br/>") + '</p>'
                        + '</div>'
                        + '<div class="row float-right feedback-name">'
                        + '-' + response['data'][i]['name']
                        + '</div>'
                        + '</div>'
                        + '</li>';
                }
            }
            document.getElementById("feedbacks-list").innerHTML = text;
        }
    });
}

$(document).ready(function () {
    updateFeedbacks();
});