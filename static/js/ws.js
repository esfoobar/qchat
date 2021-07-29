document.addEventListener("DOMContentLoaded", function () {
  messageHtml = function (data) {
    const HTMLmarkup = `
          <div class="message-object"> 
            <div class="message-user-profile">
              <a href="/user/${data.username}">
                <img
                  class="img-thumbnail img-circle"
                  src="${data.user_images.image_url_sm}"
                  width="50"
                  height="50"
                  alt="${data.username}}"
                />
              </a>
            </div>
            <div class="message-body"> 
              <div class="message-body-username">
                <a href="/user/${data.username}">
                  @${data.username}
                </a>
              </div>
              ${data.body}
            </div>
        </div>
        `;

    return HTMLmarkup;
  };

  var cursorId = qChat.cursorId;

  var ws = new WebSocket(
    "ws://" +
      document.domain +
      ":" +
      location.port +
      "/ws?cursor_id=" +
      cursorId
  );

  ws.onmessage = function (event) {
    var messages_dom = document.getElementById("chat-messages");
    var message_dom = document.createElement("text");
    message_dom.innerHTML = messageHtml(JSON.parse(event.data)).trim();
    messages_dom.appendChild(message_dom);
  };

  var button = document.getElementById("chat-message-button");
  button.onclick = function () {
    var messageInput = document.getElementById("chat-message-input");
    var content = messageInput.value;
    ws.send(content);
    messageInput.value = "";
  };
});
