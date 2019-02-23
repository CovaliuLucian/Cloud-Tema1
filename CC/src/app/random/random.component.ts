import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
declare var $: any;

@Component({
  selector: 'app-random',
  templateUrl: './random.component.html',
  styleUrls: ['./random.component.css']
})
export class RandomComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  url = "http://localhost:55555/random"

  ngOnInit() {
  }

  random() {
    this.httpClient.get(this.url).subscribe(
      data => {
        console.log(JSON.stringify(data))
        $("#random").val(data["number"])
      }, error => {
        console.log(JSON.stringify(error))
      }

    )

  }

}
