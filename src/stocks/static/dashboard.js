url = "ws://" + window.location.host + "/ws/stocks/1/";
socket = new WebSocket(url);

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
