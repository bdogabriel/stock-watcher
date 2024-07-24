import StockPriceChart from "./stockPriceChart.js";

// variables
const watchStockSlug = JSON.parse(
	document.getElementById("watch-stock").textContent
).slug;

if (watchStockSlug) {
	const socket = new WebSocket(
		`ws://${window.location.host}/ws/stocks/${watchStockSlug}/`
	);

	socket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		chart.prices = data.prices.map((el) => Number(el.price));
		chart.times = data.prices.map((el) => new Date(el.timestamp));
		chart.updateChart();
	};

	const chart = new StockPriceChart("stock-price-chart", watchStockSlug);
	chart.drawChart();
}
