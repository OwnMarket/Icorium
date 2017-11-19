import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { DisclaimerComponent } from '../disclaimer/disclaimer.component';

@NgModule({
  declarations: [
    DisclaimerComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild([
      { path: '', component: DisclaimerComponent }
    ])
  ]
})
export class DisclaimerModule { }
