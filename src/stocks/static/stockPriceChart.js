class StockPriceChart {
	prices = [];
	times = [];
	chartHistory = 30; // minutes
	chartForecast = 15; // minutes
	maxTime;
	minTime;
	chart;
	canvasId;
	ctx;
	stockSlug;

	tunnelConfig = {
		basePrice: 37,
		range: 0.001,
		interval: 5, // minutes
		color: "#F43F5E",
	};

	constructor(canvasId, stockSlug) {
		this.ctx = document.getElementById(canvasId);
		this.stockSlug = stockSlug;
	}

	fetchPrices = async () => {
		if (!this.stockSlug) {
			return [];
		}
		const response = await fetch(`${window.location.href}prices/`);
		const data = await response.json();
		this.prices = data.prices.map((el) => Number(el.price));
		this.times = data.prices.map((el) => new Date(el.timestamp));
	};

	drawChart = async () => {
		if (this.prices.length < 1) {
			await this.fetchPrices();
		}

		this.chart = new Chart(this.ctx, {
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
						min: this.minTime,
						max: this.maxTime,
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

		this.updateXAxis();
		this.chart.update();
	};

	updateData() {
		const lastPrice = this.prices[this.prices.length - 1];

		this.chart.data.datasets[0].data.push(
			lastPrice + lastPrice * this.tunnelConfig.range
		);
		this.chart.data.datasets[1].data.push(lastPrice);
		this.chart.data.datasets[2].data.push(
			lastPrice - lastPrice * this.tunnelConfig.range
		);

		this.chart.data.labels.push(this.times[this.times.length - 1]);
	}

	updateXAxis = () => {
		const lastTime = this.times[this.times.length - 1];

		this.maxTime = new Date(
			lastTime.getTime() + this.chartForecast * 60000
		);

		if (this.chart.data.datasets[1].data.length >= this.chartHistory) {
			this.minTime = new Date(
				lastTime.getTime() - this.chartHistory * 60000
			);
		} else {
			this.minTime = undefined;
		}

		this.chart.options.scales.x.min = this.minTime;
		this.chart.options.scales.x.max = this.maxTime;
	};

	updateChart() {
		this.updateData();
		this.updateXAxis();
		this.chart.update();
	}
}

export default StockPriceChart;
