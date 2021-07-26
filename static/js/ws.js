document.addEventListener("DOMContentLoaded", function () {
  postHtml = function (data) {
    const HTMLmarkup = `
        <div class="media" id="post-${data.post_uid}">
          <div class="media-left">
            <a href="${data.user_profile_url}">
              <img class="media-object" src="${data.user_image}" alt="${data.username}">
            </a>
          </div>
          <div class="media-body">
            <a href="${data.user_profile_url}">
              <div class="media-username">@${data.username}</div>
            </a>      
            <div class="media-body-text" id="post-text-${data.post_uid}">${data.body}</div>
            <div class="media-body-datetime">
              <span id="post-datetime-${data.post_uid}">${data.datetime}</span>&nbsp;-&nbsp;
              <a class="post-comment-link" data-post-uid="${data.post_uid}" href="#">Comment</a>&nbsp;-&nbsp;
              <a class="post-like-link" data-post-uid="${data.post_uid}" href="#">Like</a>
            </div>
            <div id="media-body-likes-list-${data.post_uid}" style="display: none">
              <span class="likes-label">Liked by</span>:
              <span class="likes-list" id="span-likes-list-${data.post_uid}">
              </span>
            </div>        
            <div class="media-body-comments-list">
              <ul id="post-${data.post_uid}-comment-list">
              </ul>
            </div>
            <div class="media-body-comment-entry" id="post-${data.post_uid}-comment" style="display: none;">
              <textarea
                name="post-comment"
                class="form-control"
                id="post-${data.post_uid}-comment-text"            
                rows="3"
                placeholder="Add your comment"></textarea>
              <button data-post-uid="${data.post_uid}" class="btn btn-primary post-comment-btn">Post</button>
            </div>
          </div>
        </div>
        <hr />
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
    var message_dom = document.createElement("li");
    var content_dom = document.createTextNode(event.data);
    message_dom.appendChild(content_dom);
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
