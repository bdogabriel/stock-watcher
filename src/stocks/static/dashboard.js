// variables
const watchStock = JSON.parse(
	document.getElementById("watch-stock").textContent
);
const slug = watchStock.slug;

let webSocketUrl;
let socket;

let chartData = [];

const ctx = document.getElementById("stock-price-chart");
let chart;

// functions
const formatDate = (date) => {
	const minutes = String(date.getMinutes()).padStart(2, "0");
	const hours = String(date.getHours()).padStart(2, "0");

	let ret = `${hours}:${minutes}`;
	return ret;
};

const fetchPrices = async () => {
	if (!slug) {
		return [];
	}
	const response = await fetch(`${window.location.href}prices/`);
	const data = await response.json();
	chartData = data.prices.map((el) => ({
		label: formatDate(new Date(el.timestamp)),
		data: el.price,
	}));
};

const drawChart = async () => {
	if (chartData.length < 1) {
		await fetchPrices();
	}

	chart = new Chart(ctx, {
		type: "line",
		data: {
			labels: chartData.map((el) => el.label),
			datasets: [
				{
					label: "price",
					data: chartData.map((el) => el.data),
					borderWidth: 1,
				},
			],
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
				x: {
					ticks: {
						maxTicksLimit: 30,
					},
				},
			},
		},
	});
};

const updateChart = () => {
	chart.data.datasets[0].data.push(chartData[chartData.length - 1].data);
	chart.data.labels.push(chartData[chartData.length - 1].label);
	chart.update();
};

// main
if (slug) {
	webSocketUrl = `ws://${window.location.host}/ws/stocks/${slug}/`;
	socket = new WebSocket(webSocketUrl);

	socket.onmessage = function (e) {
		data = JSON.parse(e.data);
		chartData = data.prices.map((el) => ({
			label: formatDate(new Date(el.timestamp)),
			data: el.price,
		}));
		updateChart();
	};
}

drawChart();
