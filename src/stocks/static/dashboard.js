// variables
const watchStock = JSON.parse(
	document.getElementById("watch-stock").textContent
);
const slug = watchStock.slug;

let webSocketUrl;
let socket;

const ctx = document.getElementById("stock-price-chart");
let chart;

let prices = [];
let times = [];

// test variables
const tunel = {
	basePrice: 38,
	range: 0.01,
	interval: 5, // minutes
};

const fetchPrices = async () => {
	if (!slug) {
		return [];
	}
	const response = await fetch(`${window.location.href}prices/`);
	const data = await response.json();
	prices = data.prices.map((el) => Number(el.price));
	times = data.prices.map((el) => new Date(el.timestamp));
};

const drawChart = async () => {
	if (prices.length < 1) {
		await fetchPrices();
	}

	lastTime = times[times.length - 1];
	time_history = 30;
	time_forecast = 15;
	maxTime = new Date(lastTime.getTime() + time_forecast * 60000);
	minTime = new Date(lastTime.getTime() - time_history * 60000);

	chart = new Chart(ctx, {
		type: "line",
		data: {
			labels: times,
			datasets: [
				{
					label: "price",
					data: prices,
					borderWidth: 1,
				},
			],
		},
		options: {
			responsive: true,
			scales: {
				x: {
					type: "time",
					time: {
						displayFormats: {
							minute: "HH:mm",
						},
					},
					min: minTime,
					max: maxTime,
				},
				y: {
					min: tunel.basePrice - tunel.basePrice * tunel.range,
					max: tunel.basePrice + tunel.basePrice * tunel.range,
				},
			},
		},
	});
};

const updateChart = () => {
	chart.data.datasets[0].data.push(prices[prices.length - 1]);
	chart.data.labels.push(times[times.length - 1]);

	lastTime = times[times.length - 1];
	time_history = 30;
	time_forecast = 15;
	maxTime = new Date(lastTime.getTime() + time_forecast * 60000);
	minTime = new Date(lastTime.getTime() - time_history * 60000);

	chart.options.scales.x.min = minTime;
	chart.options.scales.x.max = maxTime;

	chart.update();
};

// main
drawChart();

if (slug) {
	webSocketUrl = `ws://${window.location.host}/ws/stocks/${slug}/`;
	socket = new WebSocket(webSocketUrl);

	socket.onmessage = function (e) {
		data = JSON.parse(e.data);
		prices = data.prices.map((el) => Number(el.price));
		times = data.prices.map((el) => new Date(el.timestamp));
		updateChart();
	};
}
