const watchStock = JSON.parse(
	document.getElementById("watch-stock").textContent
);
const stockId = watchStock.id;

let webSocketUrl;
let socket;

if (stockId) {
	webSocketUrl = `ws://${window.location.host}/ws/stocks/${stockId}/`;
	socket = new WebSocket(webSocketUrl);

	socket.onmessage = function (e) {
		console.log("server: " + e.data);
		prices = JSON.parse(e.data).prices.map((el) => el.price);
		updateChart();
	};
}

let prices = [];

const fetchPrices = async () => {
	if (!stockId) {
		return [];
	}
	const response = await fetch(`${window.location.href}prices/`);
	const data = await response.json();
	prices = data.prices.map((el) => el.price);
};

const ctx = document.getElementById("stock-price-chart");
let chart;

const drawChart = async () => {
	if (prices.length < 1) {
		await fetchPrices();
	}

	chart = new Chart(ctx, {
		type: "line",
		data: {
			labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
			datasets: [
				{
					label: "price",
					data: prices,
					borderWidth: 1,
				},
			],
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});
};

drawChart();

const updateChart = async () => {
	if (chart) {
		chart.destroy();
	}

	await drawChart();
};
