import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { MarketComponent } from '../market/market.component';

@NgModule({
  declarations: [
    MarketComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild([
      { path: '', component: MarketComponent }
    ])
  ]
})
export class MarketModule { }
