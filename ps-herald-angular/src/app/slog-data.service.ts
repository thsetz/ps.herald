import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';

import { Searchvalues, SearchOptions } from './search-values'
import { Observable, Subject, throwError, of } from 'rxjs';
import { catchError, retry, tap, map} from 'rxjs/operators';
import { Log } from './log';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class SlogDataService {
  search_tuple = new Searchvalues();
  search_options = new SearchOptions();
  logs : Log[];

  private _refreshNeeded$ = new Subject<void>();
  url = "http://localhost:5000";
  get refreshNeeded$() {
    return this._refreshNeeded$;
  }
  refresh() {
    this._refreshNeeded$.next();
    this._oget();
  }
  get_params() {
    const params = new HttpParams()
      .set('system_id', this.search_tuple.system_id)
      .set('sub_system_id', this.search_tuple.sub_system_id)
      .set('sub_sub_system_id', this.search_tuple.sub_sub_system_id)
      .set('user_spec_1', this.search_tuple.user_spec_1)
      .set('user_spec_2', this.search_tuple.user_spec_2)
      .set('produkt_id', this.search_tuple.produkt_id)
      .set('pattern', this.search_tuple.pattern)
      .set('starting_at', this.search_tuple.starting_at)
      .set('notify_level', this.search_tuple.notify_level)
      .set('num_records', this.search_tuple.num_records)
      .set('order', this.search_tuple.order)
    return params;
  }
  getData(): Observable<Log[]> {
    let params = this.get_params();
    return this.http.get<Log[]>(this.url + "/angular/list", { params });
  }

  _oget() {
    //this.http.get<any>('http://localhost:5000/angular/options').subscribe({
    this.http.get<any>(this.url + '/angular/options').subscribe({
      next: data => {
        this.search_options["system_ids"] = data.system_ids;
        this.search_options["sub_system_ids"] = data.sub_system_ids;
        this.search_options["sub_sub_system_ids"] = data.sub_sub_system_ids;
        this.search_options["user_spec_1s"] = data.user_spec_1s;
        this.search_options["user_spec_2s"] = data.user_spec_2s;
        this.search_options["produkt_ids"] = data.produkt_ids;
      },
      error: error => {
        this.messageService.add("Option ERR Handler called with " + error)
        console.error('There was an error!', error);
      }
    })
  }

  constructor(private http: HttpClient, private messageService: MessageService ) { 
    this.messageService.add("data service: constructed");
    this._oget() ;

  }
}
