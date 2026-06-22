async function sendMessage(){

let input =
document.getElementById("user-input");

let message =
input.value;

if(message.trim()==="")
return;

let chatBox =
document.getElementById("chat-box");

chatBox.innerHTML +=
`
<div class="user-message">
${message}
</div>
`;

let response =
await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
message:message
})

});

let data =
await response.json();

chatBox.innerHTML +=
`
<div class="bot-message">
${data.response}
</div>
`;

input.value="";

chatBox.scrollTop =
chatBox.scrollHeight;
}