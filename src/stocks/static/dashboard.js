import StockPriceChart from "./stockPriceChart.js";

// variables
const watchStock = JSON.parse(
	document.getElementById("watch-stock").textContent
);

const watchStockConfig = JSON.parse(
	document.getElementById("watch-stock-config").textContent
)[0];

if (watchStock.slug) {
	const socket = new WebSocket(
		`ws://${window.location.host}/ws/stocks/${watchStock.slug}/`
	);

	const chart = new StockPriceChart(watchStock, watchStockConfig);
	await chart.setup();

	socket.onmessage = function (e) {
		const data = JSON.parse(e.data).prices;
		chart.updateData(
			data.map((el) => Number(el.price)),
			data.map((el) => new Date(el.timestamp))
		);
	};
}
