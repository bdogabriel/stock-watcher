class StockPriceChart {
	chart;
	stock;
	prices = [];
	tunnel = { upper: [], lower: [] };
	times = [];
	chartHistory = 30; // minutes
	chartForecast = 15; // minutes
	canvas;
	messageDiv;
	stockConfig;
	// tunnelColor = "#F43F5E"; // rose
	tunnelColor = "#F1BD2D"; // amber

	constructor(
		stock,
		stockConfig,
		canvasId = "stock-price-chart-canvas",
		messageDivId = "stock-price-chart-message-div"
	) {
		this.stock = stock;
		this.stockConfig = stockConfig;
		this.canvas = document.getElementById(canvasId);
		this.messageDiv = document.getElementById(messageDivId);
	}

	async setup() {
		const response = await fetch(
			`${window.origin}/stocks/${this.stock.slug}/prices/`
		);
		const jsonData = await response.json();
		const data = await jsonData.prices;

		if (data.length < 5) {
			this.messageDiv.style.display = "block";
			this.canvas.style.display = "none";
		} else {
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
		} else if (this.prices.length > 4) {
			this.canvas.style.display = "";
			this.messageDiv.style.display = "none";
			this.updateTunnel(this.prices);
			this.drawChart();
		}
	}

	updateTunnel(prices) {
		prices = [63, 64, 65, 66, 63, 64, 65, 66, 63, 64, 65, 66];
		const range = this.stockConfig.tunnel_range;
		const interval = this.stockConfig.tunnel_time_interval;

		this.tunnel = {
			upper: [],
			lower: [],
		};

		if (interval === 0) {
			let lcp = Number(this.stock.last_closing_price);
			this.tunnel = {
				upper: Array(prices.length).fill(lcp + lcp * range),
				lower: Array(prices.length).fill(lcp - lcp * range),
			};
		} else {
			this.tunnel.stepped = interval > 1;
			for (let p = 0; p < prices.length; p += interval) {
				this.tunnel.upper = this.tunnel.upper.concat(
					Array(interval).fill(prices[p] + prices[p] * range)
				);
				this.tunnel.lower = this.tunnel.lower.concat(
					Array(interval).fill(prices[p] - prices[p] * range)
				);
			}
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
						data: this.tunnel.upper,
						borderColor: this.tunnelColor,
						backgroundColor: this.tunnelColor,
						stepped: this.tunnel.stepped,
					},
					{
						label: "Price",
						data: this.prices,
						borderColor: "#14B8A6",
						backgroundColor: "#14B8A6",
					},
					{
						label: "Tunnel Lower",
						data: this.tunnel.lower,
						borderColor: this.tunnelColor,
						backgroundColor: this.tunnelColor,
						stepped: this.tunnel.stepped,
					},
					// {
					// 	label: "Last Closing Price",
					// 	data: Array(this.prices.length).fill(
					// 		Number(this.stock.last_closing_price)
					// 	),
					// 	borderColor: "gray",
					// 	backgroundColor: "gray",
					// 	borderDash: [8, 8],
					// },
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				elements: {
					point: {
						radius: 0,
						hitRadius: 10,
					},
					line: {
						borderWidth: 4,
					},
				},
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
							stepSize: 1,
						},
					},
				},
			},
		});
	}

	getMinMaxTimes(times) {
		function roundDate(date) {
			return new Date(Math.round(date.getTime() / 60000) * 60000);
		}

		const lastTime = times[times.length - 1];

		let max = new Date(lastTime.getTime() + this.chartForecast * 60000);
		let min = times[0];

		if (times.length > this.chartHistory) {
			min = new Date(
				lastTime.getTime() - (this.chartHistory - 1) * 60000
			);
		}

		return [roundDate(min), roundDate(max)];
	}

	updateChart() {
		const lastPrice = this.prices.length
			? this.prices[this.prices.length - 1]
			: undefined;

		if (lastPrice) {
			// updating data
			this.chart.data.datasets[1].data.push(lastPrice);

			// this.chart.data.datasets[3].data.push(
			// 	Number(this.stock.last_closing_price)
			// );

			this.updateTunnel(this.chart.data.datasets[1].data);

			this.chart.data.datasets[0].data.push(
				this.tunnel.upper[this.tunnel.upper.length - 1]
			);
			this.chart.data.datasets[2].data.push(
				this.tunnel.lower[this.tunnel.upper.length - 1]
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
