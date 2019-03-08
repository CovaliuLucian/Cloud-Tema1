import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare var $: any;

@Component({
  selector: 'app-se',
  templateUrl: './se.component.html',
  styleUrls: ['./se.component.css']
})
export class SeComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  url = "http://localhost:55555/se"

  ngOnInit() {
  }

  se(){
    this.httpClient.get(this.url).subscribe(
      data => {
        console.log(JSON.stringify(data))
        $("#se").val(data["title"])
      }, error => {
        console.log(JSON.stringify(error))
      }

    )
  }

}
