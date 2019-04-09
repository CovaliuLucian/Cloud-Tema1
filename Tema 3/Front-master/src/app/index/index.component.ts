import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs';
import { GoogleChartInterface } from 'ng2-google-charts/google-charts-interfaces';
declare var $: any;

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  images = []

  uploadEndpoint: string = 'https://upload-236609.appspot.com/upload'
  shotsEndpoint: string = 'https://refined-window-236417.appspot.com/shots/'
  labelsEndpoint: string = 'https://labels-236518.appspot.com/label/'
  bucketUrl: string = 'https://storage.googleapis.com/galeata_magica_123/'

  ngOnInit() {
  }

  fileToUpload: File = null;

  public columnChart: GoogleChartInterface = {
    chartType: 'ColumnChart',
    dataTable: [['Label', 'Confidence'], ['',0]],
    options: {
      title: 'Labels',
      animation: {
        duration: 1000,
        easing: 'out',
        startup: true,
      },
      height: 1000,
    }
  };

  postFile(fileToUpload: File): Observable<Object> {
    const endpoint = this.uploadEndpoint;
    const formData: FormData = new FormData();
    formData.append('fileKey', fileToUpload, fileToUpload.name);
    return this.httpClient
      .post(endpoint, formData)
  }

  handleFileInput(files: FileList) {
    let id: string
    this.fileToUpload = files.item(0);
    console.log(this.fileToUpload)
    this.postFile(this.fileToUpload).subscribe(
      data => {
        console.log("upload done")
        id = data["id"]
        //id = "a3e45367-2783-4d87-b397-07777a73ca56"
        console.log(id)
        let endpoint = this.shotsEndpoint + id
        this.httpClient.get(endpoint).subscribe(
          data => {
            console.log("shots done")
            console.log(data)
            let count = data["Counter"]
            this.images = []
            for (var i=0; i<count; i++) {
              this.images.push(id + '/' + i + ".jpg");
            }
            console.log(this.images)
            let endpoint = this.labelsEndpoint + id
            this.httpClient.get(endpoint).subscribe(
              data => {
                console.log("lables done")
                this.columnChart.dataTable = [['Label', 'Confidence']]
                var keys = Object.keys(data);
                for (var i = 0; i < keys.length; i++) {
                  this.columnChart.dataTable.push([keys[i],data[keys[i]]])
                }
                this.columnChart.component.draw()
              },
              error => {
                console.log("error at get labels")
                console.log(JSON.stringify(error))
              }
            )
          },
          error => {
            console.log("error at get shots")
            console.log(JSON.stringify(error))
          }
        )
      },
      error => {
        console.log("error at upload")
        console.log(JSON.stringify(error))
      })
  }

}
