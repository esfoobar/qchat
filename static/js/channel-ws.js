document.addEventListener("DOMContentLoaded", function () {
  // messageHtml = function (data) {
  //   const HTMLmarkup = `
  //         <div class="message-object">
  //           <div class="message-user-profile">
  //             <a href="/user/${data.user.username}">
  //               <img
  //                 class="img-thumbnail img-circle"
  //                 src="${data.user.images.image_url_sm}"
  //                 width="50"
  //                 height="50"
  //                 alt="${data.user.username}}"
  //               />
  //             </a>
  //           </div>
  //           <div class="message-body">
  //             <div class="message-body-username">
  //               <a href="/user/${data.user.username}">
  //                 @${data.user.username}
  //               </a>
  //             </div>
  //             ${data.body}
  //           </div>
  //       </div>
  //       `;

  //   return HTMLmarkup;
  // };

  var ws = new WebSocket(
    "ws://" + document.domain + ":" + location.port + "/channel-ws"
  );

  ws.onmessage = function (event) {
    //   var messages_dom = document.getElementById("chat-messages");
    //   var message_dom = document.createElement("text");
    //   message_dom.innerHTML = messageHtml(JSON.parse(event.data)).trim();
    //   messages_dom.appendChild(message_dom);
    console.log(JSON.parse(event.data));
  };
});
