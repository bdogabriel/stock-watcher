import StockPriceChart from "./stockPriceChart.js";

// variables
const watchStockSlug = JSON.parse(
	document.getElementById("watch-stock").textContent
).slug;

if (watchStockSlug) {
	const socket = new WebSocket(
		`ws://${window.location.host}/ws/stocks/${watchStockSlug}/`
	);

	const chart = new StockPriceChart(watchStockSlug);
	await chart.setup();

	socket.onmessage = function (e) {
		const data = JSON.parse(e.data).prices;
		chart.updateData(
			data.map((el) => Number(el.price)),
			data.map((el) => new Date(el.timestamp))
		);
	};
}
