import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-metrics',
  templateUrl: './metrics.component.html',
  styleUrl: './metrics.component.css'
})
export class MetricsComponent {
  @Input() agent: boolean = true;
  @Input() message: string = "";
  @Input() decision: string = '';
  @Input() decisionClass: string = '';
  @Input() total_value: number = 0;
  @Input() cash: number = 0;
  @Input() quantite_detenue: number = 0;


}
