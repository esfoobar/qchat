document.addEventListener("DOMContentLoaded", function () {
  channelUserHtml = function (channelUserData) {
    const HTMLmarkup = `
      <div class="user-object"> 
        <div class="channel-user-profile">
          <a href="/user/${channelUserData.username}">
            <img
              class="img-thumbnail img-circle"
              src="${channelUserData.images.image_url_sm}"
              width="50"
              height="50"
              alt="${channelUserData.username}"
            />
            </a>
            <div class="channel-user-body"> 
              <div class="channel-user-body-username">
                <a href="/user/${channelUserData.username}">
                  @${channelUserData.username}
                </a>
              </div>
            </div>            
        </div>
      </div>
        `;

    return HTMLmarkup;
  };

  var ws = new WebSocket(
    "ws://" + document.domain + ":" + location.port + "/channel-ws"
  );

  ws.onmessage = function (event) {
    var channelUsersElement = document.getElementById("channel-users");
    channelUsersData = JSON.parse(event.data).users;
    var channel_users_dom = document.createElement("text");

    for (var i = 0; i < channelUsersData.length; i++) {
      var channel_user_dom = document.createElement("text");
      channel_user_dom.innerHTML = channelUserHtml(channelUsersData[i]).trim();
      channel_users_dom.appendChild(channel_user_dom);
    }
    channelUsersElement.innerHTML = channel_users_dom.outerHTML;
  };
});
