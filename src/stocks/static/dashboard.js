const watchStock = JSON.parse(
	document.getElementById("watch-stock").textContent
);
const stockId = watchStock.id;

webSocketUrl = `ws://${window.location.host}/ws/stocks/${stockId}/`;
socket = new WebSocket(webSocketUrl);

socket.onmessage = function (e) {
	console.log("server: " + e.data);
	updateChart(JSON.parse(e.data).prices.map((el) => el.price));
};

const fetchPrices = async () => {
	const response = await fetch(`${window.location.href}prices/`);
	const data = await response.json();
	return data.prices.map((el) => el.price);
};

const ctx = document.getElementById("stock-price-chart");
let chart;

const drawChart = async (prices) => {
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

drawChart(fetchPrices());

const updateChart = async (prices) => {
	if (chart) {
		chart.destroy();
	}

	await drawChart(prices);
};
