import { Component, Input } from '@angular/core';
import { Color, ScaleType } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrl: './chart.component.css'
})
export class ChartComponent {

  @Input() chartData: any[] = [];
  @Input() colorScheme: Color = {
    name: 'dark',
    selectable: true,
    group: ScaleType.Ordinal,
    domain: ['#00E676', '#FF4081', '#2979FF', '#FFA726']
  };

  
  index: number = 0;

  view: [number, number] = [900, 400];
  showXAxis = true;
  showYAxis = true;
  gradient = true;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Temps';
  showYAxisLabel = true;
  yAxisLabel = 'Valeur (€)';
  autoScale = true;
  timeline = true;
  animations = true;

}
