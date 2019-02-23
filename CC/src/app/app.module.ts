import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AlertModule } from 'ngx-bootstrap';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TranslateComponent } from './translate/translate.component';
import { RandomComponent } from './random/random.component';
import { SeComponent } from './se/se.component';
import { MetricsComponent } from './metrics/metrics.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { BlankComponent } from './blank/blank.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    TranslateComponent,
    RandomComponent,
    SeComponent,
    MetricsComponent,
    PageNotFoundComponent,
    BlankComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AlertModule.forRoot(),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
