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
  urlRandom = "http://localhost:55555/random?min=0&max=5"
  urlSe = "http://localhost:55555/se"
  langs = ["en", "ro", "fr", "ru", "it", "de"]

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
    var title: string
    var lang: string
    this.httpClient.get(this.urlSe).subscribe(
      data => {
        console.log(JSON.stringify(data))
        title = data["title"]

        this.httpClient.get(this.urlRandom).subscribe(
          data => {
            console.log(JSON.stringify(data))
            lang = this.langs[data["number"]]

            this.httpClient.post(this.url, { "text": title, "lang": lang }).subscribe(
              data => {
                console.log(JSON.stringify(data))
                $("#random").val(data["text"])
              }, error => {
                console.log(JSON.stringify(error))
                $(".alert").show()
              }
            )
          }, error => {
            console.log(JSON.stringify(error))
          })
      }, error => {
        console.log(JSON.stringify(error))
      })




  }

  setLang(l: string) {
    this.lang = l
  }

}
