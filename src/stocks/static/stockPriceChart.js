class StockPriceChart {
	chart;
	stockSlug;
	prices = [];
	times = [];
	chartHistory = 30; // minutes
	chartForecast = 15; // minutes
	canvas;
	messageDiv;

	tunnelConfig = {
		basePrice: 37,
		range: 0.001,
		interval: 5, // minutes
		color: "#F43F5E",
	};

	constructor(
		stockSlug,
		canvasId = "stock-price-chart-canvas",
		messageDivId = "stock-price-chart-message-div"
	) {
		this.stockSlug = stockSlug;
		this.canvas = document.getElementById(canvasId);
		this.messageDiv = document.getElementById(messageDivId);
	}

	async setup() {
		const response = await fetch(`${window.location.href}prices/`);
		const jsonData = await response.json();
		const data = jsonData.prices;

		if (!data.length) {
			this.messageDiv.style.display = "block";
			this.canvas.style.display = "none";
		} else if (data.length > 2) {
			this.messageDiv.style.display = "none";
			this.canvas.style.display = "";
			this.updateData(
				data.map((el) => Number(el.price)),
				data.map((el) => new Date(el.timestamp))
			);
		}
	}

	updateData(prices, times) {
		this.prices = prices;
		this.times = times;

		if (this.chart) {
			this.updateChart();
		} else if (this.prices.length > 2) {
			this.drawChart();
			this.canvas.style.display = "";
		}
	}

	drawChart() {
		const [minTime, maxTime] = this.getMinMaxTimes(this.times);

		this.chart = new Chart(this.canvas, {
			type: "line",
			data: {
				labels: this.times,
				datasets: [
					{
						label: "Tunnel Upper",
						data: this.prices.map(
							(el) => el + el * this.tunnelConfig.range
						),
						borderWidth: 1,
						borderColor: this.tunnelConfig.color,
						backgroundColor: this.tunnelConfig.color,
					},
					{
						label: "Price",
						data: this.prices,
						borderWidth: 1,
						borderColor: "#14B8A6",
						backgroundColor: "#14B8A6",
					},
					{
						label: "Tunnel Lower",
						data: this.prices.map(
							(el) => el - el * this.tunnelConfig.range
						),
						borderWidth: 1,
						borderColor: this.tunnelConfig.color,
						backgroundColor: this.tunnelConfig.color,
					},
				],
			},
			options: {
				responsive: true,
				plugins: {
					legend: {
						display: false,
					},
				},
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
						ticks: {
							stepSize: 2,
						},
					},
					y: {
						ticks: {
							stepSize: 0.01,
						},
					},
				},
			},
		});
	}

	getMinMaxTimes(times) {
		const lastTime = times[times.length - 1];

		let max = new Date(lastTime.getTime() + this.chartForecast * 60000);
		let min = times[0];

		if (times.length >= this.chartHistory) {
			min = new Date(
				lastTime.getTime() - (this.chartHistory - 1) * 60000
			);
		}

		return [min, max];
	}

	updateChart() {
		const lastPrice = this.prices.length
			? this.prices[this.prices.length - 1]
			: undefined;

		if (lastPrice) {
			// updating data
			this.chart.data.datasets[0].data.push(
				lastPrice + lastPrice * this.tunnelConfig.range
			);
			this.chart.data.datasets[1].data.push(lastPrice);
			this.chart.data.datasets[2].data.push(
				lastPrice - lastPrice * this.tunnelConfig.range
			);

			this.chart.data.labels.push(this.times[this.times.length - 1]);

			// updating x axis
			const [minTime, maxTime] = this.getMinMaxTimes(
				this.chart.data.labels
			);

			this.chart.options.scales.x.min = minTime;
			this.chart.options.scales.x.max = maxTime;

			this.chart.update();
		}
	}
}

export default StockPriceChart;
