import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TranslateComponent } from './translate/translate.component';
import { RandomComponent } from './random/random.component';
import { SeComponent } from './se/se.component';
import { MetricsComponent } from './metrics/metrics.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AppComponent } from './app.component';
import { BlankComponent } from './blank/blank.component';

const routes: Routes = [
  { path: '', component: BlankComponent },
  { path: 'translate', component: TranslateComponent },
  { path: 'random', component: RandomComponent },
  { path: 'se', component: SeComponent },
  { path: 'metrics', component: MetricsComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
