import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
declare var $: any;

@Component({
  selector: 'app-translate',
  templateUrl: './translate.component.html',
  styleUrls: ['./translate.component.css']
})

export class TranslateComponent implements OnInit {

  lang = "en"
  url = "http://localhost:55555/translate"

  constructor(private httpClient: HttpClient) { }

  ngOnInit() {
    $(".alert").hide()
  }

  translate() {
    console.log(this.lang)

    this.httpClient.post(this.url, { "text": $("#input").val(), "lang": this.lang }).subscribe(
      data => {
        console.log(JSON.stringify(data))
        $("#output").val(data["text"])
      }, error => { 
        console.log(JSON.stringify(error)) 
        $(".alert").show()
      }

    )

  }

  randomTranslation() {
    $("#random").val("soon")
  }

  setLang(l: string) {
    this.lang = l
  }

}
