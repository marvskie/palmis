let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let attachButton = $('#btn-attach');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user" id="${data[i]['username']}">${data[i]['get_full_name']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.id);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    console.log(message)
    if (message.user !== currentUser && message.seen_timestamp === null ){
        console.log('updating seen timestamp');
        setSeenTimestamp(message, date)
    }
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br><hr>
                            <span class="small timestamp">Sent: ${date}</span><br>
                            <span class="small timestamp" id="seen-${message.id}">Seen: ${message.seen_timestamp}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    //update messages to seen 

    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setSeenTimestamp(message, date) {
    let payload = {
        recipient: message.recipient, 
        body: message.body
    }
    $.ajax({
        url: `/api/v1/message/${message.id}/`,
        method: 'PUT',
        data: JSON.stringify(payload),
        contentType:'application/json', 
        success: function(result){
            console.log('updated seen status')
        }, 
        error: function(request, msg, error){
            alert('Error! Check console!');
        } 
    })
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {

    $('#fileupload').fileupload({
        dataType: 'json',
        add: function (e, data) {
            data.context = $('<p class="file">')
                .append($('<a target="_blank">').text(data.files[0].name))
                .appendTo($('#attachedFile'));

            attachButton.click(()=>{
                data.context.appendTo($('#attachedFile'));
                data.submit()
            })
            
        }
    });

    updateUserList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });


    socket.onmessage = function (e) {
        let data = JSON.parse(e.data).message;
        let payload = data.split('|')
        console.log(payload)
        if(payload.length > 1){
            console.log("seen update receieved")

            $(`#seen-${payload[0]}`).text(`Seen: ${payload[1]}`)
        }else{
            console.log("message receieved")

            getMessageById(e.data);
        }
        
    };
});



