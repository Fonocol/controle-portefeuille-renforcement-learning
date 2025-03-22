import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../../services/websocket.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  decision: string = '';
  decisionClass: string = '';
  total_value: number = 0;
  cash: number = 0;
  quantite_detenue: number = 0;
  price:number = 0;
  chartData: any[] = [
    { name: 'Valeur du Portefeuille', series: [] },
    { name: 'Moyenne Mobile', series: [] }
  ];

  bandesChart : any[] = [
    { name: 'price', series: [] },
    { name: 'Upper Band', series: [] },
    { name: 'Lower Band', series: [] },
  ];

  rsiChartData: any[] = [
    { name: 'RSI', series: [] },
    { name: 'Upper', series: [] },
    { name: 'Lower', series: [] },
  ];

  



  constructor(private socketService: WebsocketService) {}

  ngOnInit() {
    this.socketService.getData().subscribe(data => {
      this.decision = data.decision;
      this.total_value = data.total_value;
      this.cash = data.cash;
      this.price = data.price;
      this.quantite_detenue= data.quantite_detenue;
      this.decisionClass = this.getDecisionClass(this.decision);

      this.updateStateChartData(data.timestamp, data.state);
      this.bandesChart[0].series.push({ name: data.timestamp, value: data.price });
      this.chartData[0].series.push({ name: data.timestamp, value: data.total_value });

      const prices = this.chartData[0].series.map((point: any) => point.value);
      const movingAverages = this.calculateMovingAverage(prices, 5);

      this.chartData[1].series = this.chartData[0].series
        .slice(4)
        .map((point: any, index: number) => ({
          name: point.name,
          value: movingAverages[index]
        }));

      this.chartData = [...this.chartData];
      this.bandesChart = [... this.bandesChart];

    });
  }

  calculateMovingAverage(prices: number[], windowSize: number): number[] {
    const movingAverages = [];
    for (let i = 0; i <= prices.length - windowSize; i++) {
      const window = prices.slice(i, i + windowSize);
      const average = window.reduce((sum, price) => sum + price, 0) / windowSize;
      movingAverages.push(average);
    }
    return movingAverages;
  }

  updateStateChartData(timestamp: string, state: number[]) {
    const [sma, rsi, macd, upperBand, lowerBand, cashRatio] = state;

    this.rsiChartData[0].series.push({ name: timestamp, value: rsi });
    this.rsiChartData[1].series.push({ name: timestamp, value: 70 });
    this.rsiChartData[2].series.push({ name: timestamp, value: 30 });

    this.bandesChart[1].series.push({ name: timestamp, value: upperBand });
    this.bandesChart[2].series.push({ name: timestamp, value: lowerBand });

    this.rsiChartData = [...this.rsiChartData];
  }

  getDecisionClass(decision: string): string {
    if (decision === 'Acheter') return 'buy';
    if (decision === 'Vendre') return 'sell';
    return 'neutral';
  }


  rsimessage = `Le RSI (Relative Strength Index) est un indicateur technique largement utilisé en analyse technique pour évaluer la force et la dynamique des mouvements de prix d'un actif. Il est particulièrement utile pour identifier les conditions de surachat (overbought) et de survente (oversold) sur les marchés financiers.`

}