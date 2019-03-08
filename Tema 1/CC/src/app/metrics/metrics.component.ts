import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { GoogleChartInterface } from 'ng2-google-charts/google-charts-interfaces';
declare var $: any;

@Component({
  selector: 'app-metrics',
  templateUrl: './metrics.component.html',
  styleUrls: ['./metrics.component.css']
})
export class MetricsComponent implements OnInit {

  url = "http://localhost:55555/metrics"
  metrics: any

  public pieChartR: GoogleChartInterface = {
    chartType: 'PieChart',
    dataTable: [],
    opt_firstRowIsData: true,
    options: { title: 'Random' },
  };

  public pieChartT: GoogleChartInterface = {
    chartType: 'PieChart',
    dataTable: [],
    opt_firstRowIsData: true,
    options: { title: 'Translation' },
  };

  public pieChartSE: GoogleChartInterface = {
    chartType: 'PieChart',
    dataTable: [],
    opt_firstRowIsData: true,
    options: { title: 'StackExchange', },
  };

  public columnChart: GoogleChartInterface = {
    chartType: 'ColumnChart',
    dataTable: [
      ['API', 'Min', 'Max', 'Average']
    ],
    options: {
      title: 'Latency',
      animation: {
        duration: 1000,
        easing: 'out',
        startup: true,
      },
      height: 1000
    }
  };

  constructor(private httpClient: HttpClient) { }

  ngOnInit() {
    this.getMetrics()
  }

  getMetrics() {
    this.httpClient.get(this.url).subscribe(
      data => {
        console.log(JSON.stringify(data))
        this.metrics = data
        console.log(this.metrics)
        this.pieChartR.dataTable = [['Failed', this.metrics["random"]["failed"]], ['Success', this.metrics["random"]["total"] - this.metrics["random"]["failed"]]]
        this.pieChartT.dataTable = [['Failed', this.metrics["translation"]["failed"]], ['Success', this.metrics["translation"]["total"] - this.metrics["translation"]["failed"]]]
        this.pieChartSE.dataTable = [['Failed', this.metrics["se"]["failed"]], ['Success', this.metrics["se"]["total"] - this.metrics["se"]["failed"]]]

        this.columnChart.dataTable.push(['Random', this.metrics["random"]["min_latency"], this.metrics["random"]["max_latency"], this.metrics["random"]["avg_latency"]])
        this.columnChart.dataTable.push(['Translation', this.metrics["translation"]["min_latency"], this.metrics["translation"]["max_latency"], this.metrics["translation"]["avg_latency"]])
        this.columnChart.dataTable.push(['Stack Exchange', this.metrics["se"]["min_latency"], this.metrics["se"]["max_latency"], this.metrics["se"]["avg_latency"]])
      }, error => {
        console.log(JSON.stringify(error))
      }
    )
  }

}
