import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { IcoListComponent } from './ico-list/ico-list.component';

const routes = [
  { path: '', component: IcoListComponent },
  { path: 'ico-directory', component: IcoListComponent },
  { path: 'about', loadChildren: './about/about.module.ts#AboutModule' },
  { path: 'market', loadChildren: './market/market.module.ts#MarketModule' },
  { path: 'contact', loadChildren: './contact/contact.module.ts#ContactModule' },
  { path: 'disclaimer', loadChildren: './disclaimer/disclaimer.module.ts#DisclaimerModule' },
  { path: 'ico-details/:id', loadChildren: './ico-details/ico-details.module.ts#IcoDetailsModule' },
  { path: '**', redirectTo: '/' }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}
