import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CmessagesComponent } from './cmessages/cmessages.component';
import { ClogFormComponent } from './clog-form/clog-form.component';
import { ClogListComponent } from './clog-list/clog-list.component';

@NgModule({
  declarations: [
    AppComponent,
    CmessagesComponent,
    ClogFormComponent,
    ClogListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
