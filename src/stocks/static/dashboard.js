const watchStock = JSON.parse(
	document.getElementById("watch_stock").textContent
);

console.log("watch stock", watchStock);

webSocketUrl = `ws://${window.location.host}/ws/stocks/${watchStock.id}/`;
socket = new WebSocket(webSocketUrl);

socket.onmessage = function (e) {
	console.log("server: " + e.data);
};

socket.onopen = function (e) {
	socket.send(
		JSON.stringify({
			message: "Hello from client",
			sender: "client",
		})
	);
};
console.log(socket);
