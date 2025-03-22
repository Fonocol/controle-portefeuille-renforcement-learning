import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { HeaderComponent } from './components/header/header.component';
import { MetricsComponent } from './components/metrics/metrics.component';
import { ChartComponent } from './components/chart/chart.component';
import { FooterComponent } from './components/footer/footer.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


const config: SocketIoConfig = { url: 'http://localhost:5000', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    HeaderComponent,
    MetricsComponent,
    ChartComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SocketIoModule.forRoot(config),
    BrowserAnimationsModule, 
    NgxChartsModule,
     
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
