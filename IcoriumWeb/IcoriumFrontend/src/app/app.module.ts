import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HttpModule } from '@angular/http';
import { Ng2PageScrollModule } from 'ng2-page-scroll';
import { Ng2AutoCompleteModule } from 'ng2-auto-complete';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { IcoListComponent } from './ico-list/ico-list.component';
import { AppRoutingModule } from './app-routing.module';
import { IcoItemComponent } from './ico-item/ico-item.component';
import { IcoApiService} from './ico-api.service';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    IcoListComponent,
    IcoItemComponent,
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    Ng2PageScrollModule,
    Ng2AutoCompleteModule,
    AppRoutingModule
  ],
  providers: [IcoApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
