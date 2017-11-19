import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Ng2PageScrollModule } from 'ng2-page-scroll';

import { IcoDetailsComponent } from '../ico-details/ico-details.component';

@NgModule({
  declarations: [
    IcoDetailsComponent
  ],
  imports: [
    CommonModule,
    Ng2PageScrollModule,
    RouterModule.forChild([
      { path: '', component: IcoDetailsComponent }
    ])
  ]
})
export class IcoDetailsModule { }
