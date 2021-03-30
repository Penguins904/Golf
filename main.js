var div = document.getElementsByClassName("cards")[0]
var cardElements = [].slice.call(div.getElementsByTagName("span"));
var cards = []
var hasStarted, isTurn = false; //game has started bool

for(let e of cardElements) {
  e.addEventListener("click", function(){flip(e)})
  if(cardElements.indexOf(e) > 1){
    e.addEventListener("mouseover", function(){showCard(e)}); //clicking flips card
    e.addEventListener("mouseout", function(){hideCard(e)}); //shows bottom cards when hovering
  }
}



var ws = new WebSocket("ws://golfcardgame.ddns.net") // creates socket
ws.onopen = function(event) {
  console.log("Connected");
  console.log("waiting for game to start");
};

ws.onmessage = function(event) { //runs when socket recives a message
  data = JSON.parse(event.data);
  console.log(data);
  switch (data.action) {
    case "start":
      start();
      break;
    case "give":
      give(data.cards);
      break;
    case "playerJoined":
      alert("number of players: " + data.players + "/" + data.max);
      console.log("number of players: " + data.players + "/" + data.max);
      break;
    case "test":
      console.log("test");
      break;
  }
};

function flip(element) {
  //ws.send(JSON.stringify({"action": "flip", "card": element.id}));
}

function showCard(element) {
  if(hasStarted) {
    element.innerHTML = cards[cardElements.indexOf(element)];
  }
}

function hideCard(element) {
  element.innerHTML = "&#127136;"; //HTML character code for back of a card
}

function start() {
  hasStarted = true;
  alert("Game has Started");
  console.log("Game has Started");
}

function give(c) {
  console.log("recived cards");
  cards = c;
}
